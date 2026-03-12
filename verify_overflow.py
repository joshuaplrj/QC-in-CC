import sys
from quantum_systems.electrical.signal_processor import SignalProcessor

def verify():
    app = SignalProcessor()
    app.n_qubits = 16
    
    print("Executing Classical...")
    c_res = app.execute_classical()
    print(f"Classical Time: {c_res['time']}s, Memory: {c_res['classical_memory_bytes']} bytes")
    
    print("Executing Quantum...")
    q_res = app.execute_quantum()
    print(f"Quantum Time: {q_res['time']}s, Compression: {q_res['memory_compression']}x")
    assert 'memory_compression' in q_res

    # Test extreme scale that previously overflowed float comparison
    app.n_qubits = 2000
    print("Executing Extreme Scale...")
    q_res_bound = app.execute_quantum()
    print(f"Extreme Compression Ratio: {q_res_bound['memory_compression']}")
    print("Success!")

if __name__ == "__main__":
    verify()
