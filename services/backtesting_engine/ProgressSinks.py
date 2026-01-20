from typing import Protocol

class BacktestProgressSink(Protocol):
    def update(
        self,
        job_id: str,
        stage: str,
        message: str,
        progress: float | None = None, #TODO: figure out how we're measuring progress
    ) -> None:
        ...

class ConsoleProgressSink(BacktestProgressSink):
    def update(self, job_id, stage, message, progress=None):
        print(f"[{job_id}] {stage}: {message}")

#TODO: implement database progress sink