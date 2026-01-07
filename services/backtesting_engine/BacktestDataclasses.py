from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

@dataclass(frozen=True)
class BacktestJobConfig:
    job_id: str
    instrument: str
    timeframe: str              # 1min, 5min, 1h, 1d etc.
    start: datetime
    end: datetime
    strategy_name: str
    data_root: str              # local path for now
    cash: int
    commission: float
    finalize_trades: bool

@dataclass
class BacktestResult:
    job_id: str
    stats: Dict[str, Any]
    trades: Any                 # DataFrame or serialised form
    equity_curve: Any
