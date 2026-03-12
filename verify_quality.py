"""Verify that CTMP quantum path now outperforms classical on quality."""
import sys
sys.path.insert(0, ".")
from quantum_systems.computer_science.cryptography import Cryptography

app = Cryptography()
app.n_qubits = 12  # reasonable scale

c = app.execute_classical()
q = app.execute_quantum()

print("=" * 60)
print("CRYPTOGRAPHY MODULE COMPARISON (n=12)")
print("=" * 60)
print(f"Classical  RMSE: {c['rmse']:.6f}  R²: {c['r2']:.6f}  Time: {c['time']:.6f}s")
print(f"Quantum    RMSE: {q['rmse']:.6f}  R²: {q['r2']:.6f}  Time: {q['time']:.6f}s")
print(f"Compression: {q['memory_compression']:.0f}×")
print()
rmse_improvement = ((c['rmse'] - q['rmse']) / max(c['rmse'], 1e-9)) * 100
r2_improvement = q['r2'] - c['r2']
print(f"RMSE improvement: {rmse_improvement:+.1f}%")
print(f"R² improvement:   {r2_improvement:+.6f}")
print(f"Quantum better?   {'YES ✓' if q['rmse'] < c['rmse'] else 'NO ✗'}")
