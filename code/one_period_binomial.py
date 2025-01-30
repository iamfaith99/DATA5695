import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod
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
    f_u = payoff(uS)
    f_d = payoff(dS) 

    # solve for D and B
    D = (f_u - f_d) / (uS - dS)
    B = np.exp(-rate * expiry) * ((u*f_d - d*f_u) / (u - d))
    
    # solve for the option premium
    f = spot*D + B

    return f, D, B


