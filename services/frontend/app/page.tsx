export default function BacktestPage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_BASE_URL

  return (
    <div className="h-full">
      {/* panel split */}
      <div className="flex h-full gap-3">
        {/* left column, trade stats + charts */}
        <div className="w-2/3 flex flex-col gap-3">
          <section
            aria-label="Trade statistics panel"
            className="flex-1 overflow-hidden rounded-md bg-card p-3"
          >
            <h2 className="text-lg font-semibold">Trade Stats (placeholder)</h2>
            <p className="text-sm text-muted-foreground mt-2">
              Placeholder area for trade statistics throughout the backtest (win
              rate, PnL, max drawdown, trade count etc.).
            </p>
          </section>

          <section
            aria-label="Charts panel"
            className="flex-1 overflow-hidden rounded-md bg-card p-3"
          >
            <h2 className="text-lg font-semibold">Charts (placeholder)</h2>
            <p className="text-sm text-muted-foreground mt-2">
              Placeholder area for equity curve, historical candlestick chart,
              and other visualizations.
            </p>
          </section>
        </div>

        {/* right, backtest config */}
        <aside
          aria-label="Backtest configuration"
          className="w-1/3 overflow-auto rounded-md bg-card p-3"
        >
          <h2 className="text-lg font-semibold">Configuration</h2>
          <p className="text-sm text-muted-foreground mt-2">
            Placeholder area for selecting strategy, instrument, and strategy
            parameters.
          </p>
        </aside>
      </div>
    </div>
  )
}
