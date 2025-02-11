import numpy as np
import matplotlib.pyplot as plt

from abc import ABC, abstractmethod
from dataclasses import astuple, dataclass, field
from enum import Enum
from scipy.stats import binom
from typing import Union, NamedTuple


class ExerciseStyle(Enum):
    European = 1
    American = 2
    Bermudan = 3

class ExerciseType(Enum):
    Call = 1
    Put  = 2
    Forward = 3

@dataclass(frozen=True, kw_only=True, slots=True)
class FinancialOption:
    ex_style: ExerciseStyle = ExerciseStyle.European
    ex_type: ExerciseType = ExerciseType.Call
    spot: float = 41.0
    strike: float = 40.0
    rate: float = 0.08
    volatility: float = 0.30
    dividend: float = 0.0
    expiry: float = 1.0



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


REGISTRY = {
    ExerciseType.Call: CallPayoff,
    ExerciseType.Put: PutPayoff,
}

def create_payoff(ex_type: ExerciseType, strike: float) -> OptionPayoff:
    payoff_class = REGISTRY[ex_type]
    return payoff_class(strike=strike)


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

    i = np.arange(nodes)
    #for i in range(nodes):
    #    spot_prices[i] = (u**(num_periods-i)) * (d**i) * spot
    spot_prices = (u**(num_periods-i)) * (d**i) * spot


    # Calculate the terminal option values
    payoffs = payoff(spot_prices)

    # Calculate the risk-neutral probabilities
    p_star = (np.exp((rate - dividend)*h) - d) / (u - d)
    probs = np.zeros(nodes)

    #for i in range(nodes):
    probs = binom.pmf(num_periods-i, num_periods, p_star)

    # Calculate the expected (rnp) option payoff at expiry and discount it
    C0 = np.exp(-rate * expiry) * np.dot(payoffs, probs)

    return C0

class Result(NamedTuple):
    option: dataclass #FinancialOption
    price: float 
    delta: float = None
    std_err: float = None
    n_steps: int = None
    n_reps: int = None

def lattice(option: FinancialOption, n_steps: int) -> Result:
    ex_style, ex_type, S, K, r, v, q, T = astuple(option)
    #payoff = PayoffFactory.create(ex_type.name, strike=K)
    payoff = create_payoff(ex_type, K)

    dt = T/n_steps
    u = np.exp((r - q)*dt + v*np.sqrt(dt))
    d = np.exp((r - q)*dt - v*np.sqrt(dt))
    pu = (np.exp((r - q)*dt) - d) / (u - d)
    pd = 1.0 - pu
    dsc = np.exp(-r * dt)

    ii = np.arange(n_steps + 1)
    x = S * (u ** (n_steps - ii)) * (d ** ii)
    f = payoff(x)

    for i in range(n_steps - 1, -1, -1):
        for j in range(i + 1):
            f_tmp = dsc * (pu*f[j] + pd*f[j+1]) 
            x[j] /= u
            f[j] = np.maximum(f_tmp, payoff(x[j])) if ex_style == ExerciseStyle.American else f_tmp

    price = np.maximum(f[0], payoff(S))

    return Result(
        option=option,
        price=price,
        delta=0.5,
        n_steps=n_steps
    )