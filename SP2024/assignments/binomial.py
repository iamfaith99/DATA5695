import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import binom
from typing import Callable

def call_payoff(spot: np.ndarray, strike: np.ndarray) -> np.ndarray:
    return np.maximum(spot - strike, 0.0)

def put_payoff(spot: np.ndarray, strike: np.ndarray) -> np.ndarray:
    return np.maximum(strike - spot, 0.0)

# European at first
def binomial(
    spot: float,
    strike: float,
    rate: float,
    volatility: float,
    dividend: float,
    expiry: float, 
    steps: int,
    payoff: Callable) -> float:

    nodes = steps + 1
    h = expiry / steps
    u = np.exp((rate - dividend) * h + np.sqrt(h) * volatility)
    d = np.exp((rate - dividend) * h - np.sqrt(h) * volatility)
    disc = np.exp(-rate * expiry)
    pu = (np.exp((rate - dividend) * h) - d) / (u - d)
    pd = 1.0 - pu

    prc_t = 0.0
    
    for i in range(nodes):
        spot_t = spot * (u ** (steps - i) * (d ** i))
        prob_t = binom.pmf(steps - i, steps, pu)
        prc_t += payoff(spot_t, strike) * prob_t

    prc_t *= disc

    return prc_t
