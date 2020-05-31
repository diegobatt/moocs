import abc

import numpy as np
import matplotlib as plt


class Solver(abc.ABC):
    
    def __init__(self, f):
        self.f = f

    def solve(
        self,
        x0,
        max_niter=10000,
        threshold=0.01,
        alpha=0.1,
        beta=0.75
    ):
        x = x0
        for i in range(max_niter):
            delta = self.delta(x)
             if self.stop(x, delta, threshold):
                print(f"Convergence achieved in {i} iterations.")
                break
            # Backtracking
            mu = 1
            while self.f(x + mu * delta) > self.f(x) + mu * alpha * delta:
                mu *= beta
            x = x + mu * delta
        else:
            print("Solver did not converge.")
        
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
        super(GradientDescent, self).__init__(f)


    def stop(self, x, threshold):
        return np.linalg.norm(self.grad(x)) < threshold
    
    def delta(self, x):
        return -self.grad(x)

class NewtonRaphson(Solver):
    
    def __init__(self, f, grad, hessian):
        self.grad = grad
        self.hessian = hessian
        super(GradientDescent, self).__init__(f)


    def stop(self, x, threshold):
        return np.linalg.norm(self.grad(x)) < threshold
    
    def delta(self, x):
        return -self.grad(x)