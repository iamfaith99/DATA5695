import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod
from scipy.stats import binom
from typing import Union


class OptionPayoff(ABC):
    def __init__(self, strike: float): 
        self._strike = strike 

    @property
    def strike(self) -> float:
        return self._strike 
    
    @strike.setter
    def strike(self, new_strike: float):
        self._strike = new_strike

    @abstractmethod
    def __call__(self, spot: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        pass 

class CallPayoff(OptionPayoff):
    """Derived class for vanilla call option payoff."""

    def __call__(self, spot: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        return np.maximum(spot - self._strike, 0.0)
    
class PutPayoff(OptionPayoff):
    """Derived class for vanilla put option payoff."""

    def __call__(self, spot: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        return np.maximum(self._strike - spot, 0.0)

def single_period_binomial(spot: float, strike: float, volatility: float, rate: float, dividend: float, expiry: float, payoff: OptionPayoff) -> float:
    # build the forward tree
    u = np.exp((rate - dividend)*expiry + volatility*np.sqrt(expiry))
    d = np.exp((rate - dividend)*expiry - volatility*np.sqrt(expiry))
    uS, dS = u*spot, d*spot

    # apply the payoff function 
    fu = payoff(uS)
    fd = payoff(dS) 

    # solve for D and B
    #D = (f_u - f_d) / (uS - dS)
    #B = np.exp(-rate * expiry) * ((u*f_d - d*f_u) / (u - d))

    # solve for the risk-neutral probabilities
    pu = ((np.exp(rate - dividend)*expiry - d) / (u - d))
    pd = 1.0 - pu
    
    # solve for the option premium
    f0 = np.exp(-rate * expiry) * (pu*fu + pd*fd)

    return f0
def european_multi_period_binomial(
    spot: float,
    strike: float,
    volatility: float,
    rate: float,
    dividend: float,
    expiry: float,
    num_periods: float,
    payoff: OptionPayoff) -> float:

    # Build the forward tree
    nodes = num_periods + 1
    h = expiry / num_periods
    u = np.exp((rate - dividend)*h + volatility*np.sqrt(h))
    d = np.exp((rate - dividend)*h - volatility*np.sqrt(h))
    spot_prices = np.zeros(nodes)

    for i in range(nodes):
        spot_prices[i] = (u**(num_periods-i)) * (d**i) * spot

    # Calculate the terminal option values
    payoffs = payoff(spot_prices)

    # Calculate the risk-neutral probabilities
    p_star = (np.exp((rate - dividend)*h) - d) / (u - d)
    probs = np.zeros(nodes)

    for i in range(nodes):
        probs[i] = binom.pmf(num_periods-i, num_periods, p_star)

    # Calculate the expected (rnp) option payoff at expiry and discount it
    C0 = np.exp(-rate * expiry) * np.dot(payoffs, probs)

    return C0
