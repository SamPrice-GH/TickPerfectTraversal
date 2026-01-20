from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any

@dataclass(frozen=True)
class BacktestJobConfig:
    job_id: str
    instrument: str
    timeframe: timedelta              # 1min, 5min, 1h, 1d etc.
    start: datetime
    end: datetime
    strategy_name: str
    data_root: Path              # local path for now
    cash: int
    commission: float
    finalize_trades: bool

@dataclass
class BacktestResult:
    job_id: str
    stats: Dict[str, Any]
    trades: Any                 # DataFrame or serialised form
    equity_curve: Any
