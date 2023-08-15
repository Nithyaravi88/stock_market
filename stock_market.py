import time
import math

class Stock:
    """
    A class representing a stock.
    
    Attributes:
        stock_symbol (str): The symbol of the stock.
        stock_type (str): The type of the stock (Common or Preferred).
        last_dividend (float): The last dividend of the stock.
        fixed_dividend (float): The fixed dividend (for Preferred stocks).
        par_value (float): The par value of the stock.
        trades (list): List of trade records for the stock.
    """
    def __init__(self, stock_symbol, stock_type, last_dividend, fixed_dividend=None, par_value=0):
        """
        Initialize a Stock instance.
        
        Args:
            stock_symbol (str): The symbol of the stock.
            stock_type (str): The type of the stock (Common or Preferred).
            last_dividend (float): The last dividend of the stock.
            fixed_dividend (float, optional): The fixed dividend (for Preferred stocks). Default is None.
            par_value (float, optional): The par value of the stock. Default is 100.
        """
        self.symbol = stock_symbol
        self.stock_type = stock_type
        self.last_dividend = last_dividend
        self.fixed_dividend = fixed_dividend
        self.par_value = par_value
        self.trades = []

    #Calculate dividend yield
    def calculate_dividend_yield(self, price):
        """
        Calculate the dividend yield for the stock.

        Args:
            price (float): The current price of the stock.

        Returns:
            float: The dividend yield.
        """
        if price <= 0:
            return None
        if self.stock_type == "Common":
            return self.last_dividend / price
        elif self.stock_type == "Preferred":
            if self.fixed_dividend is None:
                return None
            return round(((self.fixed_dividend * self.par_value) / price),2)

    #Calculate PE ratio
    def calculate_pe_ratio(self, price):
        """
        Calculate the P/E ratio for the stock.

        Args:
            price (float): The current price of the stock.

        Returns:
            float: The P/E ratio.
        """
        if price <= 0:
            return None
        if self.last_dividend == 0:
            return None
        return round(price / self.last_dividend ,2)

    #Recording trade
    def record_trade(self, quantity, indicator, price):
        """
        Record a trade for the stock.

        Args:
            quantity (int): The quantity of shares traded.
            trade_type (str): 'buy' for buy trade, 'sell' for sell trade.
            price (float): The traded price of the shares.
        """
        timestamp = time.time()
        trade = {'timestamp': timestamp, 'quantity': quantity, 'indicator': indicator, 'price': price}
        print("Record a trade ", trade)
        self.trades.append(trade)

    #calculate Volume weighted Stock Price
    def calculate_volume_weighted_stock_price(self):
        """
        Calculate the volume-weighted stock price for the stock.

        Returns:
            float: The volume-weighted stock price.
        """
        now = time.time()
        total_price_quantity = 0
        total_quantity = 0
        for trade in self.trades:
            if now - trade['timestamp'] <= 15 * 60:  # Within the last 15 minutes
                total_price_quantity += trade['price'] * trade['quantity']
                total_quantity += trade['quantity']
        if total_quantity == 0:
            return None
        return round(total_price_quantity / total_quantity,2)

#calculate geometric mean
def calculate_geometric_mean(prices):
    """
    Calculate the geometric mean of a list of prices.

    Args:
        prices (list): List of prices for which to calculate the geometric mean.

    Returns:
        float: The geometric mean of prices.
    """
    if len(prices) == 0:
        return None
    product = 1
    for price in prices:
        if price <= 0:
            return None
        product *= price
    return round(math.sqrt(product),2)

# Create stock objects
tea = Stock("TEA", "Common", 0, None, 100)
pop = Stock("POP", "Common", 8, None, 100)
ale = Stock("ALE", "Common", 23, None, 60)
gin = Stock("GIN", "Preferred", 8, 0.02, 100)
joe = Stock("JOE", "Common", 13, None, 250)

# Record trades for some stocks
pop.record_trade(50, 'buy', 150)
pop.record_trade(25, 'sell', 140)
ale.record_trade(100, 'buy', 155)
gin.record_trade(75, 'buy', 200)
gin.record_trade(30, 'sell', 195)
joe.record_trade(100, 'buy', 210)

# Calculate dividend yield and P/E ratio for some stocks
price_pop = 1000
price_ale = 1700
price_gin = 1800
print(f"Dividend Yield for {pop.symbol}: {pop.calculate_dividend_yield(price_pop)}")
print(f"Dividend Yield for {ale.symbol}: {ale.calculate_dividend_yield(price_ale)}")
print(f"Dividend Yield for {gin.symbol}: {gin.calculate_dividend_yield(price_gin)}")

print(f"P/E Ratio for {pop.symbol}: {pop.calculate_pe_ratio(price_pop)}")
print(f"P/E Ratio for {ale.symbol}: {ale.calculate_pe_ratio(price_ale)}")
print(f"P/E Ratio for {gin.symbol}: {gin.calculate_pe_ratio(price_gin)}")

# Calculate volume weighted stock price for some stocks
print(f"Volume Weighted Stock Price for {pop.symbol}: {pop.calculate_volume_weighted_stock_price()}")
print(f"Volume Weighted Stock Price for {ale.symbol}: {ale.calculate_volume_weighted_stock_price()}")
print(f"Volume Weighted Stock Price for {gin.symbol}: {gin.calculate_volume_weighted_stock_price()}")

# Calculate GBCE All Share Index (Geometric Mean of prices)
all_prices = [price_pop, price_ale, price_gin, joe.calculate_volume_weighted_stock_price()]
geometric_mean = calculate_geometric_mean(all_prices)
print(f"GBCE All Share Index: {geometric_mean}")
