import abc

import cvxpy as cp
import numpy as np

# Stock market options
class Option(abc.ABC):
    def __init__(self, price, start_stock_price=1):
        self.price = price
        self.start_stock_price = start_stock_price

    @abc.abstractmethod
    def payoff(self, end_stock_price):
        pass


class Keep(Option):
    def __init__(self, start_stock_price=1):
        super().__init__(start_stock_price, start_stock_price)

    def payoff(self, end_stock_price):
        return end_stock_price


class Call(Option):
    def __init__(self, strike, price, start_stock_price=1):
        self.strike = strike
        super().__init__(price, start_stock_price)

    def payoff(self, end_stock_price):
        return max(0, end_stock_price - self.strike)


class Put(Option):
    def __init__(self, strike, price, start_stock_price=1):
        self.strike = strike
        super().__init__(price, start_stock_price)

    def payoff(self, end_stock_price):
        return max(0, self.strike - end_stock_price)


class Collar(Option):
    def __init__(self, cap, floor, price, start_stock_price=1):
        self.cap = cap
        self.floor = floor
        super().__init__(price, start_stock_price)

    def payoff(self, end_stock_price):
        if end_stock_price > self.cap:
            return self.cap - self.start_stock_price
        elif end_stock_price < self.floor:
            return self.floor - self.start_stock_price
        else:
            return end_stock_price - self.start_stock_price


# Variables
M = 200
stock0 = 1
r = 1.05
stocks = np.linspace(0.5, 2, 200)
p = cp.Variable()
y = cp.Variable(M)

options = (
    Keep(stock0),
    Call(1.1, 0.06, stock0),
    Call(1.2, 0.03, stock0),
    Put(0.8, 0.02, stock0),
    Put(0.7, 0.01, stock0),
    Collar(1.15, 0.9, p, stock0),
)
prices = cp.hstack([1] + [option.price for option in options])

# Outcomes matrix V
V = []
for stock in stocks:
    subV = [r]  # The risk fre asset
    for option in options:
        subV.append(option.payoff(stock))
    V.append(subV)
V = np.array(V)

constraints = [V.T @ y == prices, y >= 0]
lower_price = cp.Problem(cp.Minimize(p), constraints).solve()
upper_price = cp.Problem(cp.Maximize(p), constraints).solve()

print("Range of prices for Collar Option:, ", (lower_price, upper_price))
