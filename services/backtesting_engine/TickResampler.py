from datetime import datetime, timedelta
from typing import Optional, Iterator

from Exceptions import TickResamplerException


class OHLCVBar:
    def __init__(self, start):
        self.start = start
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.volume = 0

    def update(self, price, volume):
        if self.open is None:
            self.open = self.high = self.low = self.close = price
        else:
            self.high = max(self.high, price)
            self.low = min(self.low, price)
            self.close = price
        self.volume += volume


class TickResampler:
    def __init__(self, timeframe: timedelta):
        self.timeframe = timeframe
        self.current_bar: Optional[OHLCVBar] = None
        self.current_start = None

    def _bar_start(self, ts):
        seconds = int(self.timeframe.total_seconds())
        epoch = int(ts.timestamp())
        return datetime.fromtimestamp(epoch - (epoch % seconds))

    def update(self, tick) -> Optional[OHLCVBar]:
        try:
            ts = tick["timestamp"]
            price = tick["last"]
            volume = tick["volume"]

            bar_start = self._bar_start(ts)

            if self.current_bar is None:
                self.current_start = bar_start
                self.current_bar = OHLCVBar(bar_start)

            if bar_start != self.current_start:
                completed = self.current_bar
                self.current_start = bar_start
                self.current_bar = OHLCVBar(bar_start)
                self.current_bar.update(price, volume)
                return completed

            self.current_bar.update(price, volume)
            return None
        except Exception as e:
            raise TickResamplerException(f"Error during tick resampling: {e}") from e
