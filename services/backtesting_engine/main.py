from BacktestDataclasses import BacktestJobConfig, BacktestResult
from TickStream import TickStream
from TickResampler import TickResampler
from BarCollector import BarCollector
from backtesting import Backtest
from BacktestStrategies import BuyAndHold
from ProgressSinks import ConsoleProgressSink, BacktestProgressSink

def run_backtest(job: BacktestJobConfig, progress_sink: BacktestProgressSink) -> BacktestResult:

    # TODO: inner functions should raise stage specific exceptions so this entire block can be wrapped in one try/except
    def report_prog(stage: str, message: str): 
        progress_sink.update(
            job_id=job.job_id,
            stage=stage,
            message=message,
        )
    
    # TODO: tick stream to later be adapted to whatever data source may be, figure out how we're selecting instrument/data
    try:
      report_prog("tick_stream_init", "Initializing tick stream")
      tick_stream = TickStream(
          root=job.data_root,
          start=job.start,
          end=job.end,
      )
    except Exception as e:
      report_prog("failed", f"Error initializing tick stream: {e}")
      raise e

    # resample ticks into OHLCV bars at specified timeframe
    try:
      report_prog("resampling", f"Resampling ticks into {job.timeframe} OHLCV bars")
      resampler = TickResampler(timeframe=job.timeframe)
      bar_collector = BarCollector()
      bar_collector.consume_stream(tick_stream, resampler)
      ohlcv_df = bar_collector.to_dataframe()
    except Exception as e:
      report_prog("failed", f"Error during resampling: {e}")
      raise e

    # run backtest
    try:
      report_prog("backtest_run", "Running backtest")
      bt = Backtest(
          ohlcv_df,
          BuyAndHold, # TODO: dynamic based on job.strategy_name
          cash=job.cash,
          commission=job.commission,
          finalize_trades=job.finalize_trades
      )

      stats = bt.run()
      trades = stats["_trades"]
      equity = stats["_equity_curve"]
    except Exception as e:
      report_prog("failed", f"Error running backtest: {e}")
      raise e

    
    report_prog("complete", "Backtest complete")

    return BacktestResult(
        job_id=job.job_id,
        stats=stats[:-2],  # exclude _trades and _equity_curve from stats dict
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
        timeframe=timedelta(minutes=1),
        start=datetime(2024, 5, 1),
        end=datetime(2024, 5, 10),
        strategy_name="BuyAndHold", # ignored for now
        data_root=Path("services/backtesting_engine/test_data"),
        cash=100_000,
        commission=0.0,
        finalize_trades=True,
    )

    result = run_backtest(job_config, ConsoleProgressSink())
    print(f"Backtest Job ID: {result.job_id}")
    print("Statistics:")
    print(result.stats)
    print("Trades:")
    print(result.trades)
    print("Equity Curve:")
    print(result.equity_curve)