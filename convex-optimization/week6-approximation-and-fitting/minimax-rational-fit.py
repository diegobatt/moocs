import numpy as np
import cvxpy as cp

K = 200
ts = np.array([(-3 + 6 * i / K) for i in range(0, K + 1)])
ys = np.exp(ts)
polinomial = np.vstack([np.ones(K + 1), ts, ts**2])

a = cp.Variable(3)
b_ = cp.Variable(2)
b = cp.hstack([1, b_])
numer = a @ polinomial
denom = b @ polinomial
phis = numer - cp.multiply(ys, denom)
objective = cp.norm(numer / denom - ys, "inf")

lower, upper, status = 0, 10000, None

# Bisection up to 3 significant digits
while (upper - lower) > 0.001 or status == "infeasible":  
    middle = lower + (upper - lower) / 2
    print(
        f"Next bound to try: {middle}. ",
        f"currently inside ({lower}, {upper}) range"
    )
    constraints = [
        denom >= 1e-60, # No strict inequalities allowed
        cp.abs(phis) <= middle * denom,
    ]
    problem = cp.Problem(cp.Minimize(1), constraints)
    problem.solve()
    status = problem.status
    if status == "infeasible":
        lower = middle
    else:
        upper = middle

print(
    f"Finished bisection:  a = {a.value}, b = {b.value}, ",
    f"Optimal value = {objective.value}, {middle}"
)
