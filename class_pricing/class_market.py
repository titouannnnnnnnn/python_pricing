from datetime import datetime
from dataclasses import dataclass


@dataclass
class Market:
    """Construct a market object.

    Attributes:
    ----
        interest_rate (float): The interest rates in percent.
        volatility (float): The volatility in percent.
        spot_price (float): The spot price of the underlying asset in dollars.
        dividend_price (float): The dividend price in dollars.
        dividend_ex_date (datetime): The dividend ex date.
    """

    interest_rate: float
    volatility: float
    start_date: datetime
    spot_price: float
    dividend_price: float
    dividend_ex_date: datetime

    #declaration des variables dans des classes