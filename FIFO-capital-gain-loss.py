# Summary: This script computes capital gain/loss for a series of buy/sell transactions
#          using the FIFO protocol. The solution uses an optimized approach to handle shares.

class StockTransaction:
    def __init__(self):
        """Initialize an empty list to hold shares as (quantity, price)."""
        self.shares = []  # FIFO queue for shares

    def buy(self, quantity, price):
        """Add shares to the queue."""
        self.shares.append((quantity, price))

    def sell(self, quantity, price):
        """
        Sell shares using FIFO and calculate the capital gain/loss.
        Args:
        quantity (int): Number of shares to sell.
        price (int): Selling price per share.

        Returns:
        int: Capital gain or loss for this transaction.
        """
        capital_gain = 0
        while quantity > 0:
            old_quantity, old_price = self.shares[0]  # Access the oldest shares
            if old_quantity <= quantity:
                # Sell all shares from this batch
                capital_gain += old_quantity * (price - old_price)
                quantity -= old_quantity
                self.shares.pop(0)  # Remove the batch
            else:
                # Partially sell shares from this batch
                capital_gain += quantity * (price - old_price)
                self.shares[0] = (old_quantity - quantity, old_price)  # Update batch
                quantity = 0
        return capital_gain

def process_transactions(transactions):
    """
    Processes a list of transactions and computes the total capital gain or loss.
    Args:
    transactions (list): List of strings, each representing a transaction.

    Returns:
    int: Total capital gain or loss.
    """
    stock = StockTransaction()
    total_capital_gain = 0

    for transaction in transactions:
        # Parse the transaction details
        action, quantity, price = transaction.split()[0], int(transaction.split()[1]), int(transaction.split()[-2][1:])
        if action == "buy":
            stock.buy(quantity, price)
        elif action == "sell":
            total_capital_gain += stock.sell(quantity, price)
        else:
            raise ValueError(f"Unknown transaction type: {action}")

    return total_capital_gain

# Driver code
if __name__ == "__main__":
    # Example 1
    transactions1 = [
        "buy 100 shares at $20 each",
        "buy 20 shares at $24 each",
        "buy 200 shares at $36 each",
        "sell 150 shares at $30 each"
    ]
    print(f"${process_transactions(transactions1)}")  # Output: $940

    # Example 2
    transactions2 = [
        "buy 10 shares at $20 each",
        "buy 20 shares at $34 each",
        "sell 25 shares at $40 each",
        "buy 100 shares at $50 each",
        "sell 85 shares at $45 each"
    ]
    print(f"${process_transactions(transactions2)}")  # Output: $-55
