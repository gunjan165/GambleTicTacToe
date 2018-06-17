class Player():

    def __init__(self, name,symbol):
        self.name = name
        self.coins_left = 100
        self.power_used = False
        self.last_bet = None
        self.symbol = symbol

    def get_coins_left(self):
        return str(self.coins_left)

    def bet_coins(self, bet_value):
        self.coins_left -= bet_value

    def use_power(self):
        self.power_used =True


