
class Player:
    def __init__(self, money=5000):
        self.money = money

    def make_bet(self, value):
        self.money -= value
        if self.money < 0:
            raise ValueError("У вас недостаточно денег")
        else:
            return value


