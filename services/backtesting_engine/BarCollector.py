from datetime import timedelta
import pandas as pd
from TickResampler import TickResampler, OHLCVBar
from TickStream import TickStream
from Exceptions import BarCollectorException

class BarCollector:
    def __init__(self):
        self.rows: list[OHLCVBar] = []

    def consume_stream(self, tick_stream: TickStream, resampler: TickResampler):
        try:
            for tick in tick_stream.stream():
                bar = resampler.update(tick)
                if bar is not None:
                    self.add_bar(bar)
        except Exception as e:
            raise BarCollectorException(f"Error consuming tick data in BarCollector: {e}") from e
        
    # might want to construct dummy test data, expose this method
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
        try:
            df = pd.DataFrame(self.rows)
            df.set_index("Timestamp", inplace=True)
            df.sort_index(inplace=True)
            return df
        except Exception as e:
            raise BarCollectorException(f"Error converting BarCollector to DataFrame: {e}") from e
        
def forward_fill_bars(ohlcv: pd.DataFrame, timeframe: timedelta) -> pd.DataFrame:
    try:
        if ohlcv.empty:
            return ohlcv

        start = ohlcv.index[0]
        end = ohlcv.index[-1]

        full_index = pd.date_range(
            start=start,
            end=end,
            freq=pd.Timedelta(timeframe),
        )

        ohlcv = ohlcv.reindex(full_index)

        # forward fill price columns
        ohlcv[["Open", "High", "Low", "Close"]] = (
            ohlcv[["Open", "High", "Low", "Close"]].ffill()
        )

        # missing volume means synthetic bar
        ohlcv["Volume"] = ohlcv["Volume"].fillna(0).astype(int)

        return ohlcv
    except Exception as e:
        raise BarCollectorException(f"Error during forward filling of bars: {e}") from e
