# -*- coding: utf-8 -*-

import os
import functools

from stocks.predicate import *

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
        return list(filter(lambda t: _dictp(t.eod_data(td), 'close', np), tickers))

    return f

def market_cap(td, np):
    def f(tickers):
        return list(filter(lambda t: _dictp(t.eod_data(td), 'MarketCapitalization', np), tickers))

    return f

def exchange(sp):
    def f(tickers):
        return list(filter(lambda t: sp(t.exchange), tickers))

    return f

def ignore_exchanges(*exchanges):
    sp = [neql(exchange) for exchange in exchanges]
    sp = andp(*sp)
    return exchange(sp)

def min_volume(v, from_date, to_date):
    def f(tickers):
        np = gte(v)
        def p(ticker):
            delta = to_date - from_date
            for num_days in range(0, delta.days + 1):
                date = from_date + datetime.timedelta(days = num_days)
                if _dictp(ticker.eod_data(date), 'volume', np):
                    return True
            return False

        return list(filter(p, tickers))

    return f

def symbol(sp):
    def f(tickers):
        return list(filter(lambda t: sp(t.symbol), tickers))

    return f

def ignore_symbols(*symbols):
    sp = [neql(symbol) for symbol in symbols]
    sp = andp(*sp)
    return symbol(sp)

with open('/Users/enis.inan/GitHub/stocks/ignored_companies.txt') as f:
    raw = f.read()
    ignored = raw.split("\n")

import datetime
td = datetime.date(2021, 2, 12)

from stocks.data_provider.eodhd import EODHD
dp = EODHD(api_token = os.environ.get('EODHD_API_TOKEN'), cache_dir = '/Users/enis.inan/.stocks_cache')

from stocks.ticker import Ticker
ticker_dict = dp.tickers('US')
tickers = list(map(lambda symbol: Ticker(symbol, 'US', ticker_dict[symbol], dp), ticker_dict))

sfilter = andf(
    ignore_symbols(*ignored),
    ignore_exchanges('OTCGREY'),
    close(td, andp(gte(0.01), lt(0.02))),
    market_cap(td, gte(3000000)),
    min_volume(1000000, td - datetime.timedelta(days = 14), td)
)
