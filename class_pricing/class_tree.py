from datetime import datetime
from dataclasses import dataclass
from class_pricing.class_option import Option
from class_pricing.class_market import Market
from class_pricing.class_node import Node
import numpy as np
from datetime import timedelta
import datetime
from scipy.stats import norm
from math import exp, sqrt, log
from class_pricing.function import calculate_alpha, calculate_delta_t


class Tree:
    nb_days=365


    def __init__(self,
    market:Market, 
    option:Option, 
    pricing_date : datetime, 
    nb_steps : int
    ):
        
        self.option = option
        self.market = market
        self.nb_steps = nb_steps
        self.pricing_date = pricing_date
        self.root=Node(self,self.market.spot_price)

        self.parent = None

        if pricing_date>self.option.maturity_date:
            raise ValueError("Pricing date must be before the maturity date")
        else:
            self.delta_t = calculate_delta_t(self.option.maturity_date, self.pricing_date, self.nb_steps, self.nb_days)
            #=((maturity_date-pricing_date)/nb_steps)/365
            #why 365 ? to have the number in year, i.e x/365

        self.alpha = calculate_alpha(self.market.volatility, self.delta_t, sqrt(3))

        self.build_tree()


    def build_tree(self):
        current_node=self.root
        for i in range(self.nb_steps):
            current_node=self.build_node_column(current_node)

    def build_node_column(self,current_node)-> Node:
        next_node= Node()
        # next_node = self.build_next_gen(current_node)
        # if current_node.get_mid()is not None:
        #     current_node.connect_node(next_node)
        #     current_node=self.move_up(current_node)
        # return current_node
    
    def build_next_gen(self,current_node):
        self.up_price = current_node.spot_price * self.tree.alpha
        self.down_price = current_node.spot_price / self.tree.alpha
        self.mid_price = current_node.forward_price
        return Node(self.market,self,)
    
    def move_up(self,current_node):
        while current_node.get_mid() is None:
            current_node = current_node.parent
        return current_node.get_mid()
    
    def connect_node(self, next_node):
        self.next_up = next_node.up
        self.next_down = next_node.down
        self.next_mid = next_node
        next_node.parent = self

    def get_mid(self):
        if self.next_mid is None:
            return None
        return self.next_mid
    

    def __str__(self) -> str:
        result_tree = "Trinomial tree class -\n"
        result_tree += f"  Steps: {self.nb_steps}\n"
        result_tree += f"  Delta_t: {self.delta_t:.4f}\n"
        result_tree += f"  Alpha: {self.alpha:.4f}\n"
        result_tree += f"  Root: {self.root}\n"
        return result_tree

    # def build_block(self, n1:Node, next:Node):
    #     fwd = self.forwar
    #     nmid = self.getmid( next, fwd)
    #     if nmid.down_node is None:
    #         ndown = Node( nmid.spot / self.alpha)
    #     else:
    #         ndown = nmid.down_node
    #     if nmid.up_node is None:
    #         nup = Node( nmid.spot * self.alpha)
    #         nup.down_node = nmid
    #         nmid.up_node = nup
    #     else:
    #         nup = mid.up_node

    #     self.next_mid = n_mid

    # def move_up(self, node:Node):
    #      if node.up is not None:  
    #         return node.up 
    #     else:
    #         return node

    # def get_mid(self, next:Node ) -> Node:
    #     if next.is_close(self.node.forward_price):
    #         return next
    #     elif self.node.forward_price > self.market.spot:
    #         while not next.is_close(self.node.forward_price):
    #             next = next.move_up()
    #     else:
    #         while not next.is_close(self.node.forward_price):
    #             next = next.move_down()
    #     return next
    
    # def is_close (self, node1=Node, node2=Node) -> bool:
	#     if node1.up == node2 or node1.down == node2 or \
    #     node2.up == node1 or node2.down == node1:
    #         return True
    #     else:
    #         return False


        
'''
1) root = prix spot : premier point en t=0
2) next_gen : root permet de créer 3 noeuds sur période suivant 
   (down, mid, up)
3) connect_node : connecte up et down avec mid
4) ensuite on va sur le prochain next_mid, qui va alors construire 
   next_gen (voir etape1), boucle for qui avance sur la longueur
5) probleme arrive, des prix vont etre en commun des que t=2, 
   il faut alors voir voir si mid a up et down avec l'aide d'une boucle 
   while qui va verifier sur la largeur des noeuds
6) verifier que tout marche


otption_value
           -  
        -  -
     -  -  -
  -  -  -  -
- -  -  -  -
  -  -  -  -
     -  -  -
        -  -
           -   
           

'''


# def __str__(self) -> str:
#     result_tree = "Trinomial tree class -\n"
#     result_tree += f"  Steps: {self.nb_steps}\n"
#     result_tree += f"  Delta_t: {self.delta_t:.4f}\n"
#     result_tree += f"  Alpha: {self.alpha:.4f}\n"
#     result_tree += f"  Root: {self.root}\n"
#     return result_tree


    # Def get_mid( next:Node ) -> Node:
	# Fwd = self.forward()
	# If next.is_close(fwd):
	# 	Return next
	# Elif fwd > self.spot:
	# 	While not next.is_close(fwd):
	# 		next = next.move_up()
	# else:
	# 	while not next.is_close(fwd):
	# 		next = next.move_down()
	# return next