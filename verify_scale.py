"""Test at large n to verify timing is now reasonable."""
import sys, time
sys.path.insert(0, ".")
from quantum_systems.computer_science.cryptography import Cryptography

for n_val in [12, 100, 500, 999]:
    app = Cryptography()
    app.n_qubits = n_val

    t0 = time.perf_counter()
    c = app.execute_classical()
    ct = time.perf_counter() - t0

    t0 = time.perf_counter()
    q = app.execute_quantum()
    qt = time.perf_counter() - t0

    print(f"n={n_val:>4}  Classical: {ct:.4f}s RMSE={c['rmse']:.4f}  "
          f"Quantum: {qt:.4f}s RMSE={q['rmse']:.4f}  "
          f"Compression={q['memory_compression']:.1f}x  "
          f"Q better? {'YES' if q['rmse'] < c['rmse'] else 'NO'}")
