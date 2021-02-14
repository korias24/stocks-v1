import datetime

from stocks.data_provider.fixture import Fixture

def close_lt(data, p):
    return list(filter(lambda x: x['close'] < p, data))

def close_gte(data, p):
    return list(filter(lambda x: x['close'] >= p, data))

def volume_gt(data, v, days = 14):
    vol_key = "avgvol_%sd" % days
    return list(filter(lambda x: x[vol_key] > v, data))

def volume_gte(data, v, days = 14):
    vol_key = "avgvol_%sd" % days
    return list(filter(lambda x: x[vol_key] >= v, data))

def volume_lt(data, v, days = 14):
    vol_key = "avgvol_%sd" % days
    return list(filter(lambda x: x[vol_key] < v, data))


def marketcap_gte(data, v):
    return list(filter(lambda x: x['MarketCapitalization'] >= v, data))

def company_list(data):
    return "\n".join([', '.join([x['code'], x['name']]) for x in data])

def write(path, string):
    with open(path, 'w') as f:
        f.write(string)

def newer(data, old):
    old_codes = {}
    for item in old:
        old_codes[item['code']] = True
    return list(filter(lambda x: not(x['code'] in old_codes), data))

def parse_ignored_companies():
    with open('/Users/enis.inan/GitHub/stocks/ignored_companies.txt', 'r') as f:
        ignored_companies_raw = f.read()
    ignored_companies_list = ignored_companies_raw.split("\n")
    ignored_companies = {}
    for item in ignored_companies_list:
        ignored_companies[item] = True
    return ignored_companies

def filter_ignored(data):
    ignored_companies = parse_ignored_companies()
    return list(filter(lambda x: not(x['code'] in ignored_companies), data))

dp = Fixture('/Users/enis.inan/.stocks_fixtures')
data_2010 = dp.eod_data_bulk(datetime.date(2010, 2, 1))
data_2013 = dp.eod_data_bulk(datetime.date(2013, 1, 31))
data_2016 = dp.eod_data_bulk(datetime.date(2016, 1, 31))
data_2018 = dp.eod_data_bulk(datetime.date(2018, 1, 31))
data_2019 = dp.eod_data_bulk(datetime.date(2019, 1, 31))
data_2020 = dp.eod_data_bulk(datetime.date(2020, 1, 31))
data_dec_2020 = dp.eod_data_bulk(datetime.date(2020, 12, 1))
data_raw = dp.eod_data_bulk(datetime.date(2021, 2, 12))
data = filter_ignored(data_raw)
