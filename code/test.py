from binomial import *

S = 41.0
K = 40.0
v = 0.30
r = 0.08
q = 0.0
T = 1.0
n = 3
call_payoff = CallPayoff(K)

C0 = european_multi_period_binomial(S, K, v, r, q, T, n, call_payoff)
print(f"The Call price is: ${C0}")