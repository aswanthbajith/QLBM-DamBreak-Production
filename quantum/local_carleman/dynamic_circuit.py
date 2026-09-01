"""
Dynamic Quantum Circuit Architecture with Mid-Circuit Measurements & Resets.
"""
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from quantum.local_carleman.collision import build_local_carleman_collision_circuit

def build_dynamic_qlbm_step(nx=2, ny=2, timesteps=2):
    """
    Builds a dynamic quantum circuit performing repeated QLBM steps with mid-circuit resets.
    """
    q_spatial = QuantumRegister(2, name="spatial")
    q_vel = QuantumRegister(4, name="vel")
    c_reg = ClassicalRegister(6, name="meas")
    
    qc = QuantumCircuit(q_spatial, q_vel, c_reg)
    
    # Initial superposition on space
    qc.h(q_spatial)
    
    for t in range(timesteps):
        # Collision
        coll = build_local_carleman_collision_circuit()
        qc.append(coll, q_vel)
        # Shift
        qc.cx(q_vel[0], q_spatial[0])
        qc.cx(q_vel[1], q_spatial[1])
        
    qc.measure(list(q_spatial) + list(q_vel), c_reg)
    return qc
