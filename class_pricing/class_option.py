from dataclasses import dataclass
from datetime import datetime
from typing import Literal


@dataclass
class Option:
    """Construct an option object
    Attributes:
    ----
        option_type (Literal[&quot;call&quot;, &quot;put&quot;]): The type of the option call or put.
        exercise_type (Literal[&quot;am&quot;, &quot;eu&quot;]): The type of the exercise american or european.
        strike_price (float): The strike price of the option.
        maturity_date (datetime): The maturity date of the option.
    """

    option_type: Literal["call", "put"] #string de valeurs
    exercise_type: Literal["am", "eu"] #string de valeurs
    strike_price: float
    maturity_date: datetime

    def payoff(self,spot) -> float:
        if self.option_type== "call":
            return max(0 , spot - self.strike_price)
        elif self.option_type == "put":
            return max (0 , self.strike_price - spot)
        else:
            raise ValueError("Wrong input, please be careful, insert call or put")

    #class option avec :
    # - type opyion
    # - type exercise
    # - strike
    # - maturity date