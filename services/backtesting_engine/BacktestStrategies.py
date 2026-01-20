from backtesting import Strategy

# TODO: figure out how we're going to store/apply/validate user inputted strategies

class BuyAndHold(Strategy):
    def init(self):
        pass

    def next(self):
        if not self.position:
            self.buy()