from typing import Protocol
import psycopg
from enum import Enum

class BacktestJobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    RESAMPLING = "resampling"
    BACKTESTING = "backtesting"
    FINALISING = "finalising"
    COMPLETED = "completed"
    FAILED = "failed"

class BacktestProgressSink(Protocol):
    def job_started(self) -> None: ...
    def progress(self, status: BacktestJobStatus, message: str, progress_pct: float) -> None: ...
    def job_finished(self) -> None: ...
    def job_failed(self, error_message: str) -> None: ...

class ConsoleProgressSink:
    def __init__(self, job_id: str):
        self.job_id = job_id

    def job_started(self) -> None:
        print(f"[{self.job_id}] started")

    def progress(self, status: BacktestJobStatus, message: str, progress_pct: float) -> None:
        print(f"[{self.job_id}] {status}: {message} ({progress_pct:.0f}%)")
    
    def job_finished(self) -> None:
        print(f"[{self.job_id}] completed")

    def job_failed(self, error: str) -> None:
        print(f"[{self.job_id}] failed: {error}")

class PostgresProgressSink:
    def __init__(self, conn: psycopg.Connection, job_id: str):
        self.conn = conn
        self.job_id = job_id

    def job_started(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE backtest_jobs
                SET job_status = %s,
                    started_at = now(),
                    updated_at = now()
                WHERE job_id = %s
                """,
                (BacktestJobStatus.RUNNING, self.job_id)
            )
        self.conn.commit()

    def progress(self, status: BacktestJobStatus, message: str, progress_pct: float) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE backtest_jobs
                SET job_status = %s,
                    status_message = %s,
                    progress_pct = %s,
                    updated_at = now()
                WHERE job_id = %s
                """,
                (status, message, progress_pct, self.job_id)
            )
        self.conn.commit()

    def job_finished(self) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE backtest_jobs
                SET job_status = %s,
                    status_message = 'Backtest completed successfully',
                    progress_pct = 100.0,
                    finished_at = now(),
                    updated_at = now()
                WHERE job_id = %s
                """,
                (BacktestJobStatus.COMPLETED, self.job_id)
            )
        self.conn.commit()

    def job_failed(self, error_message: str) -> None:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                UPDATE backtest_jobs
                SET job_status = %s,
                    error_message = %s,
                    finished_at = now(),
                    updated_at = now()
                WHERE job_id = %s
                """,
                (BacktestJobStatus.FAILED, error_message, self.job_id)
            )
        self.conn.commit()