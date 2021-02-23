import os
import json
import datetime

from stocks.data_provider.eodhd import EODHD
from stocks.filter_dsl import *
from stocks.predicate import *

def parse_ignored_companies():
    with open('/Users/enis.inan/GitHub/stocks/ignored_companies.txt') as f:
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

td = datetime.date(2021, 2, 22)
dp = EODHD(api_token = os.environ.get('EODHD_API_TOKEN'), cache_dir = '/Users/enis.inan/.stocks_cache')
tickers = dp.tickers('US')

# sfilter => stocks filter
sfilter = andf(
    ignore_symbols(*parse_ignored_companies()),
    ignore_exchanges('OTCGREY'),
    close(td, andp(gt(0), lt(0.05))),
    market_cap(td, gte(3000000)),
    min_volume(1000000, td - datetime.timedelta(days = 14), td, 1)
)
