from __future__ import annotations
from datetime import  timedelta
from class_pricing.class_option import Option
from class_pricing.class_market import Market
from class_pricing.class_tree import Tree
from class_pricing.function import calculate_forward_factor, calculate_discount_factor, calculate_forward_price
from math import exp
from class_pricing.class_node import Node


class Node:


    def __init__(self,market,tree,spot_price:float) -> None:

        self.tree=tree
        self.market=market
        self.spot_price=spot_price

        self.forward_price = calculate_forward_price
        (
        self.spot_price, 
        self.market.interest_rate, 
        self.tree.delta_t
        )

        


        #for i in range(self.tree.nb_steps):
        if (self.tree.pricing_date
            <= self.market.dividend_ex_date
            <=self.tree.pricing_date + timedelta ( self.tree.delta_t * self.tree.nb_days).days
        ):
            forward_ajuste= self.forward_price-self.market.dividend_price
        else:
            forward_ajuste = self.forward_price
            
        self.forward_price = forward_ajuste

        self.down_node = None  # Initialise down_node à None
        self.mid_node = None    # Initialise mid_node à None
        self.up_node = None     # Initialise up_node à None
    
       
        # mettre dans init les autres trucs du bas genre esperance, variance, proba up mid and down
    # def calculate_all(self):
    #     self.calculate_variance()
    #     self.calculate_proba()
    #     self.calculate_option()
    #     self.calculate_check()


    def calculate_esperance(self)->float:
        self.esperance=self.spot_price * calculate_forward_factor(self.market.interest_rate, self.tree.delta_t) - self.market.dividend_price
        # calcul de l'esperance utile pour calcul des proba, et aussi pour verifier les conditions (voir calculate_check)
        

    def calculate_variance(self)-> float:
        self.variance=(self.spot_price **2) * exp(2*self.market.interest_rate * self.tree.delta_t) * (exp(self.market.volatility**2 * self.tree.delta_t) -1)
        # calcul de la variance utile pour calcul des proba, et aussi pour verifier les conditions (voir calculate_check)


    def calculate_proba(self)->float:
        self.proba_down= (1/self.forward_price**2)*((self.variance + self.esperance**2)- 1 -(self.tree.alpha + 1) *(1/self.forward_price * self.esperance - 1)/(1-self.tree.alpha)*((1/self.tree.alpha**2)-1))
        self.proba_up= self.proba_down/self.tree.alpha
        self.proba_mid=1 - self.proba_down - self.proba_up
        # calcul des différentes proba, c'est à dire proba pour aller vers état up, mid et odwn


    def calculate_option(self) -> float:
        self.up_price = self.spot_price * self.tree.alpha
        self.down_price = self.spot_price / self.tree.alpha
        self.mid_price = self.forward_price
        # calcul des prix de l'option
        # S_u = S * alpha ... -> T
        # S_d = S / alpha ... -> T
        # S_m = Fwd ... -> T

    

    def calculate_check(self):
        if self.proba_down + self.proba_mid + self.proba_up != 1:
            raise ValueError('The sum of the probabilities down + mid + up must be equal to 1, please look at node class')
            #si somme des proba différent de 1 -> error 
        elif (self.down_price* self.proba_down + self.mid_price * self.proba_mid + self.up_price + self.proba_up) != self.forward_price:
            raise ValueError('Moment of order 1 is not verified')
            # it good : self.forward_price = self.esperance
            # Moment d'ordre 1:
        elif (self.down_price**2 * self.proba_down + self.mid_price**2 * self.proba_mid + self.up_price**2 + self.proba_up) != self.variance + self.esperance **2: 
            raise ValueError('Moment of order 2 is not verified')
        

    def price (self, option:Option) -> float:
        if self.next_mid is None: #quand on se retrouve a T
            self.option_value = option.payoff(self.spot_price)


        elif self.option_value is None: #[0 , T-1]
            self.option_value = calculate_discount_factor(self.market.interest_rate, self.tree.delta_t)*(
            self.proba_up * self.up_price + 
            self.proba_mid * self.mid_price + 
            self.proba_down * self.down_price
            ) #exp (-r * delta_t)* [proba pondéré par prix]
        elif option.option_type == "am":
            self.option_value= max(self.option_value, option.payoff(self.spot_price)) #prend le max entre VI et valeur du noeud
        else :
            raise ValueError("Problem about the function price, please look at node class")

        return self.option_value


    def build_block(self, next:Node):
        nmid=self.get_mid(next)
        if nmid.down_node is None:
            ndown=Node(self.market,self,nmid.spot_price/self.tree.alpha)
            ndown.up_node=nmid
            nmid.down_node=ndown
        else:
            ndown=nmid.down_node
        if nmid.up_node is None:
            nup=Node(self.market,self,nmid.spot_price*self.tree.alpha)
            nup.down_node=nmid
            nmid.up_node=nup
        else:
            nup=nmid.up_node

            #self.tree.next_mid=nmid
        self.next_mid = nmid


    def is_close(self,forward) -> bool:
        return self.spot_price * (1+1/self.tree.alpha)/2 <= forward <= self.spot_price * (1+self.tree.alpha)/2


    def get_mid(self,next : Node):
        forward= calculate_forward_price(self.spot_price, self.market.interest_rate, self.tree.delta_t)
        if next.is_close(forward): #regarder si None ou pas, avec debeuguuer
            return next
        elif forward > self.spot_price:
            while not next.is_close(forward):
                next=next.move_up()
        else :
            while not next.is_close(forward):
                next=next.move_down()
        return next
                 



    def move_up(self):
        if self.up_node is None:
            nup=Node(self.market,self,self.spot_price*self.tree.alpha)
            nup.down_node=self
            self.up_node=nup
            #return nup
        else:
            nup = self.up_node
            #return self.up_node

        return nup
        #rien


    def move_down(self) :
        if self.down_node is None:
            ndown=Node(self.market,self,self.spot_price/self.alpha)
            ndown.up_node=self
            self.down_node=ndown
        else:
            ndown=self.down_node

        return ndown          

    def __str__(self) -> str:
        result_node = "Node class -\n"
        result_node += f"  Spot Price: {self.spot_price:.2f}\n"
        result_node += f"  Forward Price: {self.forward_price:.2f}\n"
        result_node += f"  Variance: {self.variance:3f}\n"
        result_node += f"  Esperance: {self.esperance:.3f}\n"
        result_node += f"  Proba Up: {self.proba_up:.3f}\n"
        result_node += f"  Proba Mid: {self.proba_mid:.3f}\n"
        result_node += f"  Proba Down: {self.proba_down:.3f}\n"
        result_node += f"  Option Value: {self.option_value:.2f}\n"
        return result_node
    



    # def calculate_option_value(self) -> float :
    #     #arranger calculate_option avec calculate_option_type afin de compute au bon endroit
    #     if next_node = "up":
    #         self.option_value = self.up_price
    #     elif next_node= "down":
    #         self.option_value=self.down_price
    #     elif next_node= "mid":
    #         self.option_value=self.mid_price
    #     else:
    #         raise ValueError("You may have a problem, please look")