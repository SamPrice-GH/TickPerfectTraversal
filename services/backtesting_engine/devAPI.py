from datetime import datetime, timedelta
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from BacktestDataclasses import BacktestJobConfig
from ProgressSinks import ConsoleProgressSink
from main import process_backtest_job

class BacktestRequest(BaseModel):
    job_id: str
    instrument: str
    timeframe_minutes: int
    start: datetime
    end: datetime
    strategy_name: str
    cash: float = 100_000
    commission: float = 0.0
    finalize_trades: bool = True

def serialise_stats(stats: dict) -> dict:
    out = {}
    for k, v in stats.items():
        if hasattr(v, "item"):  # numpy scalars
            out[k] = v.item()
        else:
            out[k] = v
    return out

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/backtest")
def run_backtest_endpoint(req: BacktestRequest):

    job = BacktestJobConfig(
        job_id=req.job_id,
        instrument=req.instrument,
        timeframe=timedelta(minutes=req.timeframe_minutes),
        start=req.start,
        end=req.end,
        strategy_name=req.strategy_name,
        data_root=Path("test_data"),
        cash=req.cash,
        commission=req.commission,
        finalize_trades=req.finalize_trades,
    )

    try:
        result = process_backtest_job(job, ConsoleProgressSink())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "job_id": req.job_id,
        "status": "completed",
        "stats_str": result.stats[:-3].to_json()
    }

