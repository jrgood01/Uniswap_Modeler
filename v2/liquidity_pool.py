from matplotlib import pyplot as plt

class LiquidityPoolModeler:
    def __init__(self, total_liquidity_x, total_liquidity_y):
        self.total_liquidity_x = total_liquidity_x
        self.total_liquidity_y = total_liquidity_y
        
        self.k = total_liquidity_x * total_liquidity_y
    
    def buy_x_sell_y(self, x_in):
        new_x = self.total_liquidity_x + x_in
        new_y = self.k / new_x
        return new_x, new_y
    
    def buy_y_sell_x(self, y_in):
        new_y = self.total_liquidity_y + y_in
        new_x = self.k / new_y
        return new_x, new_y
    
    def price_x_in_y(self, x_in):
        return self.total_liquidity_y / self.total_liquidity_x * x_in
    
    def price_y_in_x(self, y_in):
        return self.total_liquidity_x / self.total_liquidity_y * y_in
    
    def plot_price_curve(self, operations=[]):
        x = range(1, int(self.total_liquidity_x * 2))
        y = [self.k / x_i for x_i in x]

        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label='Price Curve')
        
        for op in operations:
            if op['type'] == 'buy_x_sell_y':
                new_x, new_y = self.buy_x_sell_y(op['amount'])
            elif op['type'] == 'buy_y_sell_x':
                new_x, new_y = self.buy_y_sell_x(op['amount'])
            plt.plot([self.total_liquidity_x, new_x], [self.total_liquidity_y, new_y], 'ro-')
            plt.axvline(x=new_x, color='gray', linestyle='--')
            plt.axhline(y=new_y, color='gray', linestyle='--')
            print(f"Operation: {op['type']} with {op['amount']} units results in new X = {new_x}, new Y = {new_y}")
            
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Price Curve with Transactions')
        plt.legend()
        plt.show()
    
    def simulate_transaction(self, type_, amount):
        if type_ == 'buy_x_sell_y':
            initial_x, initial_y = self.total_liquidity_x, self.total_liquidity_y
            new_x, new_y = self.buy_x_sell_y(amount)
        elif type_ == 'buy_y_sell_x':
            initial_x, initial_y = self.total_liquidity_x, self.total_liquidity_y
            new_x, new_y = self.buy_y_sell_x(amount)
        
        print(f"Before transaction: X = {initial_x}, Y = {initial_y}")
        print(f"After transaction: X = {new_x}, Y = {new_y}")
        print(f"Difference: ΔX = {new_x - initial_x}, ΔY = {new_y - initial_y}")
