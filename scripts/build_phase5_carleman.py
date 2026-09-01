import os

repo_dir = "/home/aswa/Research/QLBM-DamBreak"
carleman_dir = os.path.join(repo_dir, "carleman")
os.makedirs(carleman_dir, exist_ok=True)

# 1. carleman/linearize.py
with open(os.path.join(carleman_dir, "linearize.py"), "w") as f:
    f.write("""\"\"\"
Carleman Linearization Transformation & Lifting Functions.
\"\"\"
import numpy as np

def lift_state(x, order=2):
    \"\"\"
    Lifts a state vector x into its Carleman representation up to given polynomial order.
    For order=1: returns x
    For order=2: returns [x, x (x) x]
    \"\"\"
    x = np.asarray(x, dtype=np.float64).flatten()
    if order == 1:
        return x
    elif order == 2:
        x_kron_x = np.kron(x, x)
        return np.concatenate((x, x_kron_x))
    else:
        terms = [x]
        curr = x
        for _ in range(2, order + 1):
            curr = np.kron(curr, x)
            terms.append(curr)
        return np.concatenate(terms)

def project_state(y, n_dim):
    \"\"\"
    Extracts the original linear physical state from a Carleman lifted state y.
    \"\"\"
    return y[:n_dim]
""")

# 2. carleman/operator.py
with open(os.path.join(carleman_dir, "operator.py"), "w") as f:
    f.write("""\"\"\"
Explicit Construction of Carleman Linear Operators.
\"\"\"
import numpy as np
import scipy.sparse as sp

def construct_carleman_matrix_2nd_order(A1, A2, n_dim):
    \"\"\"
    Constructs the block Carleman matrix A_C for dx/dt = A1 x + A2 (x (x) x):
    A_C = [ A1       A2      ]
          [ 0   A1(x)I + I(x)A1 ]
    Dimension: n_dim + n_dim^2
    \"\"\"
    I = np.eye(n_dim)
    A22 = np.kron(A1, I) + np.kron(I, A1)
    
    row1 = np.hstack((A1, A2))
    row2 = np.hstack((np.zeros((n_dim**2, n_dim)), A22))
    A_C = np.vstack((row1, row2))
    return A_C

def construct_discrete_carleman_step(F1, F2, n_dim):
    \"\"\"
    Constructs the discrete Carleman step matrix M_C for x_{t+1} = F1 x_t + F2 (x_t (x) x_t):
    x_{t+1} = F1 x_t + F2 (x_t (x) x_t)
    (x_{t+1} (x) x_{t+1}) = (F1 (x) F1) (x_t (x) x_t) + O(x^3)
    
    M_C = [ F1      F2     ]
          [ 0    F1 (x) F1 ]
    \"\"\"
    M22 = np.kron(F1, F1)
    row1 = np.hstack((F1, F2))
    row2 = np.hstack((np.zeros((n_dim**2, n_dim)), M22))
    M_C = np.vstack((row1, row2))
    return M_C
""")

# 3. carleman/truncation.py
with open(os.path.join(carleman_dir, "truncation.py"), "w") as f:
    f.write("""\"\"\"
Carleman Truncation Error Bounds, Sparsity & Normalization.
\"\"\"
import numpy as np
import scipy.linalg as la

class CarlemanTruncator:
    def __init__(self, n_dim, order=2):
        self.n_dim = n_dim
        self.order = order
        if order == 1:
            self.dim_C = n_dim
        elif order == 2:
            self.dim_C = n_dim + n_dim**2
        else:
            self.dim_C = sum(n_dim**k for k in range(1, order + 1))
            
    def required_qubits(self):
        \"\"\"
        Number of qubits needed to represent the Carleman state: ceil(log2(D_C)).
        \"\"\"
        return int(np.ceil(np.log2(self.dim_C)))
    
    def estimate_truncation_error(self, x0, F1, F2, steps=10):
        \"\"\"
        Estimates the analytical Carleman truncation error compared to exact recurrence.
        \"\"\"
        from carleman.operator import construct_discrete_carleman_step
        from carleman.linearize import lift_state, project_state
        
        M_C = construct_discrete_carleman_step(F1, F2, self.n_dim)
        
        x_exact = np.copy(x0)
        y_carleman = lift_state(x0, order=self.order)
        
        errors = []
        for _ in range(steps):
            # Exact nonlinear step
            x_exact = F1 @ x_exact + F2 @ np.kron(x_exact, x_exact)
            # Linear Carleman step
            y_carleman = M_C @ y_carleman
            x_c = project_state(y_carleman, self.n_dim)
            
            err = la.norm(x_exact - x_c) / (la.norm(x_exact) + 1e-14)
            errors.append(err)
            
        return errors
""")

# 4. carleman/validation.py
with open(os.path.join(carleman_dir, "validation.py"), "w") as f:
    f.write("""\"\"\"
Validation of Carleman Linearization against Classical Reference.
\"\"\"
import numpy as np
import scipy.linalg as la
from carleman.linearize import lift_state, project_state
from carleman.operator import construct_discrete_carleman_step

def validate_carleman_single_step(x0, F1, F2, atol=1e-7):
    \"\"\"
    Verifies that order-2 Carleman linearization matches the quadratic system
    identically in the first step: x_1 = F1 x0 + F2 (x0 (x) x0).
    \"\"\"
    n_dim = len(x0)
    M_C = construct_discrete_carleman_step(F1, F2, n_dim)
    
    y0 = lift_state(x0, order=2)
    y1 = M_C @ y0
    x1_c = project_state(y1, n_dim)
    
    x1_exact = F1 @ x0 + F2 @ np.kron(x0, x0)
    diff = la.norm(x1_exact - x1_c)
    
    return {
        "passed": bool(diff < atol),
        "difference": float(diff),
        "relative_error": float(diff / (la.norm(x1_exact) + 1e-14))
    }
""")

print("Successfully generated all Phase 5 Carleman linearization modules.")
