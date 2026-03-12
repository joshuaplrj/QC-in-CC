"""Deterministic reference-data models for all simulation scenes."""
from __future__ import annotations

from dataclasses import dataclass
import math
import random


@dataclass(frozen=True)
class BaselineDataset:
    x: list[float]
    reference: list[float]
    x_label: str
    y_label: str
    unit: str


def _stable_scalar(key: str) -> float:
    value = 0
    for byte in key.encode("utf-8"):
        value = (value * 131 + byte) % 1_000_003
    return value / 1_000_003.0


def _series_range(values: list[float]) -> float:
    if not values:
        return 1.0
    return max(max(values) - min(values), 1e-9)


def build_reference_dataset(scene_kind: str, size: int, seed: int, system_key: str) -> BaselineDataset:
    points = max(24, min(int(size), 1024))
    x = [idx / max(1, points - 1) for idx in range(points)]
    phase = 2.0 * math.pi * _stable_scalar(system_key)
    gain = 0.85 + 0.35 * _stable_scalar(f"{system_key}:gain")
    jitter = random.Random(seed ^ 0xA5A5)

    y: list[float] = []
    x_label = "Normalized Position"
    y_label = "Response"
    unit = "arb"

    if scene_kind in {"fluid", "marine"}:
        x_label, y_label, unit = "Channel Length", "Pressure", "kPa"
        for t in x:
            boundary = 102.0 - 26.0 * t
            vortices = 5.5 * math.sin(8.0 * math.pi * t + phase)
            wake = -9.0 * math.exp(-((t - 0.58) ** 2) / 0.02)
            y.append(gain * (boundary + vortices + wake))
    elif scene_kind in {"network", "blockchain"}:
        x_label, y_label, unit = "Time", "Flow Load", "MW"
        for t in x:
            base = 62.0 + 14.0 * math.sin(2.0 * math.pi * t + phase)
            burst = 9.0 * math.sin(6.0 * math.pi * t + phase * 0.5)
            y.append(gain * (base + burst))
    elif scene_kind in {"structural", "lattice"}:
        x_label, y_label, unit = "Span Fraction", "Deflection", "mm"
        for t in x:
            shape = 24.0 * t * (1.0 - t)
            modal = 2.1 * math.sin(5.0 * math.pi * t + phase)
            y.append(gain * (shape + modal))
    elif scene_kind in {"wave", "antenna"}:
        x_label, y_label, unit = "Angle", "Amplitude", "dB"
        for t in x:
            angle = (t * 2.0 - 1.0) * math.pi
            main = 17.0 * math.cos(angle + phase) ** 2
            side = 4.5 * math.cos(3.0 * angle - phase)
            y.append(gain * (main + side))
    elif scene_kind in {"energy", "process", "reactor"}:
        x_label, y_label, unit = "Time", "State Variable", "unit"
        for t in x:
            ramp = 35.0 + 48.0 * (1.0 - math.exp(-3.0 * t))
            ripple = 3.0 * math.sin(7.0 * math.pi * t + phase)
            y.append(gain * (ramp + ripple))
    elif scene_kind in {"orbit", "aerospace"}:
        x_label, y_label, unit = "Orbit Angle", "Radius", "km"
        for t in x:
            theta = 2.0 * math.pi * t
            r = 6800.0 + 260.0 * math.cos(theta + phase)
            perturb = 22.0 * math.sin(3.0 * theta - phase * 0.4)
            y.append(gain * (r + perturb))
    elif scene_kind in {"scanner", "pharma"}:
        x_label, y_label, unit = "Time", "Concentration", "mg/L"
        for t in x:
            uptake = 52.0 * (1.0 - math.exp(-4.8 * t))
            elimination = 38.0 * math.exp(-2.4 * t)
            y.append(gain * (uptake + elimination))
    elif scene_kind in {"dna", "algorithm", "crypto"}:
        x_label, y_label, unit = "Index", "Score", "a.u."
        for t in x:
            envelope = 0.7 + 0.3 * math.sin(2.0 * math.pi * t + phase)
            signal = 68.0 + 11.0 * math.sin(10.0 * math.pi * t + phase)
            y.append(gain * envelope * signal)
    elif scene_kind in {"agriculture", "windfarm"}:
        x_label, y_label, unit = "Time", "Yield", "%"
        for t in x:
            growth = 18.0 + 74.0 / (1.0 + math.exp(-8.0 * (t - 0.42)))
            climate = 4.0 * math.sin(6.0 * math.pi * t + phase)
            y.append(gain * (growth + climate))
    elif scene_kind in {"chip", "circuit"}:
        x_label, y_label, unit = "Node", "Signal Integrity", "%"
        for t in x:
            baseline = 91.0 - 14.0 * t
            ringing = 3.3 * math.sin(12.0 * math.pi * t + phase)
            y.append(gain * (baseline + ringing))
    else:
        x_label, y_label, unit = "Time", "System Response", "arb"
        for t in x:
            base = 55.0 + 16.0 * math.sin(4.0 * math.pi * t + phase)
            trend = 8.0 * t
            y.append(gain * (base + trend))

    for idx in range(len(y)):
        y[idx] += jitter.uniform(-0.18, 0.18)

    return BaselineDataset(x=x, reference=y, x_label=x_label, y_label=y_label, unit=unit)


def predict_from_reference(reference: list[float], quality: float, seed: int, style: str) -> list[float]:
    quality = max(0.0, min(1.0, quality))
    rng = random.Random(seed)
    values = list(reference)
    span = _series_range(values)
    sigma = (1.0 - quality) * span * 0.08
    drift_weight = (1.0 - quality) * 0.09
    phase = rng.random() * 2.0 * math.pi
    freq = 1.2 + rng.random() * 2.5

    out: list[float] = []
    count = len(values)
    for idx, value in enumerate(values):
        t = idx / max(1, count - 1)
        drift = drift_weight * math.sin((freq * 2.0 * math.pi * t) + phase)
        noise = rng.gauss(0.0, sigma)
        out.append(value * (1.0 + drift) + noise)

    return out


def fit_metrics(reference: list[float], estimate: list[float]) -> dict[str, float]:
    if not reference or not estimate:
        return {
            "rmse": 0.0,
            "mae": 0.0,
            "mape": 0.0,
            "r2": 1.0,
            "max_error": 0.0,
            "confidence": 1.0,
        }

    n = min(len(reference), len(estimate))
    ref = reference[:n]
    est = estimate[:n]

    residuals = [e - r for r, e in zip(ref, est)]
    abs_res = [abs(r) for r in residuals]
    mse = sum(r * r for r in residuals) / n
    rmse = math.sqrt(mse)
    mae = sum(abs_res) / n

    mean_ref = sum(ref) / n
    ss_tot = sum((r - mean_ref) ** 2 for r in ref)
    ss_res = sum(r * r for r in residuals)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 1e-12 else 1.0

    denominator = max(sum(abs(r) for r in ref) / n, 1e-9)
    mape = (sum(abs(r) / max(abs(v), denominator * 0.2) for r, v in zip(residuals, ref)) / n) * 100.0

    span = _series_range(ref)
    confidence = max(0.0, 1.0 - (rmse / max(span, 1e-9)))

    return {
        "rmse": float(rmse),
        "mae": float(mae),
        "mape": float(mape),
        "r2": float(r2),
        "max_error": float(max(abs_res) if abs_res else 0.0),
        "confidence": float(confidence),
    }
