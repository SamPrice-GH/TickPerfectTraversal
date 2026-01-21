CREATE TABLE backtest_jobs (
    job_id TEXT PRIMARY KEY,
    job_status TEXT NOT NULL,
    status_message TEXT,
    progress_pct REAL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    started_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    error_message TEXT
);

CREATE TABLE backtest_results (
    job_id TEXT PRIMARY KEY REFERENCES backtest_jobs(job_id) ON DELETE CASCADE,
    
    -- backtest params
    strategy_name TEXT NOT NULL,
    instrument TEXT NOT NULL,
    timeframe TEXT NOT NULL,
    start_ts TIMESTAMPTZ NOT NULL,
    end_ts TIMESTAMPTZ NOT NULL,
    duration INTERVAL NOT NULL,
    cash REAL NOT NULL,
    commission REAL NOT NULL,
    finalize_trades BOOLEAN NOT NULL,

    -- performance metrics
    -- exposure / equity
    exposure_pct REAL,
    equity_final REAL,
    equity_peak REAL,

    -- returns
    return_pct REAL,
    buy_hold_return_pct REAL,
    return_ann_pct REAL,
    cagr_pct REAL,

    -- risk / ratios
    volatility_ann_pct REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    calmar_ratio REAL,
    alpha_pct REAL,
    beta REAL,

    -- drawdowns
    max_drawdown_pct REAL,
    avg_drawdown_pct REAL,
    max_drawdown_duration INTERVAL,
    avg_drawdown_duration INTERVAL,

    -- trades
    trades_count INT,
    win_rate_pct REAL,
    best_trade_pct REAL,
    worst_trade_pct REAL,
    avg_trade_pct REAL,
    max_trade_duration INTERVAL,
    avg_trade_duration INTERVAL,

    -- performance quality
    profit_factor REAL,
    expectancy_pct REAL,
    sqn REAL,
    kelly_criterion REAL,


    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);