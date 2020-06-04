import abc

import numpy as np
import matplotlib.pyplot as plt


plt.style.use("seaborn")


class Solver(abc.ABC):
    
    def __init__(self, f):
        self.f = f

    def solve(
        self,
        x0,
        max_niter=10000,
        threshold=0.1,
        alpha=0.1,
        beta=0.75,
        plot=False
    ):
        x = x0
        fs = []
        for i in range(max_niter):
            delta = self.delta(x)
            if self.stop(x, delta, threshold):
                print(f"Convergence achieved in {i} iterations.")
                break
            f_x = self.f(x)
            grad_x = self.grad(x)
            fs.append(f_x)
            # Backtracking
            mu = 1
            while (
                self.f(x + mu * delta)
                > f_x + mu * alpha * np.sum(grad_x * delta)
            ):
                mu *= beta
            x = x + mu * delta
        else:
            print("Solver did not converge.")

        if plot:
            plt.figure()
            plt.plot(fs)
            plt.xlabel("Iteration")
            plt.ylabel("Objective")
            plt.show()
        
        return self.f(x), x

    @abc.abstractmethod
    def delta(self, x):
        pass

    @abc.abstractmethod
    def stop(self, x, delta, threshold):
        pass


class GradientDescent(Solver):
    
    def __init__(self, f, grad):
        self.grad = grad
        super().__init__(f)

    def stop(self, x, delta, threshold):
        return np.linalg.norm(delta) < threshold
    
    def delta(self, x):
        return -self.grad(x)

class NewtonRaphson(Solver):
    
    def __init__(self, f, grad, hessian):
        self.grad = grad
        self.hessian = hessian
        super().__init__(f)

    def stop(self, x, delta, threshold):
        if isinstance(x, np.ndarray):
            return np.abs(self.grad(x) @ delta) < threshold
        else:
            return abs(self.grad(x) * delta) < threshold
    
    def delta(self, x):
        if isinstance(x, np.ndarray):
            return np.linalg.solve(self.hessian(x), -self.grad(x))
        else:
            return -self.grad(x) / self.hessian(x)