# 🤖 IA TRADING MASTER

An intelligent trading application powered by Streamlit that provides high-probability trading signals with professional risk management.

## Features

✨ **AI-Powered Trading Signals**
- Real-time EMA (9/21) crossover analysis
- RSI-based momentum confirmation
- Automatic buy/sell signal generation

🛡️ **Risk Management**
- Dynamic position sizing based on capital
- Customizable stop-loss and take-profit levels
- Configurable risk per trade percentage

📊 **Live Market Data**
- Real-time price feeds via yfinance
- Interactive candlestick charts with Plotly
- Multiple timeframes (1m, 5m, 15m, 1h)

⚡ **Signal Expiration Logic**
- Prevents late entries (>0.15% candle movement)
- High-probability trade confirmation

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Doomsky1975/trading.git
cd trading
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Configuration

Use the sidebar to customize:
- **Actif (Asset)**: Symbol to trade (e.g., BTC-USD, EURUSD=X, AAPL)
- **Unité de temps (Timeframe)**: 1m, 5m, 15m, or 1h
- **Risque par trade (%)**: Risk percentage per trade (0.1-5.0%)
- **Capital ($)**: Your trading capital amount

## Trading Logic

### Buy Signal 🚀
- EMA 9 > EMA 21
- RSI < 65
- Not expired (price movement < 0.15%)

### Sell Signal 📉
- EMA 9 < EMA 21
- RSI > 35
- Not expired (price movement < 0.15%)

## Risk Management

The application calculates:
- **Stop Loss**: 0.5% below entry (buy) / above entry (sell)
- **Take Profit**: 1% above entry (buy) / below entry (sell)
- **Position Size**: Based on risk amount and stop-loss distance

## Requirements

See `requirements.txt` for all dependencies:
- streamlit
- pandas
- pandas-ta
- yfinance
- plotly

## License

MIT License

## Disclaimer

⚠️ **This application is for educational purposes only. Trading carries risk. Always use proper risk management and never risk more than you can afford to lose.**

## Author

Created by Doomsky1975
