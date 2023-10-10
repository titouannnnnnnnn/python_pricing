from math import exp, sqrt
from datetime import datetime
from scipy.stats import norm



'''
Ensemble des definitions utiles pour les autres classes
'''

### Forward
def calculate_forward_price(spot_price, interest_rates, delta_t) -> float:
    return spot_price * calculate_forward_factor (interest_rates, delta_t)

def calculate_forward_factor(interest_rates: float, delta_t: float) -> float:
    return exp(interest_rates * delta_t)  # = S_0 * exp(r * delta_t) avec S0 dans la cass node


### Discount
def calculate_discount_price(spot_price, interest_rates: float, delta_t: float) -> float:
    return spot_price * calculate_discount_factor(interest_rates, delta_t)

def calculate_discount_factor(interest_rates: float, delta_t: float) -> float:
    return exp(interest_rates * delta_t)  # exp(-r * delta_t) avec S0 dans la cass node 




### Delta_t
def calculate_delta_t(maturity_date:datetime, pricing_date:datetime,nb_steps:int, nb_days:int) -> float:
    return ((maturity_date - pricing_date)/nb_steps) / nb_days
    # delta_t = ((date_maturite - date_pricing)/ nb_steps)/365
    #il calcule le facteur entre chaque noeud selon nos dates d'arrivées et depart
    # on divise le tout par le nb de steps pour subdivisions
    #enfin on divise par 365 pour avoir sous format jour


### Alpha
def calculate_alpha(volatility:float, delta_t:float, mutliplicateur:float) -> float:
    return exp (volatility * mutliplicateur * sqrt (delta_t))
    #alpha = exp (sigma * multiplicateur * racine(delta_t)), avec souvent mutliplicateur = racine (3)


def calculate_norm(x : float) ->float:
    return norm.cdf(x)
    #sert pour le cauclu de d1 et d2