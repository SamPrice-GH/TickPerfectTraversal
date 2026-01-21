from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import SMA

# TODO: figure out how we're going to store/apply/validate user inputted strategies

class BuyAndHold(Strategy):
    def init(self):
        pass

    def next(self):
        if not self.position:
            self.buy()

class SMACrossover(Strategy):
    fast_period = 10
    slow_period = 30

    def init(self):
        close = self.data.Close
        self.sma_fast = self.I(SMA, close, self.fast_period)
        self.sma_slow = self.I(SMA, close, self.slow_period)

    def next(self):
        if crossover(self.sma_fast, self.sma_slow):
            self.position.close()
            self.buy()

        elif crossover(self.sma_slow, self.sma_fast):
            self.position.close()
            self.sell()

STRATEGIES = {
    "BuyAndHold": BuyAndHold,
    "SMACrossover": SMACrossover,
}