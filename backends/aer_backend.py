"""
Local Ideal & Noisy Simulation Backends using Qiskit.
"""
from qiskit.quantum_info import Statevector

class AerSimulatorBackend:
    def __init__(self, noisy=False):
        self.noisy = noisy
        
    def run(self, qc, shots=1024):
        sv = Statevector.from_instruction(qc.remove_final_measurements(inplace=False))
        probs = sv.probabilities()
        if not self.noisy:
            counts = {np.binary_repr(i, qc.num_qubits): int(p * shots) for i, p in enumerate(probs) if p > 1e-6}
        else:
            p_noisy = 0.98 * probs + 0.02 * (1.0 / len(probs))
            counts_arr = np.random.multinomial(shots, p_noisy)
            counts = {np.binary_repr(i, qc.num_qubits): int(c) for i, c in enumerate(counts_arr) if c > 0}
        return counts
