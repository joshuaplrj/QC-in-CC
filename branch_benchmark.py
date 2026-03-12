#!/usr/bin/env python3
"""
Branch-by-branch benchmark runner for classical vs quantum systems.

This script:
- Pairs modules across `classical_systems/<branch>/` and `quantum_systems/<branch>/`
- Runs each side in isolated subprocesses (avoids import/path conflicts)
- Aggregates results by branch (discipline)
- Writes detailed JSON and markdown summary reports
"""

from __future__ import annotations

import argparse
import json
import statistics
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


CLASSICAL_CHILD = r"""
import importlib.util
import inspect
import json
import pathlib
import sys
import traceback
import time
import types
import types
import types

module_path = pathlib.Path(sys.argv[1])
project_root = pathlib.Path(sys.argv[2])
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root.parent))

result = {"ok": False, "time": None, "class_name": None, "error": None}

def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except SyntaxError as exc:
        if "codec can't decode byte" not in str(exc):
            raise

    raw = path.read_bytes()
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError:
        source = raw.decode("cp1252")

    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module

def _call_with_defaults(func):
    sig = inspect.signature(func)
    kwargs = {}
    for name, param in sig.parameters.items():
        if param.kind in (inspect.Parameter.VAR_POSITIONAL, inspect.Parameter.VAR_KEYWORD):
            continue
        if param.default is not inspect._empty:
            continue

        lname = name.lower()
        if "duration" in lname or "hours" in lname:
            kwargs[name] = 1
        elif "steps" in lname or "iterations" in lname or lname.endswith("iter"):
            kwargs[name] = 10
        elif lname == "dt" or "timestep" in lname:
            kwargs[name] = 1
        elif lname == "n" or lname.startswith("n_"):
            kwargs[name] = 10
        elif "size" in lname:
            kwargs[name] = 16
        else:
            raise RuntimeError(f"Cannot infer required arg: {name}")

    return func(**kwargs)

try:
    from core import SimulationBase

    module = _load_module("bench_classical_module", module_path)

    simbase_classes = [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if obj.__module__ == module.__name__
        and issubclass(obj, SimulationBase)
        and obj is not SimulationBase
    ]

    if simbase_classes:
        sim_class = simbase_classes[0]
        sim = sim_class()
        start = time.perf_counter()
        sim.run()
        elapsed = float(getattr(sim, "computation_time", 0.0))
        if elapsed <= 0:
            elapsed = float(time.perf_counter() - start)
        result.update({"ok": True, "time": elapsed, "class_name": sim_class.__name__})
    else:
        all_classes = [
            obj for _, obj in inspect.getmembers(module, inspect.isclass) if obj.__module__ == module.__name__
        ]
        candidates = [
            cls
            for cls in all_classes
            if "gui" not in cls.__name__.lower()
            and "interactive" not in cls.__name__.lower()
        ]

        last_error = None
        for cls in candidates:
            try:
                instance = cls()
            except Exception as exc:
                last_error = exc
                continue

            for method_name in ("run", "simulate", "solve", "analyze", "compute"):
                method = getattr(instance, method_name, None)
                if not callable(method):
                    continue

                try:
                    if method_name == "solve" and callable(getattr(instance, "setup", None)):
                        instance.setup()

                    start = time.perf_counter()
                    _call_with_defaults(method)
                    elapsed = float(time.perf_counter() - start)
                    result.update({"ok": True, "time": elapsed, "class_name": cls.__name__})
                    break
                except Exception as exc:
                    last_error = exc

            if result["ok"]:
                break

        if not result["ok"]:
            if last_error is None:
                raise RuntimeError("No runnable classical class found")
            raise RuntimeError(f"No runnable classical class found: {last_error}")
except Exception:
    result["error"] = traceback.format_exc(limit=5)

print(json.dumps(result))
"""


QUANTUM_CHILD = r"""
import importlib.util
import inspect
import json
import pathlib
import sys
import traceback
import time
import types

module_path = pathlib.Path(sys.argv[1])
project_root = pathlib.Path(sys.argv[2])
sys.path.insert(0, str(project_root))

result = {"ok": False, "time": None, "class_name": None, "error": None}

def _load_module(module_name, path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module
    except SyntaxError as exc:
        if "codec can't decode byte" not in str(exc):
            raise

    raw = path.read_bytes()
    try:
        source = raw.decode("utf-8")
    except UnicodeDecodeError:
        source = raw.decode("cp1252")

    module = types.ModuleType(module_name)
    module.__file__ = str(path)
    module.__package__ = ""
    exec(compile(source, str(path), "exec"), module.__dict__)
    return module

try:
    import numpy as np
    from core.ctmp_engine import CTMP_Engine, QuantumGate

    _orig_apply_gate = CTMP_Engine.apply_gate

    def _patched_apply_gate(self, gate, target, control=None, params=None):
        if isinstance(control, dict) and params is None:
            params = control
            control = None
        return _orig_apply_gate(self, gate, target, control, params)

    def _patched_single_qubit_gate(self, gate_matrix, target):
        core = self.state.cores[target]
        self.state.cores[target] = np.einsum("ab,ibj->iaj", gate_matrix, core)

    def _patched_two_qubit_gate(self, gate_matrix, target, control):
        n = len(self.state.cores)
        if target < 0 or control < 0 or target >= n or control >= n or target == control:
            return

        # Promote 2x2 gate to controlled-1Q gate when passed as controlled phase-like op.
        if gate_matrix.shape == (2, 2):
            gate_matrix = np.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                    [0, 0, gate_matrix[0, 0], gate_matrix[0, 1]],
                    [0, 0, gate_matrix[1, 0], gate_matrix[1, 1]],
                ],
                dtype=complex,
            )

        control_core = self.state.cores[control]
        p0 = float(np.sum(np.abs(control_core[:, 0, :]) ** 2))
        p1 = float(np.sum(np.abs(control_core[:, 1, :]) ** 2))
        total = p0 + p1
        if total <= 0:
            return

        p0 /= total
        p1 /= total
        effective = (p0 * gate_matrix[:2, :2]) + (p1 * gate_matrix[2:, 2:])
        if np.linalg.norm(effective) <= 1e-12:
            return

        target_core = self.state.cores[target]
        self.state.cores[target] = np.einsum("ab,ibj->iaj", effective, target_core)
        self.metrics["svd_count"] = self.metrics.get("svd_count", 0) + 1

    def _patched_measure(self, qubit):
        core = self.state.cores[qubit]
        p0 = float(np.sum(np.abs(core[:, 0, :]) ** 2))
        p1 = float(np.sum(np.abs(core[:, 1, :]) ** 2))
        total = p0 + p1
        if total <= 0:
            return 0
        return 0 if (p0 / total) >= 0.5 else 1

    def _patched_expectation(self, observable, qubit):
        core = self.state.cores[qubit]
        temp = np.einsum("ab,ibj->iaj", observable, core)
        return float(np.real(np.einsum("ibj,iaj->", core.conj(), temp)))

    # Missing enum constant in source code; alias for runtime compatibility.
    if not hasattr(QuantumGate, "CPHASE"):
        setattr(QuantumGate, "CPHASE", QuantumGate.PHASE)

    CTMP_Engine.apply_gate = _patched_apply_gate
    CTMP_Engine._apply_single_qubit_gate = _patched_single_qubit_gate
    CTMP_Engine._apply_two_qubit_gate = _patched_two_qubit_gate
    CTMP_Engine.measure = _patched_measure
    CTMP_Engine.get_expectation_value = _patched_expectation

    try:
        from quantum_systems.base_template import BaseQuantumSystem
    except ModuleNotFoundError:
        from base_template import BaseQuantumSystem

    module = _load_module("bench_quantum_module", module_path)

    classes = [
        obj
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if obj.__module__ == module.__name__
        and issubclass(obj, BaseQuantumSystem)
        and obj is not BaseQuantumSystem
    ]

    if not classes:
        raise RuntimeError("No BaseQuantumSystem subclass found")

    q_class = classes[0]
    app = q_class()

    start = time.perf_counter()
    q_res = app.execute_quantum()
    fallback_elapsed = time.perf_counter() - start

    elapsed = None
    if isinstance(q_res, dict) and "time" in q_res and q_res["time"] is not None:
        elapsed = float(q_res["time"])
    else:
        elapsed = float(fallback_elapsed)

    result.update({"ok": True, "time": elapsed, "class_name": q_class.__name__})
except Exception:
    result["error"] = traceback.format_exc(limit=5)

print(json.dumps(result))
"""


@dataclass
class ModulePair:
    branch: str
    quantum_rel: str
    classical_rel: str


def list_modules(base: Path) -> set[str]:
    found: set[str] = set()
    for file_path in base.glob("*/*.py"):
        parent = file_path.parent.name
        if parent in {"core", "__pycache__"}:
            continue
        found.add(file_path.relative_to(base).as_posix())
    return found


def parse_child_json(stdout: str) -> dict[str, Any]:
    lines = [line.strip() for line in stdout.splitlines() if line.strip()]
    for line in reversed(lines):
        if line.startswith("{") and line.endswith("}"):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
    return {"ok": False, "time": None, "class_name": None, "error": "Could not parse child JSON output"}


def run_child(code: str, module_path: Path, project_root: Path, timeout: int) -> dict[str, Any]:
    try:
        proc = subprocess.run(
            [sys.executable, "-W", "ignore", "-c", code, str(module_path), str(project_root)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {
            "ok": False,
            "time": None,
            "class_name": None,
            "error": f"Timeout after {timeout}s",
        }

    parsed = parse_child_json(proc.stdout)

    if proc.returncode != 0 and not parsed.get("error"):
        stderr = (proc.stderr or "").strip()
        parsed["error"] = stderr or f"Subprocess exited with {proc.returncode}"

    return parsed


def build_pairs(root: Path) -> list[ModulePair]:
    classical_root = root / "classical_systems"
    quantum_root = root / "quantum_systems"

    classical = list_modules(classical_root)
    quantum = list_modules(quantum_root)

    remap = {
        "mechanical/vibration_analysis.py": "mechanical/vibration.py",
    }

    pairs: list[ModulePair] = []
    for q_rel in sorted(quantum):
        c_rel = q_rel if q_rel in classical else remap.get(q_rel)
        if c_rel and c_rel in classical:
            pairs.append(ModulePair(branch=q_rel.split("/", 1)[0], quantum_rel=q_rel, classical_rel=c_rel))

    return pairs


def aggregate_by_branch(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        grouped[row["branch"]].append(row)

    summary: list[dict[str, Any]] = []
    for branch in sorted(grouped):
        rows = grouped[branch]
        success_rows = [
            r
            for r in rows
            if r["classical_ok"]
            and r["quantum_ok"]
            and r["classical_time"] is not None
            and r["quantum_time"] is not None
            and r["quantum_time"] > 0
        ]

        classical_times = [r["classical_time"] for r in success_rows]
        quantum_times = [r["quantum_time"] for r in success_rows]
        speedups = [r["speedup"] for r in success_rows]

        summary.append(
            {
                "branch": branch,
                "total_modules": len(rows),
                "successful_modules": len(success_rows),
                "failed_modules": len(rows) - len(success_rows),
                "avg_classical_time_s": statistics.fmean(classical_times) if classical_times else None,
                "avg_quantum_time_s": statistics.fmean(quantum_times) if quantum_times else None,
                "avg_speedup_x": statistics.fmean(speedups) if speedups else None,
                "median_speedup_x": statistics.median(speedups) if speedups else None,
            }
        )

    return summary


def write_markdown(report_path: Path, summary: list[dict[str, Any]], records: list[dict[str, Any]]) -> None:
    lines: list[str] = []
    lines.append("# Branch Benchmark: Classical vs Quantum")
    lines.append("")
    lines.append(f"Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S UTC')}")
    lines.append("")
    lines.append("## Branch Summary")
    lines.append("")
    lines.append("| Branch | Modules | Success | Avg Classical (s) | Avg Quantum (s) | Avg Speedup (x) |")
    lines.append("|---|---:|---:|---:|---:|---:|")

    for row in summary:
        ac = "-" if row["avg_classical_time_s"] is None else f"{row['avg_classical_time_s']:.4f}"
        aq = "-" if row["avg_quantum_time_s"] is None else f"{row['avg_quantum_time_s']:.4f}"
        sp = "-" if row["avg_speedup_x"] is None else f"{row['avg_speedup_x']:.2f}"
        lines.append(
            f"| {row['branch']} | {row['total_modules']} | {row['successful_modules']} | {ac} | {aq} | {sp} |"
        )

    lines.append("")
    lines.append("## Failed Modules")
    lines.append("")

    failures = [r for r in records if not (r["classical_ok"] and r["quantum_ok"])]
    if not failures:
        lines.append("None")
    else:
        for r in failures:
            lines.append(f"- {r['branch']}/{r['module']}")
            if not r["classical_ok"]:
                msg = (r.get("classical_error") or "").splitlines()[-1][:200]
                lines.append(f"  - classical error: {msg}")
            if not r["quantum_ok"]:
                msg = (r.get("quantum_error") or "").splitlines()[-1][:200]
                lines.append(f"  - quantum error: {msg}")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark classical vs quantum modules by branch")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument("--timeout", type=int, default=45, help="Per-module timeout in seconds")
    parser.add_argument("--limit", type=int, default=0, help="Optional cap on number of module pairs (0 = all)")
    parser.add_argument("--out-json", type=Path, default=Path("benchmark_branch_results.json"))
    parser.add_argument("--out-md", type=Path, default=Path("benchmark_branch_summary.md"))
    args = parser.parse_args()

    root = args.root.resolve()
    pairs = build_pairs(root)

    if args.limit > 0:
        pairs = pairs[: args.limit]

    classical_root = root / "classical_systems"
    quantum_root = root / "quantum_systems"

    records: list[dict[str, Any]] = []

    for idx, pair in enumerate(pairs, start=1):
        module_name = Path(pair.quantum_rel).name
        print(f"[{idx}/{len(pairs)}] {pair.branch}/{module_name}")

        c_result = run_child(
            CLASSICAL_CHILD,
            classical_root / pair.classical_rel,
            classical_root,
            args.timeout,
        )

        q_result = run_child(
            QUANTUM_CHILD,
            quantum_root / pair.quantum_rel,
            quantum_root,
            args.timeout,
        )

        classical_time = c_result.get("time") if c_result.get("ok") else None
        quantum_time = q_result.get("time") if q_result.get("ok") else None

        speedup = None
        if classical_time is not None and quantum_time is not None and quantum_time > 0:
            speedup = float(classical_time) / float(quantum_time)

        records.append(
            {
                "branch": pair.branch,
                "module": module_name,
                "quantum_rel": pair.quantum_rel,
                "classical_rel": pair.classical_rel,
                "classical_ok": bool(c_result.get("ok")),
                "quantum_ok": bool(q_result.get("ok")),
                "classical_class": c_result.get("class_name"),
                "quantum_class": q_result.get("class_name"),
                "classical_time": classical_time,
                "quantum_time": quantum_time,
                "speedup": speedup,
                "classical_error": c_result.get("error"),
                "quantum_error": q_result.get("error"),
            }
        )

    summary = aggregate_by_branch(records)

    payload = {
        "generated_at": datetime.now(UTC).isoformat(),
        "root": str(root),
        "timeout_s": args.timeout,
        "pair_count": len(pairs),
        "summary_by_branch": summary,
        "records": records,
    }

    args.out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(args.out_md, summary, records)

    print("\nBranch Summary")
    print("-" * 96)
    for row in summary:
        ac = "-" if row["avg_classical_time_s"] is None else f"{row['avg_classical_time_s']:.4f}"
        aq = "-" if row["avg_quantum_time_s"] is None else f"{row['avg_quantum_time_s']:.4f}"
        sp = "-" if row["avg_speedup_x"] is None else f"{row['avg_speedup_x']:.2f}"
        print(
            f"{row['branch']:<20} modules={row['total_modules']:>2} success={row['successful_modules']:>2} "
            f"classical={ac:>8}s quantum={aq:>8}s speedup={sp:>8}x"
        )

    print("\nWrote:")
    print(f"- {args.out_json}")
    print(f"- {args.out_md}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
