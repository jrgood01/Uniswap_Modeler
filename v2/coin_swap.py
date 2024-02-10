from matplotlib import pyplot as plt

class CoinSwapModeler:
    def __init__(self, total_liquidity_x, total_liquidity_y, currency_x, currency_y, fee=.003):
        self.fee = fee

        self.currency_x = currency_x
        self.currency_y = currency_y

        self.total_liquidity_x = total_liquidity_x
        self.total_liquidity_y = total_liquidity_y

    def get_k(self):
        return self.total_liquidity_x * self.total_liquidity_y
    
    def place_order(self, order):
        if order['type'] == f'buy_{self.currency_x}_sell_{self.currency_y}':
            price_with_fee = self.price_x_in_y(order[f'amount_{self.currency_x}']) * (1 + self.fee)
            ammount_out = order[f'amount_{self.currency_x}'] * (1 - self.fee)
            
            self.total_liquidity_x -= order[f'amount_{self.currency_x}'] * (1 - self.fee)
            self.total_liquidity_y += price_with_fee
            return ammount_out
        
        elif order['type'] == f'sell_{self.currency_x}_buy_{self.currency_y}':
            price_with_fee = self.price_y_in_x(order[f'amount_{self.currency_y}']) * (1 + self.fee)
            ammount_out = order[f'amount_{self.currency_y}'] * (1 - self.fee)
            
            self.total_liquidity_x += price_with_fee
            self.total_liquidity_y -= order[f'amount_{self.currency_y}'] * (1 - self.fee)
            
            return {
                f'recieved_{self.currency_x}': ammount_out,
                f'new_price_{self.currency_y}_in_{self.currency_x}': self.price_y_in_x(1),
            }
        
        else: 
            raise ValueError(f'''Invalid order type. Valid types are:
                             - buy_{self.currency_x}_sell_{self.currency_y}
                             - sell_{self.currency_x}_buy_{self.currency_y}''')
        
        self.k = self.total_liquidity_x * self.total_liquidity_y
    def price_x_in_y(self, x_in):
        return self.total_liquidity_y / self.total_liquidity_x * x_in
    
    def price_y_in_x(self, y_in):
        return self.total_liquidity_x / self.total_liquidity_y * y_in
    
    def plot_price_curve(self, operations=None):
        x = range(1, int(self.total_liquidity_x * 2))
        y = [self.get_k() / x_i for x_i in x]

        plt.figure(figsize=(20, 12))
        plt.plot(x, y, label='Price Curve')
        
        plt.axvline(x=self.total_liquidity_x, color='gray', linestyle='--')
        plt.axhline(y=self.total_liquidity_y, color='gray', linestyle='--')

        plt.xlabel(self.currency_x)
        plt.ylabel(self.currency_y)
        plt.title('Price Curve')
        plt.legend()
        plt.show()
    
    
