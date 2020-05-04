import numpy as np
import cvxpy as cp
import matplotlib.pyplot as plt


plt.style.use("seaborn")

# create problem data  
N = 100
x = np.zeros(N)
x[1:40] = 0.1
x[50] = 2
x[70:80] = 0.15
x[80] = 1
x = np.cumsum(x)
# pass the increasing input through a moving-average filter 
# and add Gaussian noise
h = np.array([1, -0.85, 0.7, -0.3])
k = len(h)
# Remove last k-1 element of convolve
y = np.convolve(h, x)
y = y[:-k+1]
noise = np.array([
    -0.43, -1.7, 0.13, 0.29, -1.1, 1.2, 1.2, -0.038, 0.33,
    0.17, -0.19, 0.73, -0.59, 2.2, -0.14, 0.11, 1.1, 0.059,
    -0.096, -0.83, 0.29, -1.3, 0.71, 1.6, -0.69, 0.86, 1.3,
    -1.6, -1.4, 0.57, -0.4, 0.69, 0.82, 0.71, 1.3, 0.67, 1.2,
    -1.2, -0.02, -0.16, -1.6, 0.26, -1.1, 1.4, -0.81, 0.53,
    0.22, -0.92, -2.2, -0.059, -1, 0.61, 0.51, 1.7, 0.59,
    -0.64, 0.38, -1, -0.02, -0.048, 4.3e-05, -0.32, 1.1, 
    -1.9, 0.43, 0.9, 0.73, 0.58, 0.04, 0.68, 0.57, -0.26,
    -0.38, -0.3, -1.5, -0.23, 0.12, 0.31, 1.4, -0.35, 0.62,
    0.8, 0.94, -0.99, 0.21, 0.24, -1, -0.74, 1.1, -0.13, 0.39,
    0.088, -0.64, -0.56, 0.44, -0.95, 0.78, 0.57, -0.82, -0.27
])
s = y + noise

# Solving the ML estimation
x_ = cp.Variable(N)
y_ = cp.conv(h, x_)[:-k+1].flatten()
constraints = [0 <= x_[0]] + [
    x_[i] <= x_[i+1] for i in range(0, N-1)
]
# With constraints
cp.Problem(cp.Minimize(cp.norm(y_ - s)), constraints).solve()
x_hat = x_.value
y_hat = y_.value
# Without constraints
cp.Problem(cp.Minimize(cp.norm(y_ - s))).solve()
x_hat_free = x_.value
y_hat_free = y_.value
fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(14, 8))

# Plotting the results
axs[0].plot(x, label="Origial")
axs[0].plot(x_hat, label="Estimated")
axs[0].plot(x_hat_free, linestyle="--", label="Estimated (no Constraints)")
axs[0].set_title("Input Signals")
axs[0].legend()

axs[1].plot(s, label="Noisy")
axs[1].plot(y, label="Original")
axs[1].plot(y_hat, label="Estimated")
axs[1].plot(y_hat_free, linestyle="--", label="Estimated (no Constraints)")
axs[1].set_title("Output Signal")
axs[1].legend()

plt.show()
