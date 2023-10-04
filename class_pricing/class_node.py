from datetime import datetime
from dataclasses import dataclass
from datetime import datetime
from dataclasses import dataclass
from class_pricing.class_option import Option
from class_pricing.class_market import Market
from class_pricing.class_tree import Tree
from class_pricing.function import calculate_forward_price
import numpy as np
import math
import datetime
from scipy.stats import norm
from math import exp, sqrt, log


class Node:



    def __init__(self,tree,spot_price:float):

        self.tree=tree
        self.spot_price=spot_price
        self.forward_price = calculate_forward_price(
        self.spot_price, 
        self.market.interest_rate, 
        self.tree.delta_t
        )
        #proba_up_test = self.forward_price * self.tree.alpha
        #proba_down_test = self.forward_price / self.tree.alpha
        # mettre dans init les autres trucs du bas genre esperance, variance, proba up mid and down

    def calculate_proba(self)->float:
        esperance=self.spot_price * calculate_forward_price(sqrt(3)) - self.market.dividend_price
        variance= (self.spot_price **2) * exp(2*self.market.interest_rates * self.tree.delta_t) * (exp(self.market.volatility**2 * self.tree.delta_t) -1)

        self.proba_down= (1/self.forward_price**2)*((variance + esperance**2) -1-(1/self.forward_price * self.forward_price - 1)/(1-self.tree.alpha)*((1/self.tree.alpha**2)-1))
        self.proba_up= self.proba_down/self.tree.alpha
        self.proba_mid=1 - self.proba_down - self.proba_up
        #verifier les conditions peut etre

        if self.proba_down + self.proba_mid + self.proba_up != 1:
            raise ValueError('The sum of the probabilities down + mid + up must be equal to 1')
        
    def calculate_state(self) -> float:


    def calculate_option(self) -> float:
        
        self.up_price = self.spot_price * self.tree.alpha
        self.down_price = self.spot_price / self.tree.alpha
        self.mid_price = self.forward_price

    def calculate_option_type(self) -> float :
        if self.option.option_type=="call":
            return max (0, self.spot_price - self.option.strike_price)
        if self.option.option_type=="put":
            return max (0,self.option.strike_price - self.spot_price)
        else:
            raise ValueError("Wrong input, please insert call or put")
        
    def calculate_option_value(self) -> float :
        #arranger calculate_option avec calculate_option_type afin de compute au bon endroit
        if next_node = "up":
            self.otption_value = self.up_price
        elif next_node= "down":
            self.otption_value=self.down_price
        elif next_node= "mid":
            self.otption_value=self.mid_price
        else:
            raise ValueError("You may have a problem, please look")
    
    def __str__(self):
        return f'About the market information, we have/n - spot price is equal to {self.spot_price:.2f}/n - volatility which is equal to {self.market.volatility:.2f}'
        