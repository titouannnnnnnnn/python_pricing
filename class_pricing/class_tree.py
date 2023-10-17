from datetime import datetime as dt
from class_pricing.class_option import Option
from class_pricing.class_market import Market
from class_pricing.class_node import Node
import datetime
from datetime import timedelta
from math import sqrt, exp
#from class_pricing.function import calculate_alpha, calculate_delta_t


class Tree:

    nb_days=365


    def __init__(
    self,
    market:Market, 
    option:Option,
    pricing_date : datetime, 
    nb_steps : int
    ):
        
        self.market = market
        self.option = option
        self.pricing_date = pricing_date
        self.nb_steps = nb_steps
        
        self.delta_t = self.calculate_delta_t()
        #self.delta_t = self.calculate_bis_delta_t()
        self.alpha = self.calculate_alpha()
        #self.alpha = self.calculate_bis_alpha()

        #self.parent = None

        # if self.pricing_date>self.option.maturity_date:
        #     raise ValueError("Pricing date must be before the maturity date")
        # else:
        #     self.delta_t = calculate_delta_t(self.option.maturity_date, self.pricing_date, self.nb_steps, self.nb_days)
        #     #=((maturity_date-pricing_date)/nb_steps)/365
        #     #why 365 ? to have the number in year, i.e x/365
        #     self.alpha = calculate_alpha(self.market.volatility, self.delta_t, sqrt(3))


        self.root=Node(self.market,self,self.market.spot_price)
        #point de depart = root

        self.build_tree(self)

    # def calculate_delta_t(maturity_date:datetime, pricing_date:datetime,nb_steps:int, nb_days:int) -> float:
    #     return ((maturity_date - pricing_date).days / nb_steps) / nb_days
    
    def calculate_delta_t(self):
        return (self.option.maturity_date - self.pricing_date).days /self.nb_steps / self.nb_days

    def calculate_alpha(self) -> float:
         return exp (self.market.volatility * sqrt (3* self.delta_t))
    

    # def calculate_bis_delta_t(self) -> float: #a regarder
    #     delta_timedelta = self.option.maturity_date - self.pricing_date
    #     delta_days = float(delta_timedelta.days)
    #     return (delta_days / self.nb_steps )/ self.nb_days
    #     #return ((self.option.maturity_date - self.pricing_date).days/self.nb_steps) / self.nb_days

    # def calculate_bis_alpha(self) -> float : #a regarder
    #     return exp(self.market.volatility  * sqrt (3 * self.delta_t))

    def build_tree(self):
        n=self.root #current node
        for i in range(self.nb_steps): #construit avec la boucle for le nb de noeud et donc le nb de root de 0 a T
            n=self.build_node_column(n) #pour chaque noeud, il faut construire les noeud du bas => def build_node_column
        #dividende ? car pas le n steps dans node

    def build_node_column(self,n : Node)-> Node:
        next_node= Node(self.market, self,n.forward_price)

        n.build_block(next_node)
        n1 = n
        while n1.down_node is not None: #tant que le noeud down != 0 donc jusq'a qu'il y ait un noeud a executer
            n1=n1.down_node #on affecte a n1 le noeud down
            n1.build_block(next_node) 
            #a partir du noeud down(n1 donc) on construit les 3 prochains=es branches4

        #on fait la meme pour l'etat up
        n2 = n
        while n2.up_node is not None:
            n2=n2.up_node
            n2.build_block(next_node)

        #return self.next_mid

    # def build_node_column(self, n: Node) -> Node:
        
    #     next_node = Node(self.market, self, n.forward_price)
        
    #     if n.down_node is None:
    #         ndown = Node(self.market, self, n.spot_price / self.alpha)
    #         ndown.up_node = n
    #         n.down_node = ndown
    #     else:
    #         ndown = n.down_node
        
    #     if n.up_node is None:
    #         nup = Node(self.market, self, n.spot_price * self.alpha)
    #         nup.down_node = n
    #         n.up_node = nup
    #     else:
    #         nup = n.up_node
        
    #     self.next_mid = n
    
    #     return next_node
 
    
    # #construction des noeuds et des connections
    # def build_block(self,next : Node):
    #     nmid=self.get_mid(next)
    #     if nmid.down_node is None:
    #         ndown=Node(self.market,self,nmid.spot_price/self.alpha)
    #         ndown.up_node=nmid
    #         nmid.down_node=ndown
    #     else:
    #         ndown=nmid.down_node
    #     if nmid.up_node is None:
    #         nup=Node(self.market,self,nmid.spot_price*self.alpha)
    #         nup.down_node=nmid
    #         nmid.up_node=nup
    #     else:
    #         nup=nmid.up_node

    #     #self.tree.next_mid=nmid
    #     self.next_mid = nmid


    # def is_close(self,forward) -> bool:
    #     return self.spot_price * (1+1/self.alpha)/2 <= forward <= self.spot_price * (1+self.tree.alpha)/2


    # def get_mid(self,next:Node):
    #     forward= calculate_forward_price(self.market.spot_price, self.market.interest_rate, self.delta_t)
    #     if next.is_close(forward): #regarder si None ou pas, avec debeuguuer
    #         return next
    #     elif forward > self.market.spot_price:
    #         while not next.is_close(forward):
    #             next=next.move_up()
    #     else :
    #         while not next.is_close(forward):
    #             next=next.move_down()
    #     return next 
    

    # def move_up(self)-> Node:
    #     if self.up_node is None:
    #         nup=
    #     else:
    #         nup=
    

    

    # def move_down(self) -> Node:
    #     if self.down_node is None:
    #         ndown=
    #     else:
    #         ndown=self


    


    def print_tree(self, node=None, depth=0):
        if node is None:
            node = self.root

        if node:
            print("  " * depth + str(node))
            self.print_tree(node.down_node, depth + 1)
            self.print_tree(node.mid_node, depth + 1)
            self.print_tree(node.up_node, depth + 1)

    

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


    
    # def build_next_gen(self,current_node):
    #     self.up_price = current_node.spot_price * self.tree.alpha
    #     self.down_price = current_node.spot_price / self.tree.alpha
    #     self.mid_price = current_node.forward_price
    #     return Node(self.market,self,)
    
    # def move_up(self,current_node):
    #     while current_node.get_mid() is None:
    #         current_node = current_node.parent
    #     return current_node.get_mid()
    
    # def connect_node(self, next_node):
    #     self.next_up = next_node.up
    #     self.next_down = next_node.down
    #     self.next_mid = next_node
    #     next_node.parent = self

    # def get_mid(self):
    #     if self.next_mid is None:
    #         return None
    #     return self.next_mid


        
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


'''
pricing amercain - pricing europeen >0
tester avec des rates < 0
'''