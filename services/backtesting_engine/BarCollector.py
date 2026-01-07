import pandas as pd
from TickResampler import TickResampler, OHLCVBar
from TickStream import TickStream

class BarCollector:
    def __init__(self):
        self.rows: list[OHLCVBar] = []

    def consume_stream(self, tick_stream: TickStream, resampler: TickResampler):
        for tick in tick_stream.stream():
            bar = resampler.update(tick)
            if bar is not None:
                self.add_bar(bar)

    # might want to make test data, expose this method
    def add_bar(self, bar):
        self.rows.append({
            "Timestamp": bar.start,
            "Open": bar.open,
            "High": bar.high,
            "Low": bar.low,
            "Close": bar.close,
            "Volume": bar.volume,
        })

    def to_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame(self.rows)
        df.set_index("Timestamp", inplace=True)
        df.sort_index(inplace=True)
        return df
