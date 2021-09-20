#!/usr/bin/env python3
"""
Fetch exchange order book data and save as jsonlines

Historical order book data are only available via paid service,
so saving the data is a cheaper way for analyzing execution cost/strategy
"""

import sys
import argparse
import time
import ccxt
import jsonlines # need to install
from datetime import datetime


def warn(msg, t=None):
    if t:
        print("[" + t.strftime("%H:%M:%S") + "]", msg, file=sys.stderr)
    else:
        print(msg, file=sys.stderr)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("symbol", type=str, help="product symbol/pair")
    parser.add_argument("file", type=str, help="output jsonlines filename")
    parser.add_argument("-x", "--exchange", required=False, default="binanceus",
                        help="exchange supported by ccxt")
    args = parser.parse_args()

    symbol = args.symbol
    filename = args.file
    exchange = getattr(ccxt, args.exchange)()

    writer = jsonlines.open(filename, mode="w")
    delay = 10
    connection_wait = 30
    stamp, prev_stamp = 0, 0
    while True:
        t = datetime.now()

        # only fetch one order book per minute due to exchange rate limit
        stamp = int(t.replace(second=0, microsecond=0).timestamp())
        if stamp == prev_stamp:
            # warn("waiting for next minute......", t)
            time.sleep(delay)
            continue
        else:
            warn("new minute in", t)
            prev_stamp = stamp

        try:
            orders = exchange.fetch_order_book(symbol)
        except ConnectionError:
            warn(f"network error. sleep {connection_wait} seconds", t)
            time.sleep(connection_wait)
            continue

        orders["bids"] = orders["bids"][:10]
        orders["asks"] = orders["asks"][:10]
        orders["timestamp"] = stamp
        del orders["datetime"]
        del orders["nonce"]

        writer.write(orders)
        time.sleep(delay)

    writer.close()


if __name__ == '__main__':
    main()
