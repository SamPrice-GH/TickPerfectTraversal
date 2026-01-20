from BacktestDataclasses import BacktestJobConfig, BacktestResult
from TickStream import TickStream
from TickResampler import TickResampler
from BarCollector import BarCollector, forward_fill_bars
from backtesting import Backtest
from BacktestStrategies import BuyAndHold
from ProgressSinks import ConsoleProgressSink, BacktestProgressSink
from Exceptions import BacktestException
import pandas as pd
from datetime import datetime, timedelta


def run_backtest(dataframe, strategy, cash, commission, finalize_trades):
    try:
      bt = Backtest(
          dataframe,
          strategy,
          cash=cash,
          commission=commission,
          finalize_trades=finalize_trades
      )
      stats = bt.run()
      return stats
    except Exception as e:
      raise BacktestException(f"Error running backtest: {e}") from e

def process_backtest_job(job: BacktestJobConfig, progress_sink: BacktestProgressSink) -> BacktestResult:
    # TODO: input validation, should this be handled on frontend form submission?
    
    def report_prog(stage: str, message: str): 
        progress_sink.update(
            job_id=job.job_id,
            stage=stage,
            message=message,
        )
    
    try:
      # TODO: tick stream to later be adapted to whatever data source may be, figure out how we're selecting instrument/data
      report_prog("tick_stream_init", "Initializing tick stream")
      tick_stream = TickStream(
          root=job.data_root,
          start=job.start,
          end=job.end,
      )
    

      # resample ticks into OHLCV bars at specified timeframe
      report_prog("resampling", f"Resampling ticks into {job.timeframe} OHLCV bars")
      resampler = TickResampler(timeframe=job.timeframe)
      bar_collector = BarCollector()
      bar_collector.consume_stream(tick_stream, resampler)
      ohlcv_df = bar_collector.to_dataframe()
      ohlcv_df = forward_fill_bars(ohlcv_df, job.timeframe) # ensure no missing bars (strategy is responsible for handling end of day gaps, etc)

      # run backtest
      report_prog("backtest_run", "Running backtest")
      bt_stats = run_backtest(
          dataframe=ohlcv_df,
          strategy=BuyAndHold, # TODO: dynamic based on job.strategy_name
          cash=job.cash,
          commission=job.commission,
          finalize_trades=job.finalize_trades
      )

      trades = bt_stats["_trades"]
      equity = bt_stats["_equity_curve"]

      report_prog("complete", "Backtest complete")

    except Exception as e:
      report_prog("failed", f"Error processing backtest job:\n{e}")
      raise e

    return BacktestResult(
        job_id=job.job_id,
        stats=bt_stats[:-2],  # exclude _trades and _equity_curve from stats
        trades=trades,
        equity_curve=equity,
    )


if __name__ == "__main__":
    # simple test run, config will later be generated from job payload
    from datetime import datetime, timedelta
    from pathlib import Path

    job_config = BacktestJobConfig(
        job_id="test_job_001",
        instrument="NQ", # ignored for now
        timeframe=timedelta(minutes=(1)),
        start=datetime(2024, 5, 1),
        end=datetime(2024, 5, 31),
        strategy_name="BuyAndHold", # ignored for now
        data_root=Path("services/backtesting_engine/test_data"),
        cash=100_000,
        commission=0.0,
        finalize_trades=True,
    )

    result = process_backtest_job(job_config, ConsoleProgressSink())
    print(f"Backtest Job ID: {result.job_id}")
    print("Statistics:")
    print(result.stats)
    print("Trades:")
    print(result.trades)
    print("Equity Curve:")
    print(result.equity_curve)