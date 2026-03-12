# Quantum Systems (Rebuilt Baseline)

This directory has been rebuilt from scratch to provide a stable and consistent quantum simulation baseline.

## What Was Rebuilt

- `base_template.py` standardized as the common runtime contract.
- `core/` replaced with lightweight, deterministic compatibility implementations:
  - `ctmp_engine.py`
  - `quantum_algorithms.py`
  - `comparison_engine.py`
  - `memristor_emulator.py`
  - `circuit_visualizer.py`
  - `neural_network_mode.py`
- All discipline modules under `quantum_systems/*/*.py` regenerated to a single template pattern.

## Runtime Guarantees

Each quantum module now provides:

- one deterministic `BaseQuantumSystem` subclass
- `execute_classical()` and `execute_quantum()`
- a `main()` GUI entrypoint compatible with `launcher_quantum.py`
- built-in reference baselines (no external datasets required)
- data-fidelity outputs (`rmse`, `mape`, `r2`, confidence) for both classical and quantum runs
- live simulation visuals tailored to each system domain with runtime + fidelity charts

## Verification

Completed after rebuild:

- Quantum module import + execute check: `78/78` pass
- Core test suite: `6/6` pass (`python -m pytest quantum_systems/core/tests/test_core.py -q`)
- Cross-branch benchmark: all paired modules successful (`78/78`)

## Usage

```bash
python quantum_systems/launcher_quantum.py
```

```bash
python quantum_systems/aerospace/aircraft_weight.py
```
