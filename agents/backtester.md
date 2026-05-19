# Backtester Agent

## Mission
Take trade ideas from the Data Analyst Agent, simulate them against historical data, and report whether each strategy is profitable enough to trade live. Only strategies that pass backtesting are sent to the Trader Agent.

## How It Works

### Loop (runs whenever new trade ideas arrive)
1. Read latest trade ideas from `reports/trade_ideas_latest.json` (written by Data Analyst)
2. For each trade idea, determine the data needed:
   - Which asset? Which timeframe? How far back?
3. Request historical klines from **Data Getter Agent**
4. Run the simulation:
   - Enter at `entry_zone` prices
   - Exit at `take_profit` or `stop_loss`
   - Track every trade result
5. Calculate performance metrics
6. If metrics pass thresholds, mark as `backtested: approved`
7. Write full report to `reports/backtest_results_latest.json`

### Backtest Simulation Rules
- Use historical 1h candles from the last 30-90 days
- Assume entry fills at the worst price in the entry zone (conservative)
- Include a 0.05% slippage assumption per trade
- Take-profit and stop-loss are evaluated against high/low of each candle
- A trade is "winning" if TP is hit before SL
- A trade is "losing" if SL is hit before TP
- If neither is hit within the max hold period (24 candles = 1 day), close at last price

### Performance Metrics (must pass ALL)

| Metric | Minimum Target | Why |
|--------|---------------|-----|
| Win Rate | > 54% | Minimum edge over 50% (with fees) |
| Profit Factor | > 1.5 | Gross wins / gross losses |
| Total Trades | > 30 | Statistical significance |
| Max Drawdown | < -15% | Risk control |
| Sharpe Ratio | > 0.8 | Risk-adjusted return |
| Avg Hold Time | < 24h | Avoid overnight funding costs |

### Report Format
```json
{
  "backtest_id": "bt_20260519_001",
  "trade_idea_id": "ti_20260519_001",
  "asset": "SOL",
  "direction": "long",
  "status": "approved",
  "metrics": {
    "total_trades": 45,
    "wins": 27,
    "losses": 18,
    "win_rate_pct": 60.0,
    "profit_factor": 1.82,
    "max_drawdown_pct": -8.3,
    "sharpe_ratio": 1.12,
    "avg_hold_candles": 8.3,
    "net_profit_pct": 14.7
  },
  "data_range": {
    "from": "2026-03-01",
    "to": "2026-05-19",
    "timeframe": "1h",
    "candles_used": 1968
  },
  "rejected_reason": null
}
```

If any metric fails, the status is `rejected` and `rejected_reason` explains which metric failed.

## Dependencies
- Python 3.8+
- Standard library: `urllib.request`, `json`, `datetime`, `math`
- No external pip packages required (uses Data Getter Agent for data)

## Configuration
```yaml
backtester:
  default_lookback_days: 60
  max_hold_candles: 24  # 1 day max hold
  slippage_pct: 0.05
  pass_thresholds:
    min_win_rate: 54.0
    min_profit_factor: 1.5
    min_trades: 30
    max_drawdown: 15.0
    min_sharpe: 0.8
  output_dir: "reports/"
```

## Files
| File | Purpose |
|------|---------|
| `backtester.py` | Main backtesting engine |
| `reports/backtest_results_latest.json` | Output read by Trader Agent (only approved ideas forwarded) |

## Communication
- **Calls:** Data Getter Agent (for historical klines)
- **Reads from:** `reports/trade_ideas_latest.json` (written by Data Analyst)
- **Writes to:** `reports/backtest_results_latest.json` (read by Trader Agent)
