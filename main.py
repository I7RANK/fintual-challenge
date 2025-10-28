# Assumptions:
# - All allocated values are positive numbers > 0 <= 1 and the sum of all numbers should be 1.
# - (I don't know about shares so I think if a share have a price of 0 you can't sell or buy)
# - so in that case Negative or zero prices are not allowed.
# - Stocks cannot have negative shares.
# - Each stock in the target distribution must exist in the portfolio
#   and have a valid current price defined.

class Stock:
  name = ''
  shares = 0

  def __init__(self, name, shares):
    self.name = name
    self.shares = shares

  def current_price(self, price):
    return self.shares * price


class Portfolio:
  stocks = {}
  allocated = {}

  def __init__(self, stocks, allocated):
    self.stocks = stocks
    self.allocated = allocated

  def rebalance(self, stock_prices):
    """
    Calculate the rebalance of the portfolio based on each stock’s allocated value.
    and Print the summary

    Args:
      target_distribution (dict):
        Dictionary that defines the target price per share for each stock.
        Each key represents a stock symbol (as a string), and each value
        represents the target price (as a float or int) for that stock.

        It is assumed that all keys in this dictionary match the names of
        the stocks currently stored in the portfolio. Additionally, each
        stock must have a valid current price defined; otherwise, the
        rebalance process will fail.

        Example:
          {
            'META': 50,
            'APPL': 10,
            'GOOGLE': 20
          }
    """
    is_balanced = True
    rebalance_summary = {}
    shares_total_value = {}
    total_money = 0

    for stock in self.stocks.values():
      # Get the current price of all my shares
      money = stock.current_price(stock_prices[stock.name])
      # Save the total
      total_money += money
      # And save the value for each stock to calculate the rebalancing_factor
      shares_total_value[stock.name] = money

    for key in shares_total_value:
      # I realized that I can get the aim value only if I multiply the allocated by total money
      target_value = self.allocated[key] * total_money
      # And Also for get target_shares is just dividing the target value with the current price of 1 share
      target_shares = target_value / stock_prices[key]
      # I will save the summary to print it later
      rebalance_summary[key] = { 'stock': self.stocks[key], 'stock_price': stock_prices[key], 'target_shares': target_shares, 'target_value': target_value }
      # And I will use this variable to print a different message if the Portfolio is balanced
      if target_shares != self.stocks[key].shares:
        is_balanced = False
    
    self.__print_rebalance_summary(rebalance_summary, is_balanced)

  def __print_rebalance_summary(self, rebalanced_summary, is_balanced):
    """
    Display a formatted and colorized summary of the portfolio rebalance process.

    Args:
      rebalanced_summary (dict):
        A dictionary containing the rebalance data for each stock. Each entry
        should have the following structure:
        {
          'stock': Stock,            # Stock instance
          'stock_price': float,      # Current price per share
          'target_shares': float,    # Target number of shares
          'target_value': float      # Desired total value
        }

      is_balanced (bool):
        Indicates whether the portfolio is already balanced.
        If True, a success message is printed and the function returns early.

    Returns:
      None: This method only prints output to the console.
    """
    if is_balanced:
        print("\n🎯 Congrats!! Your Portfolio is perfectly balanced.\n")
        return

    print("\n📊 Rebalance Summary\n" + "=" * 50)

    for summary in rebalanced_summary.values():
        stock = summary['stock']
        stock_name = stock.name
        current_value = stock.current_price(summary['stock_price'])
        target_value = summary['target_value']
        # Get differences between values to get the action (Sell or Buy)
        difference = current_value - target_value

        print(f"\n🟦 {stock_name}")
        print("-" * (len(stock_name) + 4))

        if difference == 0:
            print("✅ Already balanced! No action needed.\n")
            continue

        # Determine action
        action = "Sell" if difference > 0 else "Buy"
        amount = abs(difference)
        shares = summary['target_shares']

        # I used IA to generate a beautiful format to print the message xd
        print(f"👉 You need to {action} ${amount:.2f} in shares to have {shares} total.")
        print(f"   (Current value: ${current_value:.2f} | Target: ${target_value:.2f})")

    print("\n" + "=" * 50 + "\n✅ Rebalance summary complete! ✅\n")


def test():
  meta = Stock('META', 1)
  appl = Stock('APPL', 5)
  google = Stock('GOOGLE', 10)
  portfolio = Portfolio({meta.name: meta, appl.name: appl, google.name: google}, {meta.name: 0.2, appl.name: 0.1, google.name: 0.7})
  portfolio.rebalance({meta.name: 50, appl.name: 10, google.name: 20})

def test_balanced():
  meta = Stock('META', 2)
  appl = Stock('APPL', 2)
  google = Stock('GOOGLE', 6)
  portfolio = Portfolio({meta.name: meta, appl.name: appl, google.name: google}, {meta.name: 0.2, appl.name: 0.2, google.name: 0.6})
  portfolio.rebalance({meta.name: 10, appl.name: 10, google.name: 10})

def test_zero():
  meta = Stock('META', 0)
  google = Stock('GOOGLE', 2)
  portfolio = Portfolio({meta.name: meta, google.name: google}, {meta.name: 0.5, google.name: 0.5})
  portfolio.rebalance({meta.name: 50, google.name: 50})

def test_zero2():
  meta = Stock('META', 0)
  google = Stock('GOOGLE', 2)
  portfolio = Portfolio({meta.name: meta, google.name: google}, {meta.name: 0.1, google.name: 0.9})
  portfolio.rebalance({meta.name: 1, google.name: 50})

test()
test_balanced()
test_zero()
test_zero2()
