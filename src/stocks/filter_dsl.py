# -*- coding: utf-8 -*-

import os
import functools

from stocks.predicate import *

def filter_tickers(p, tickers):
    return {symbol: ticker for symbol, ticker in tickers.items() if p(ticker)}

def andf(*fs):
    def _f(tickers):
        return functools.reduce(lambda _tickers, f: f(_tickers), fs, tickers)

    return _f

# _dictp => dictionary predicate
def _dictp(d, k, p):
    if k in d:
        return p(d[k])
    return False

def close(td, np):
    def f(tickers):
        return filter_tickers(lambda t: _dictp(t.eod_data(td), 'close', np), tickers)

    return f

def market_cap(td, np):
    def f(tickers):
        return filter_tickers(lambda t: _dictp(t.eod_data(td), 'MarketCapitalization', np), tickers)

    return f

def exchange(sp):
    def f(tickers):
        return filter_tickers(lambda t: sp(t.exchange), tickers)

    return f

def ignore_exchanges(*exchanges):
    sp = [neql(exchange) for exchange in exchanges]
    sp = andp(*sp)
    return exchange(sp)

def min_volume(v, from_date, to_date, min_satisfying):
    def f(tickers):
        np = gte(v)
        def p(ticker):
            num_satisfying = 0
            delta = to_date - from_date
            for num_days in range(0, delta.days + 1):
                date = from_date + datetime.timedelta(days = num_days)
                if _dictp(ticker.eod_data(date), 'volume', np):
                    num_satisfying = num_satisfying + 1
            return num_satisfying >= min_satisfying

        return filter_tickers(p, tickers)

    return f

def symbol(sp):
    def f(tickers):
        return filter_tickers(lambda t: sp(t.symbol), tickers)

    return f

def ignore_symbols(*symbols):
    sp = [neql(symbol) for symbol in symbols]
    sp = andp(*sp)
    return symbol(sp)

with open('/Users/enis.inan/GitHub/stocks/ignored_companies.txt') as f:
    raw = f.read()
    ignored = raw.split("\n")

import datetime
td = datetime.date(2021, 2, 18)

from stocks.data_provider.eodhd import EODHD
dp = EODHD(api_token = os.environ.get('EODHD_API_TOKEN'), cache_dir = '/Users/enis.inan/.stocks_cache')

from stocks.ticker import Ticker
tickers = dp.tickers('US')

sfilter = andf(
    ignore_symbols(*ignored),
    ignore_exchanges('OTCGREY'),
    close(td, andp(gte(0.001), lt(0.03))),
    # TODO: Add 3-5 cents
    #close(td, lt(0.1)),
    # for 0.02 <= x < 0.03
    #close(td, andp(gte(0.02), lt(0.03))),
    # for 0.01 <= x < 0.02 stocks
    #close(td, andp(gte(0.01), lt(0.02))),
    market_cap(td, gte(3000000)),
    min_volume(10000000, td - datetime.timedelta(days = 14), td, 1)
    #min_volume(1000000, td - datetime.timedelta(days = 14), td)
)
