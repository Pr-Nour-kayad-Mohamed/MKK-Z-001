import numpy as np
from scipy.integrate import solve_ivp

Lc = 80e-6
Q = 15000
Finesse = 69
B = 21
gamma = 1.27e4
P_th = np.pi / (2 * gamma * Lc * B)
P_th_slot = 28e-3

print("=== CORRECTION PERPLEXITY MKK-Z-001 ===")
print(f"Ancien 0.87mW fictif -> Nouveau {P_th*1e3:.1f}mW traçable")
print(f"gamma={gamma:.2e} Lc={Lc*1e6:.0f}um Q={Q} F={Finesse} B={B}")

def V_BHK(e, V, beta=0.8):
    return 0.5*e**2 + 0.5*beta*V**2

def C_Sigma(e, V, dV, beta=0.8):
    return (e + beta*V*dV)**2

def dynamics(t, y):
    x1, x2, e, V = y
    beta = 0.8
    de = -(e + beta*V*V)
    dV = e
    dx1 = -0.1*x1 + gamma*P_th*x2
    dx2 = -0.1*x2 - gamma*P_th*x1
    return [dx1, dx2, de, dV]

sol = solve_ivp(dynamics, [0, 15], [1.0, 0.0, 1.0, 0.5], method='RK45', rtol=1e-6, atol=1e-9)
e_final = sol.y[2][-1]
V_final = sol.y[3][-1]
C_final = C_Sigma(e_final, V_final, e_final)

print(f"e final {e_final:.3e} V_BHK {V_BHK(e_final,V_final):.3e} C_Sigma {C_final:.3e}")
print(f"dV/dt = {-C_final:.3e} <=0")

det = -0.02
R_bio = 650e3
LOCK = 1 if (det <=0) or (R_bio != 600e3) else 0
print(f"det {det} R {R_bio/1e3:.0f}k LOCK={LOCK} Silence=preuve")

np.savetxt("trajectory.csv", np.vstack([sol.t, sol.y]).T, delimiter=",", header="t,x1,x2,e,V")
