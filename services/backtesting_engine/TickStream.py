from pathlib import Path
import csv
from datetime import datetime, timedelta
from typing import Iterator, Dict

from Exceptions import TickStreamException


Tick = Dict[str, object]

class TickStream:
    def __init__(self, root, start=None, end=None, max_initial_gap_days=3):
        self.root = root
        self.start = start
        self.end = end
        self.max_initial_gap_days = timedelta(days=max_initial_gap_days) # this is sort of arbitrary for now, 3 wont trigger over most weekends

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
        try:
            first_file_timestamp = None
            last_file_timestamp = None

            for file_path in self._iter_files():
                with file_path.open() as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        ts = datetime.fromisoformat(row["Timestamp"])

                        if self.start and ts < self.start:
                            continue
                        if self.end and ts >= self.end:
                            continue
                        
                        if first_file_timestamp is None: 
                            first_file_timestamp = ts
                            if first_file_timestamp - self.start > self.max_initial_gap_days:
                                raise TickStreamException(f"No data available from start time {self.start}, first available tick is at {first_file_timestamp}")
                        
                        last_file_timestamp = ts

                        yield {
                            "timestamp": datetime.fromisoformat(row["Timestamp"]),
                            "last": float(row["Last"]),
                            "bid": float(row["Bid"]),
                            "ask": float(row["Ask"]),
                            "volume": int(row["Volume"]),
                        }

            if self.end - last_file_timestamp > self.max_initial_gap_days:
                raise TickStreamException(f"No data available up to end time {self.end}, last available tick is at {last_file_timestamp}")
            
        except Exception as e:
            raise TickStreamException(f"Error reading tick data: {e}") from e

