import ccxt
import pandas as pd

binance = ccxt.binance({'enableRateLimit': True})

params  = {'type': 'future'}
markets = binance.load_markets(True, params)
# "BTC/USDT" PERPETUAL

params  = {'type': 'delivery'}
markets = binance.load_markets(True, params)
# 'BTC/USD', 'BTCUSD_210924', 'BTCUSD_211231'

symbol = "BTC/USDT"
bars = binance.fetch_ohlcv(symbol, timeframe='1d', limit=500)
df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
