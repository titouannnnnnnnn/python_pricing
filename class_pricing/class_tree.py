from datetime import datetime
from dataclasses import dataclass
from class_pricing.class_option import Option
from class_pricing.class_market import Market
import numpy as np
import math
import datetime
from scipy.stats import norm
from math import exp, sqrt, log



class Tree:
    def __init(self,
    market:Market, 
    option:Option, 
    pricing_date : datetime, 
    nb_steps : int
    ):

        self.option = option
        self.market = market

        self.nb_steps = nb_steps
        self.pricing_date = pricing_date
        if pricing_date<self.option.maturity_date:
            raise ValueError("Pricing date must be before the maturity date")
        else:
            self.delta_t = calculate_delta_t()
            #=((maturity_date-pricing_date)/nb_steps)/365
            #why 365 ? to have the number in year, i.e x/365

        self.alpha = calculate_alpha(sqrt(3))



def calculate_delta_t(self) -> datetime:
    return ((self.option.maturity_date - self.pricing_date)/self.nb_steps) / 365


def calculate_alpha(self, mutliplicateur:float) -> float:
    return exp (self.market.volatility * mutliplicateur * sqrt (self.delta_t))
    #alpha = exp (sigma * multiplicateur * racine(delta_t)), avec souvent mutliplicateur = racine (3)