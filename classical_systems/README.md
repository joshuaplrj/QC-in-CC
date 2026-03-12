# Classical Systems (Rebuilt Baseline)

This directory was rebuilt from scratch to provide a stable, deterministic classical baseline across all simulation modules.

## What Was Rebuilt

- `core/__init__.py` now provides a lightweight, consistent runtime contract:
  - `SimulationConfig`
  - `SimulationBase`
  - `InteractiveGUI` compatibility shim
- All domain modules under `classical_systems/*/*.py` were regenerated to one template contract.
- Every module now exposes:
  - exactly one runnable simulation class
  - a `main()` entrypoint
  - deterministic outputs (seeded)

## Module Coverage

The rebuild includes all existing discipline folders in this repository:

- `aerospace`
- `agricultural`
- `biomedical`
- `chemical`
- `civil`
- `computer_science`
- `electrical`
- `environmental`
- `industrial`
- `marine`
- `materials_science`
- `mechanical`
- `nuclear`
- `petroleum`

Total regenerated modules: `79`.

## Usage

### Run launcher

```bash
python classical_systems/launcher.py
```

### Run a module directly

```bash
python classical_systems/electrical/power_flow.py
```

### Import and run in code

```python
from classical_systems.electrical.power_flow import main
result = main()
print(result)
```

## Verification

Classical-side validation command used during rebuild:

```bash
python -c "import importlib.util,inspect,sys,pathlib;root=pathlib.Path(r'C:\Users\John Jacob\Desktop\QB in CC\classical_systems');sys.path.insert(0,str(root));from core import SimulationBase;ok=0;fails=[]
for p in sorted(root.glob('*/*.py')):
    if p.parent.name in {'core','__pycache__'}: continue
    s=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
    cls=[c for _,c in inspect.getmembers(m,inspect.isclass) if c.__module__==m.__name__ and issubclass(c,SimulationBase) and c is not SimulationBase]
    (cls[0]().run(),None) if cls else fails.append(str(p.relative_to(root)))
    ok += 1 if cls else 0
print({'success':ok,'failures':len(fails)})"
```

Expected result after this rebuild: all modules succeed.
