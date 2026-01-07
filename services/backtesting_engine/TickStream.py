from pathlib import Path
import csv
from datetime import datetime, timedelta
from typing import Iterator, Dict


Tick = Dict[str, object]

class TickStream:
    def __init__(self, root, start=None, end=None):
        self.root = root
        self.start = start
        self.end = end

    def _iter_files(self):
      for month_dir in sorted(self.root.iterdir()):
          month = int(month_dir.name)
          if self.start and month < int(self.start.strftime("%Y%m")):
              continue
          if self.end and month > int(self.end.strftime("%Y%m")):
              continue

          for csv_file in sorted(month_dir.glob("*.Last.csv")):
              file_dt = datetime.strptime(
                  csv_file.stem.split(".")[0],
                  "%Y%m%d%H%M"
              )

              if self.start and file_dt + timedelta(hours=1) <= self.start:
                  continue
              if self.end and file_dt > self.end:
                  continue

              yield csv_file

    def stream(self):
        for file_path in self._iter_files():
            with file_path.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ts = datetime.fromisoformat(row["Timestamp"])

                    if self.start and ts < self.start:
                        continue
                    if self.end and ts >= self.end:
                        continue
                    
                    yield {
                        "timestamp": datetime.fromisoformat(row["Timestamp"]),
                        "last": float(row["Last"]),
                        "bid": float(row["Bid"]),
                        "ask": float(row["Ask"]),
                        "volume": int(row["Volume"]),
                    }

