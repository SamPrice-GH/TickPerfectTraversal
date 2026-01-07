import pandas as pd

class BarCollector:
    def __init__(self):
        self.rows = []

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
