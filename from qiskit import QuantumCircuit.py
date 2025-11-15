from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

qc = QuantumCircuit(1, 1)
qc.h(0)
qc.z(0)
qc.measure(0, 0)

simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
counts = job.result().get_counts(qc)

print("Measurement results after Z gate phase flip:", counts)
plt.bar(counts.keys(), counts.values())
plt.xlabel('Measurement Outcome')
plt.ylabel('Counts')
plt.title('Phase Flip with Z Gate')
plt.show()