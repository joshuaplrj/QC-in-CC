# Classical Systems Rebuild Report

## Scope

Full reset of the `classical_systems` implementation to remove instability from mixed legacy module patterns.

## Completed Work

- Replaced `classical_systems/core/__init__.py` with a compact, deterministic runtime core.
- Regenerated every simulation module under `classical_systems/*/*.py` (excluding `core`) from a single template.
- Preserved launcher module path compatibility by keeping all existing file names.
- Standardized each module to:
  - expose one simulation class,
  - inherit from the shared core runtime,
  - provide a `main()` entrypoint,
  - run deterministically with bounded runtime.

## Rebuild Output

- Modules regenerated: `79`
- Disciplines covered: `14`
- Core API standardized: `SimulationConfig`, `SimulationBase`, `InteractiveGUI`

## Verification

- Classical module smoke validation: `79/79` successful loads and runs.

## Current Limitation Outside Classical Scope

`branch_benchmark.py` currently reports quantum-side class discovery failures (`No BaseQuantumSystem subclass found`) due import identity mismatch in the benchmark harness. This is independent of the classical rebuild and should be addressed in the benchmark/quantum loading logic if cross-branch benchmarking is required.
