from pathlib import Path
from datetime import timedelta
from TickStream import TickStream
from TickResampler import TickResampler
from BarCollector import BarCollector

root = Path("services/backtesting_engine/test_data")  # contains 202405/
timeframe = timedelta(minutes=1)

tick_stream = TickStream(root)
resampler = TickResampler(timeframe)
collector = BarCollector()

for tick in tick_stream.stream():
    bar = resampler.update(tick)
    if bar is not None:
        collector.add_bar(bar)

df = collector.to_dataframe()
print(df.head())
print(df.tail())

from backtesting import Backtest, Strategy

class BuyAndHold(Strategy):
    def init(self):
        pass

    def next(self):
        if not self.position:
            self.buy()

bt = Backtest(
    df,
    BuyAndHold,
    cash=100_000,
    commission=0.0,
)

stats = bt.run()
print(stats)