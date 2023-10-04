from math import exp, sqrt
import math
from datetime import datetime
from scipy.stats import norm
from class_pricing.class_option import Option
from class_pricing.class_market import Market
from class_pricing.class_tree import Tree

def calculate_forward_price(interest_rates: float, delta_t: float) -> float:
    return exp(interest_rates * delta_t)  # = S_0 * exp(r * delta_t) avec S0 dans la cass node

def calculate_discount_price(interest_rates: float, delta_t: float) -> float:
    return exp(interest_rates * delta_t)  # = S_0 * exp(-r * delta_t) avec S0 dans la cass node 

