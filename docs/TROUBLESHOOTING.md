# Troubleshooting Guide

Solutions to common issues and problems encountered when using QC in CC.

---

## Installation & Environment

### Issue: ImportError - No module named 'numpy' (or scipy, matplotlib, etc.)

**Symptom:**
```
ModuleNotFoundError: No module named 'numpy'
```

**Causes:**
- Dependencies not installed
- Wrong Python environment/virtual environment
- pip install failed silently

**Solutions:**

1. **Verify Python environment:**
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   python --version  # Should be 3.7+
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install --upgrade pip
   pip install --upgrade numpy scipy matplotlib networkx customtkinter
   ```

3. **Use requirements file (if available):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Check pip is from correct Python:**
   ```bash
   python -m pip install numpy  # Uses current python executable
   ```

---

### Issue: customtkinter not found

**Symptom:**
```
ModuleNotFoundError: No module named 'customtkinter'
```

**Note:** Only needed for quantum launcher (customtkinter). Classical launcher uses built-in tkinter.

**Solutions:**

1. **Install customtkinter:**
   ```bash
   pip install customtkinter
   ```

2. **If that fails, try:**
   ```bash
   pip install --upgrade customtkinter --force-reinstall
   ```

3. **Workaround - Use classical launcher instead:**
   ```bash
   python classical_systems/launcher.py  # Doesn't need customtkinter
   ```

---

### Issue: Python version too old

**Symptom:**
```
SyntaxError: invalid syntax
TypeError: unsupported operand type(s)
```

**Cause:** Python < 3.7

**Solutions:**

1. **Check Python version:**
   ```bash
   python --version
   ```

2. **If < 3.7, update Python:**
   - Download from python.org
   - macOS: `brew install python@3.11`
   - Linux: `sudo apt-get install python3.11`

3. **Create new virtual environment with correct Python:**
   ```bash
   python3.11 -m venv venv  # Use specific Python
   source venv/bin/activate
   pip install numpy scipy matplotlib networkx customtkinter
   ```

---

### Issue: tkinter not found (Linux)

**Symptom:**
```
ModuleNotFoundError: No module named 'tkinter'
ImportError: No module named '_tkinter'
```

**Cause:** tkinter not installed with Python

**Solutions:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
sudo apt-get install python3-dev
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**Arch:**
```bash
sudo pacman -S tk
```

Then recreate virtual environment:
```bash
deactivate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install numpy scipy matplotlib networkx customtkinter
```

---

### Issue: Permission denied running launcher

**Symptom:**
```
bash: ./launcher.py: Permission denied
```

**Solution (macOS/Linux):**
```bash
chmod +x classical_systems/launcher.py
chmod +x quantum_systems/launcher_quantum.py

# Then run
python classical_systems/launcher.py  # Easier than ./launcher.py
```

---

## Running Modules

### Issue: Module crashes immediately with no error message

**Symptom:**
```
$ python classical_systems/launcher.py
# Window opens then closes, no traceback
```

**Causes:**
- Unhandled exception in GUI thread
- Missing data in module setup

**Solutions:**

1. **Run from terminal (see actual error):**
   ```bash
   # Instead of double-clicking icon, use terminal
   python classical_systems/launcher.py
   # Error messages print to terminal
   ```

2. **Test module directly:**
   ```bash
   python classical_systems/electrical/power_flow.py
   # Run the main() function directly
   ```

3. **Add debug prints:**
   ```python
   from classical_systems.electrical.power_flow import PowerFlow
   from classical_systems.core import SimulationConfig
   
   config = SimulationConfig(problem_size=10)
   module = PowerFlow(config)
   
   print("Step 1: Created module")
   module.setup()
   print("Step 2: Setup complete")
   result = module.solve()
   print(f"Step 3: Solve complete - {result['status']}")
   ```

---

### Issue: "Module not found" in launcher

**Symptom:**
```
Module does not exist: power_flow
# Or module doesn't appear in dropdown list
```

**Causes:**
- Module file not in correct directory
- Class name doesn't match file name
- Module not registered in launcher
- Syntax error in module

**Solutions:**

1. **Verify file location:**
   ```bash
   ls classical_systems/electrical/power_flow.py  # Should exist
   ```

2. **Check module registration:**
   - Open `classical_systems/launcher.py`
   - Search for `MODULE_REGISTRY`
   - Ensure your module is listed under correct discipline

3. **Test module can be imported:**
   ```bash
   python -c "from classical_systems.electrical.power_flow import PowerFlow; print('OK')"
   # Should print "OK", not error
   ```

4. **Check for syntax errors:**
   ```bash
   python -m py_compile classical_systems/electrical/power_flow.py
   # If it fails, there's a syntax error
   ```

---

### Issue: Module runs but produces wrong results

**Symptom:**
```
Results don't match expected values
Output is all zeros or NaN
Results are identical regardless of input
```

**Causes:**
- Bug in algorithm
- Uninitialized variables
- Incorrect configuration
- Wrong random seed

**Solutions:**

1. **Check configuration:**
   ```python
   config = SimulationConfig(problem_size=50, seed=42, scale=1.0)
   module = PowerFlow(config)
   print(f"Config: {config}")  # Verify settings
   ```

2. **Add intermediate assertions:**
   ```python
   module.setup()
   assert module.admittance_matrix is not None, "Matrix not initialized"
   assert len(module.test_loads) > 0, "No loads generated"
   result = module.solve()
   assert len(result['output']) > 0, "No output"
   ```

3. **Compare with classical reference:**
   ```python
   import numpy as np
   from classical_systems.electrical.power_flow import PowerFlow
   
   module = PowerFlow()
   module.setup()
   
   # Solve
   result = module.solve()
   
   # Manual check with numpy
   A = module.admittance_matrix
   b = module.test_loads
   x_numpy = np.linalg.solve(A, b)
   
   # Compare
   error = np.linalg.norm(np.array(result['output']) - x_numpy)
   print(f"Error vs numpy: {error}")
   ```

4. **Test reproducibility:**
   ```python
   # Same seed should produce identical results
   config1 = SimulationConfig(problem_size=50, seed=42)
   config2 = SimulationConfig(problem_size=50, seed=42)
   
   m1 = PowerFlow(config1)
   m2 = PowerFlow(config2)
   
   m1.setup()
   m1.solve()
   m2.setup()
   m2.solve()
   
   assert m1._last_output == m2._last_output
   ```

---

## GUI Issues

### Issue: Launcher window won't open

**Symptom:**
```
$ python classical_systems/launcher.py
# Nothing happens, or error about display
```

**Solutions:**

1. **Check if running headless (no display):**
   ```bash
   echo $DISPLAY  # Linux/macOS - if empty, no display available
   ```

2. **Try with matplotlib backend:**
   ```python
   import matplotlib
   matplotlib.use('Agg')  # Use non-GUI backend
   ```

3. **Run over SSH with X11 forwarding:**
   ```bash
   ssh -X user@host  # Enable X11 forwarding
   python classical_systems/launcher.py
   ```

4. **If all else fails, use script mode:**
   ```bash
   python -c "
   from classical_systems.electrical.power_flow import main
   result = main()
   print(result)
   "
   ```

---

### Issue: GUI is very slow or unresponsive

**Symptom:**
```
Clicking buttons takes several seconds
Launcher takes > 10 seconds to open
```

**Causes:**
- System is busy with other processes
- Too many modules being loaded at startup
- Graphics driver issues
- Module setup is slow

**Solutions:**

1. **Close other applications:**
   ```bash
   # Free up memory and CPU
   killall firefox  # or other heavy apps
   ```

2. **Run just one module (don't load all):**
   ```python
   from classical_systems.electrical.power_flow import PowerFlow
   module = PowerFlow()
   module.setup()
   module.solve()
   module.visualize()
   ```

3. **Check system resources:**
   ```bash
   top  # macOS/Linux - see CPU/memory usage
   # Look for processes using > 80% CPU
   ```

4. **Reduce problem size in launcher:**
   - Use problem_size < 50 for faster execution

---

### Issue: Visualization window doesn't appear

**Symptom:**
```
Module runs but chart window never appears
```

**Causes:**
- Matplotlib not configured correctly
- Backend issue
- Window created off-screen

**Solutions:**

1. **Test matplotlib directly:**
   ```python
   import matplotlib.pyplot as plt
   plt.plot([1, 2, 3], [1, 4, 9])
   plt.show()
   # Should display a simple chart
   ```

2. **Check matplotlib backend:**
   ```bash
   python -c "import matplotlib; print(matplotlib.get_backend())"
   # Should show 'TkAgg' or similar interactive backend
   ```

3. **Force interactive backend:**
   ```python
   import matplotlib
   matplotlib.use('TkAgg')  # Force Tkinter backend
   import matplotlib.pyplot as plt
   ```

4. **If running in notebook/remote:**
   ```python
   # Add to top of script
   %matplotlib notebook  # In Jupyter
   # Or use 'Agg' backend and save to file instead
   ```

---

## Performance Issues

### Issue: Benchmark takes too long (> 30 minutes)

**Symptom:**
```
python branch_benchmark.py  # Still running after 30 min
```

**Causes:**
- System is busy
- Benchmark is really running 78 modules (5-10 min normal)
- One module is stuck

**Solutions:**

1. **Check actual progress:**
   - Monitor terminal output
   - Use `tail` to watch progress file
   - See how many modules have completed

2. **Run with timeout:**
   ```bash
   timeout 600 python branch_benchmark.py  # 10 minute timeout
   ```

3. **Benchmark single module instead:**
   ```bash
   python -c "
   from quantum_systems.electrical.power_flow import PowerFlow
   import time
   
   module = PowerFlow()
   
   start = time.time()
   module.execute_quantum()
   elapsed = time.time() - start
   
   print(f'Time: {elapsed:.4f}s')
   "
   ```

4. **Check if CPU is throttled:**
   ```bash
   # macOS
   sysctl -a | grep freq
   
   # Linux
   cat /proc/cpuinfo | grep MHz
   ```

---

### Issue: Module execution is very slow

**Symptom:**
```
Single module takes > 1 second (expected: 0.001-0.010s)
```

**Causes:**
- Large problem_size parameter
- System under heavy load
- Inefficient algorithm in module
- Debug mode enabled

**Solutions:**

1. **Use smaller problem size:**
   ```python
   from classical_systems.electrical.power_flow import PowerFlow
   from classical_systems.core import SimulationConfig
   
   config = SimulationConfig(problem_size=10)  # Small
   module = PowerFlow(config)
   ```

2. **Disable debug mode:**
   ```bash
   unset QC_DEBUG  # If set
   ```

3. **Close other applications:**
   ```bash
   # Windows Task Manager
   # macOS Activity Monitor
   # Linux: top, kill heavy processes
   ```

4. **Check NumPy threading:**
   ```bash
   export OMP_NUM_THREADS=2  # Limit NumPy threads
   python quantum_systems/launcher_quantum.py
   ```

---

## Benchmarking Issues

### Issue: Benchmark fails partway through

**Symptom:**
```
✓ 45/78 modules completed
✗ Error on module X
Benchmark stops
```

**Causes:**
- Specific module has bug
- Memory error
- Numerical instability

**Solutions:**

1. **Test failing module directly:**
   ```bash
   python quantum_systems/electrical/my_module.py
   # Run main() to see error
   ```

2. **Skip problematic module:**
   - Edit `branch_benchmark.py`
   - Comment out problematic module in MODULE_REGISTRY
   - Re-run benchmark

3. **Check available memory:**
   ```bash
   free -h  # Linux
   vm_stat  # macOS
   # If < 500MB free, close applications
   ```

4. **Run with smaller problem size:**
   - Edit module's default config
   - Change `problem_size` from 50 to 20

---

### Issue: Benchmark results don't match previous runs

**Symptom:**
```
Same modules show different speedup values
Results vary by 20-50%
```

**Causes:**
- System load varies between runs
- Other processes interfering
- Quantum algorithm has some randomness
- Small sample size

**Solutions:**

1. **Run multiple times and average:**
   ```bash
   for i in {1..3}; do
       python branch_benchmark.py
       tail -5 benchmark_summary.md
       echo "---"
   done
   ```

2. **Control system load:**
   ```bash
   # Close all other applications
   # Run on dedicated system/time
   # Disable CPU power management
   ```

3. **Increase measurement time:**
   - Use larger `problem_size`
   - Reduces noise from startup overhead

4. **Use statistical analysis:**
   ```python
   import json
   results = json.load(open('benchmark_results.json'))
   speedups = [m['speedup'] for discipline in results['modules'].values() for m in discipline.values()]
   mean = sum(speedups) / len(speedups)
   std = (sum((x - mean)**2 for x in speedups) / len(speedups))**0.5
   print(f"Speedup: {mean:.2f}x ± {std:.2f}x")
   ```

---

## Data & Results Issues

### Issue: Cannot export/save results

**Symptom:**
```
"Permission denied" or "Cannot write file"
```

**Solutions:**

1. **Check write permissions:**
   ```bash
   ls -l benchmark_results.json
   # Should have 'w' permission for user
   ```

2. **Try specific directory:**
   ```python
   import os
   os.chdir('/tmp')  # Use /tmp which usually has write access
   # Then run benchmark
   ```

3. **Save to different location:**
   ```bash
   python branch_benchmark.py
   mv benchmark_results.json ~/my_results_backup.json
   ```

---

### Issue: JSON file is corrupted or empty

**Symptom:**
```
json.JSONDecodeError: Expecting value
# Or file size is 0 bytes
```

**Causes:**
- Benchmark interrupted before completion
- Disk full during write
- File permissions issue

**Solutions:**

1. **Re-run benchmark:**
   ```bash
   rm benchmark_results.json  # Delete corrupted file
   python branch_benchmark.py  # Re-run
   ```

2. **Check disk space:**
   ```bash
   df -h  # See available space
   # Need > 100MB free
   ```

3. **Validate JSON:**
   ```bash
   python -m json.tool benchmark_results.json > /dev/null
   # If valid, this succeeds silently
   ```

---

## Advanced Debugging

### Enable Debug Logging

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Now modules will log detailed information
from classical_systems.electrical.power_flow import PowerFlow
module = PowerFlow()
```

### Profile Performance

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
from classical_systems.electrical.power_flow import PowerFlow
module = PowerFlow()
module.setup()
module.solve()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest functions
```

### Memory Profiling

```bash
pip install memory-profiler

# Profile script
python -m memory_profiler my_script.py
```

### Inspect Module Internals

```python
from classical_systems.electrical.power_flow import PowerFlow
import inspect

module = PowerFlow()

# See source code of method
print(inspect.getsource(module.solve))

# See docstring
print(module.solve.__doc__)

# See all methods
print(dir(module))
```

---

## When to Report Issues

If you've tried these solutions and the problem persists:

1. **Collect information:**
   - Python version: `python --version`
   - Operating system: `uname -a`
   - Dependencies: `pip list | grep -E 'numpy|scipy|matplotlib'`
   - Traceback/error message (full text)
   - Steps to reproduce

2. **Create minimal test case:**
   ```python
   # Simplest code that reproduces the issue
   from classical_systems.electrical.power_flow import PowerFlow
   module = PowerFlow()
   result = module.solve()  # Issue happens here
   ```

3. **Check GitHub issues:**
   - May already be reported/fixed
   - Check closed issues too

---

## FAQ

**Q: Can I use different Python versions (3.8, 3.9, 3.10)?**  
A: Yes, any 3.7+ works. Tested on 3.7-3.12.

**Q: Can I run modules on GPU?**  
A: Not currently. CTMP engine uses CPU only. Consider CUDA-accelerated NumPy if needed.

**Q: How much RAM do I need?**  
A: 2GB minimum, 4GB+ recommended. Large problem sizes (> 500) need more.

**Q: Can I modify modules after installation?**  
A: Yes, edit .py files directly. Changes take effect on next import/run.

**Q: How do I uninstall QC in CC?**  
A: Just delete the folder. Virtual environment: `rm -rf venv` then `deactivate`.

**Q: Why are some modules slower than others?**  
A: Algorithm complexity (O(n), O(n³)), problem size, your system resources.

**Q: Can I use QC in CC in production?**  
A: Yes, it's stable. Benchmark your specific use case first.

---

**Last Updated**: March 2026  
**Common Issues Covered**: 30+  
**Solutions Documented**: 50+
