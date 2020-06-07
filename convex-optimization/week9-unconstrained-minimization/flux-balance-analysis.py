import itertools as it

import numpy as np
import cvxpy as cp

"""
data file for flux balance analysis in systems biology
From Segre, Zucker et al "From annotated genomes to metabolic flux
models and kinetic parameter fitting" OMICS 7 (3), 301-316. 
"""
# Stoichiometric matrix
S = np.array([
#	M1	M2	M3	M4	M5	M6	
	[1,	0,	0,	0,	0,	0],	#	R1:  extracellular -->  M1
	[-1, 1,	0,	0,	0,	0],	#	R2:  M1 -->  M2
	[-1, 0,	1,	0,	0,	0],	#	R3:  M1 -->  M3
	[0,	-1,	0,	2,	-1,	0],	#	R4:  M2 + M5 --> 2 M4
	[0,	0,	0,	0,	1,	0],	#	R5:  extracellular -->  M5
	[0,	-2,	1,	0,	0,	1],	#	R6:  2 M2 -->  M3 + M6
	[0,	0,	-1,	1,	0,	0],	#	R7:  M3 -->  M4
	[0,	0,	0,	0,	0, -1],	#	R8:  M6 --> extracellular
	[0,	0,	0,	-1,	0,	0],	#	R9:  M4 --> cell biomass
]).T
m, n = S.shape
v_max = np.array([
	10.10,	# R1:  extracellular -->  M1
	100,	# R2:  M1 -->  M2
	5.90,	# R3:  M1 -->  M3
	100,	# R4:  M2 + M5 --> 2 M4
	3.70,	# R5:  extracellular -->  M5
	100,	# R6:  2 M2 --> M3 + M6
	100,	# R7:  M3 -->  M4
	100,	# R8:  M6 -->  extracellular
	100,	# R9:  M4 -->  cell biomass
])

v = cp.Variable(n)
objective = cp.Maximize(v[-1])
constraints = [S @ v == 0, v >= 0, v <= v_max]
problem = cp.Problem(objective, constraints)
problem.solve()
print(f"The optimal G is: {problem.value}")

non_zero_multipliers = np.argwhere(
	constraints[2].dual_value > 1e-9
)
max_multiplier = np.argmax(constraints[2].dual_value)
print(f"Non zero multipliers: {non_zero_multipliers}")
print(f"Max multiplier: {max_multiplier}")
min_G = 0.2 * problem.value

essentials = []
for i in range(n):
	new_G = cp.Problem(objective, constraints + [v[i] == 0]).solve()
	if new_G < min_G:
		essentials.append(i)
print(f"The {essentials} genes are essential.")

non_essentials = filter(lambda i: i not in essentials, range(n))
pairs = it.combinations(non_essentials, 2)
lethals = []
for g1, g2 in pairs:
	new_G = cp.Problem(objective, constraints + [v[g1] == 0, v[g2] == 0]).solve()
	if new_G < min_G:
		lethals.append((g1, g2))
print(f"The combinations {lethals} are lethals.")