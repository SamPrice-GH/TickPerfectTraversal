from BacktestDataclasses import BacktestJobConfig, BacktestResult
from TickStream import TickStream
from TickResampler import TickResampler
from BarCollector import BarCollector, forward_fill_bars
from backtesting import Backtest
from BacktestStrategies import STRATEGIES
from ProgressSinks import ConsoleProgressSink, BacktestProgressSink, DatabaseProgressSink, BacktestJobStatus
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
    
    try:
      # TODO: tick stream to later be adapted to whatever data source may be, figure out how we're selecting instrument/data
      # no need to report prog here, will be instant to init data stream and will fail with stream error if issues
      tick_stream = TickStream(
          root=job.data_root,
          start=job.start,
          end=job.end,
      )
    

      # resample ticks into OHLCV bars at specified timeframe
      progress_sink.progress(BacktestJobStatus.RESAMPLING, f"Resampling ticks into {job.timeframe} OHLCV bars", 0.0)
      resampler = TickResampler(timeframe=job.timeframe)
      bar_collector = BarCollector()

      # construct bars with progress reporting
      total_span = (job.end - job.start).total_seconds()
      REPORT_ON_PCT_INCREMENTS = 0.05  # report every 5%
      last_reported_pct = 0.0

      for tick in tick_stream.stream():
                bar = resampler.update(tick)

                if bar is not None:
                    bar_collector.add_bar(bar)
                    
                    current_ts = bar.start # done on bar completion but close enough
                    resampling_prog_pct = (current_ts - job.start).total_seconds() / total_span
                    resampling_prog_pct = max(0.0, min(resampling_prog_pct, 1.0))

                    if resampling_prog_pct - last_reported_pct >= REPORT_ON_PCT_INCREMENTS:
                        last_reported_pct = resampling_prog_pct
                        progress_sink.progress(
                            status=BacktestJobStatus.RESAMPLING,
                            message=f"Resampling ticks into {job.timeframe} OHLCV bars",
                            progress_pct=resampling_prog_pct * 60.0,  # resampling is ~60% of total progress
                        )

      ohlcv_df = bar_collector.to_dataframe()
      ohlcv_df = forward_fill_bars(ohlcv_df, job.timeframe) # ensure no missing bars (strategy is responsible for handling end of day gaps, etc)

      # run backtest
      progress_sink.progress(BacktestJobStatus.BACKTESTING, "Running backtest", 60.0)
      bt_stats = run_backtest(
          dataframe=ohlcv_df,
          strategy=STRATEGIES[job.strategy_name],
          cash=job.cash,
          commission=job.commission,
          finalize_trades=job.finalize_trades
      )
    
      # TODO: upload trades and equity curve to database, S3?
      progress_sink.progress(BacktestJobStatus.FINALISING, "Finalising backtest results", 90.0)
      trades = bt_stats["_trades"]
      equity = bt_stats["_equity_curve"]
    
      # completed
      progress_sink.job_finished()

    except Exception as e:
      progress_sink.job_failed(f"Error processing backtest job:\n{e}")
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
        end=datetime(2024, 5, 10),
        strategy_name="SMACrossover",
        data_root=Path("services/backtesting_engine/test_data"),
        cash=100_000,
        commission=0.0,
        finalize_trades=True,
    )

    result = process_backtest_job(job_config, ConsoleProgressSink(job_config.job_id))
    print(f"Backtest Job ID: {result.job_id}")
    print("Statistics:")
    print(result.stats)
    print("Trades:")
    print(result.trades)
    print("Equity Curve:")
    print(result.equity_curve)