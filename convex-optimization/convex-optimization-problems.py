import cvxpy as cp

def problem1():
    x1 = cp.Variable()
    x2 = cp.Variable()
    constraints = [x1 >= 0, x2 >= 0, 2*x1 + x2 >= 1, x1 + 3*x2 >= 1]
    fs = [x1 + x2, x1**2 + 9 * x2**2]

    for f in fs:
        obj = cp.Minimize(f)
        prob = cp.Problem(obj, constraints)
        prob.solve()
        print(
            f"Status: {prob.status}, Optimal value: {prob.value},"
            f"Vars: {(x1.value, x2.value)}"
        )

def problem2():
    pass