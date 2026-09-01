"""
Safe IBM Quantum Connection Diagnostic.
"""
import sys

def check_connection():
    print("--- IBM Quantum Connection Diagnostic ---")
    try:
        from qiskit_ibm_runtime import QiskitRuntimeService
        service = QiskitRuntimeService()
        backends = service.backends()
        print("IBM connection: YES")
        print("Account: configured")
        print(f"Available backends: {[b.name for b in backends]}")
        return True
    except Exception as e:
        print("IBM connection: NO")
        print("Account: not configured / credentials absent")
        print(f"Detail: {str(e)}")
        return False

if __name__ == "__main__":
    check_connection()
