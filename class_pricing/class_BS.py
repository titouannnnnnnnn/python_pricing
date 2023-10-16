from datetime import  timedelta
from class_pricing.class_option import Option
from class_pricing.class_market import Market
#from class_pricing.class_node import Node
from class_pricing.class_tree import Tree
from datetime import datetime
from scipy.stats import norm
from math import exp, sqrt, log
from class_pricing.function import calculate_norm

class BS:
    nb_days=365

    def __init__(self, option:Option,market:Market,tree: Tree):
        self.market=market
        self.option=option
        self.tree=tree

    def calculate_d1_d2(self) -> float:

        self.d1=1/(self.market.volatility*sqrt(self.time_to_maturity_value)) * (log(self.market.spot_price/self.option.strike_price) 
        + (self.market.interest_rate+(self.market.volatility**2)/2)*self.time_to_maturity_value)
        
        self.d2=self.d1-self.market.volatility*sqrt(self.time_to_maturity_value)
        
    def time_to_maturity(self) -> float:
        nb_days = 365
        #current_date=datetime.now()
        self.time_to_maturity_value=((self.option.maturity_date - self.tree.pricing_date)) /nb_days #pour avoir en fraction #  
        #self.time_to_maturity_value=((self.option.maturity_date - self.tree.pricing_date).days) /nb_days 
        #.days necessaire ?

    def calculate_option_price(self) -> float:
        if self.option.option_type== "call":
            option_price_BS = self.market.spot_price * calculate_norm(self.d1) - self.option.strike_price * calculate_norm(self.d2)* exp(-self.market.interest_rate * self.time_to_maturity_value)
        if self.option.option_type== "put":
            option_price_BS =  self.option.strike_price * calculate_norm(-self.d2)* exp(-self.market.interest_rate * self.time_to_maturity_value) - self.market.spot_price * calculate_norm(-self.d1)
        else:
            raise ValueError("Option type does not exist, please select call or put")
        
        return option_price_BS


    def calculate_check_BS(self):
        if self.market.spot_price * calculate_norm(self.d1) - self.option.strike_price * calculate_norm(self.d2)* exp(-self.market.interest_rate * self.time_to_maturity_value)\
        -self.option.strike_price * calculate_norm(-self.d2)* exp(-self.market.interest_rate * self.time_to_maturity_value) - self.market.spot_price * calculate_norm(-self.d1) != \
        self.market.spot_price - self.option.strike_price * exp(-self.market.interest_rate * self.tree.delta_t) :
            raise ValueError("Problem about BS")
    


        
        