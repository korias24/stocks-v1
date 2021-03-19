import os
import json
import datetime

from stocks.data_provider.eodhd import EODHD
from stocks.filter_dsl import *
from stocks.predicate import *

def parse_ignored_companies(path = '/Users/enis.inan/GitHub/stocks/ignored_companies.txt'):
    with open(path) as f:
        raw = f.read()
        ignored = raw.split("\n")

    return ignored

def pretty_str(tickers):
    return "\n".join([str(t) for _, t in tickers.items()])

def pretty_json(data):
    return json.dumps(data, indent = 2)

def write_tickers(path, tickers):
    with open(path, 'w') as f:
        f.write("\n".join([t.symbol for _, t in tickers.items()]))

td = datetime.date(2021, 3, 18)
dp = EODHD(api_token = os.environ.get('EODHD_API_TOKEN'), cache_dir = '/Users/enis.inan/.stocks_cache')
tickers = dp.tickers('US')

# dfilter => default filter
dfilter = andf(
    ignore_symbols(*parse_ignored_companies()),
    ignore_symbols(*parse_ignored_companies('/Users/enis.inan/GitHub/stocks/absolutely_ignored_companies.txt')),
    ignore_symbols(*parse_ignored_companies('/Users/enis.inan/GitHub/stocks/temporarily_ignored_companies.txt')),
    ignore_exchanges('OTCGREY'),
    close(td, andp(gte(0.01), lte(0.022))),
    market_cap(td, gte(3000000)),
    min_volume(10000000, td - datetime.timedelta(days = 14), td, 3)
)

sfilter = andf(
    ignore_symbols(*parse_ignored_companies('/Users/enis.inan/GitHub/stocks/absolutely_ignored_companies.txt')),
    ignore_symbols(*parse_ignored_companies('/Users/enis.inan/GitHub/stocks/temporarily_ignored_companies.txt')),
    ignore_exchanges('OTCGREY'),
    close(td, andp(gt(0), lt(0.005))),
    market_cap(td, gt(0)),
    #market_cap(td, gte(3000000)),
    min_volume(20000000, td - datetime.timedelta(days = 14), td, 5)
)

print("REMINDER: DELETE TEMPORARILY IGNORED COMPANIES")

