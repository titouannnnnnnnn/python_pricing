from class_pricing.class_option import Option
from class_pricing.class_market import Market
import numpy as np
import math
import datetime
from scipy.stats import norm
from math import exp, sqrt, log


class BS:


    def __init__(self, option:Option,market:Market):
        self.market=market
        self.option=option



    def calculate_d1(self) -> float:
        spot_price = self.market.spot_price
        strike_price = self.option.strike_price
        volatility = self.market.volatility
        interest_rate = self.market.interest_rate
        maturity_date = self.option.maturity_date
        d1=1/(self.market.volatility*sqrt(time_to_maturity)) * (log(market.spot_price/option.strike_price) 
        + (market.interest_rate+(market.volatility**2)/2)*time_to_maturity)
        return d1

    def calculate_d2(option : Option, market : Market) -> float:
        d2=calculate_d1-market.volatility*sqrt(time_to_maturity)
        return d2

    def time_to_maturity(self) -> float:
        nb_days = 365
        maturity_date=self.option.maturity_date
        current_date=datetime.now()
        time_to_maturity=(maturity_date - current_date) /nb_days #pour avoir en fraction
        return time_to_maturity

    def calculate_norm(x : float) ->float:
        return norm.cdf(x)


    def calculate_option_price(option : Option, market : Market) -> float:
        d1=calculate_d1
        d2=calculate_d2
        if option.option_type== "call":
            option_price = market.spot_price * calculate_norm(d1) - option.strike_price * calculate_norm(d2)* exp(-market.interest_rate * time_to_maturity)
        if option.option_type== "put":
            option_price =  option.strike_price * calculate_norm(-d2)* exp(-market.interest_rate * time_to_maturity) - market.spot_price * calculate_norm(-d1)
        else:
            raise ValueError("Option type does not exist, please select call or put")
        
        return option_price