#!/usr/bin/env python3
"""
Generate hypothetical order book based on OHLCV data
"""

import argparse
import json
import numpy as np

TIMESTAMP_INDEX = 0
OPEN_INDEX = 1
HIGH_INDEX = 2
LOW_INDEX = 3
CLOSE_INDEX = 4


def simple_deterministic(ohlcv: list) -> list:
    """
    Generate bid/ask around open prices
    Assume cummulative bids and asks follow a fixed discreet log distribution
    from 0.01% to 0.1% for the total amount for $50k on each side
    """
    ohlcv_mx = np.array(ohlcv)
    timestamps = ohlcv_mx[:, TIMESTAMP_INDEX]
    prices = ohlcv_mx[:, OPEN_INDEX]
    row_count = len(ohlcv)  # = ohlcv_mx.shape[0]
    
    ask_bumps = 1 + np.arange(1, 11) / 1e4
    bid_bumps = 1 - np.arange(1, 11) / 1e4
    ask_prices = np.outer(prices, ask_bumps)
    ask_volumes = 5000 / ask_prices
    bid_prices = np.outer(prices, bid_bumps)
    bid_volumes = 5000 / bid_prices

    order_book = []
    for i in range(row_count):
        order_book.append({
            "timestamp": int(timestamps[i]),
            "bids": list(zip(bid_prices[i, :], bid_volumes[i, :])),
            "asks": list(zip(ask_prices[i, :], ask_volumes[i, :]))
        })
    return order_book


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="input OHLCV data json file")
    parser.add_argument("output", type=str, help="output order book json file")
    args = parser.parse_args()

    in_file = args.input
    out_file = args.output

    with open(in_file, "r") as fp:
        ohlcv = json.load(fp)

    order_book = simple_deterministic(ohlcv)

    with open(out_file, "w") as fp:
        json.dump(order_book, fp)


if __name__ == "__main__":
    main()
