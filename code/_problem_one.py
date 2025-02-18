import numpy as np
from binomial import *

## Set up the term sheet and market data
data = {
    'ex_style': ExerciseStyle.European,
    'ex_type': ExerciseType.Call,
    'spot': 100.0,
    'strike': 105.0,
    'rate': 0.08,
    'volatility': 0.30,
    'dividend': 0.0,
    'expiry': 0.5
}

## Create the call option object
the_call = FinancialOption(**data)

## Price the option
result = lattice(the_call, 3)
print(f"The call price is: {result.price}")