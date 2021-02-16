# -*- coding: utf-8 -*-

import functools
import json
import os.path
import requests

from stocks.data_provider.interface import Interface

"""
This class fetches data from EOD Historical Data. Its constructor requires
two arguments:
    * api_token
    * cache_dir

TODO: Add logging later
"""
class EODHD(Interface):
    def __init__(self, api_token, cache_dir):
        self._api_token = api_token
        if not os.path.isdir(cache_dir):
            raise RuntimeError("cache directory %s does not exist" % cache_dir)
        self._cache_dir = cache_dir

    def eod_data(self, ticker, exchange, date):
        bulk_data = self.eod_data_bulk(exchange, date)
        return bulk_data.get(ticker, {})

    """
    This is cached as
        <cache_dir>
            fundamental_data
                <exchange>
                    <ticker>.json
    """
    def fundamental_data(self, ticker, exchange):
        def op():
            data = self.eodhd_get("fundamentals/%s.%s" % (ticker, exchange))
            # data is large so just return what we need.
            #
            # TODO: we may need to re-evaluate this approach
            # if our subset becomes too large
            subset = {}
            general_data = data.get('General')
            if general_data:
                subset['company'] = general_data.get('Name')
                for key in ['Sector', 'Industry', 'Exchange']:
                    subset[key.lower()] = general_data.get(key)
            return subset

        rel_path = os.path.join(
            'fundamental_data',
            exchange,
            "%s.json" % ticker
        )
        return self.cached_op(
            rel_path,
            op
        )

    """
    This is cached as
        <cache_dir>
            eod_data_bulk
                <exchange>
                    <year>
                        <month>
                            <day>.json

    TODO: We cache the most recent 21 calls. It might be worth creating a more
    specialized cache for this later (e.g. maybe one that focuses on date vs. lru?).
    """
    @functools.lru_cache(maxsize = 21)
    def eod_data_bulk(self, exchange, date):
        def op():
            raw_data = self.eodhd_get(
                "eod-bulk-last-day/%s" % exchange,
                query_params = { 'date': str(date), 'filter': 'extended' }
            )
            data = {}
            for d in raw_data:
                ticker = d.pop('code')
                data[ticker] = d
            return data

        rel_path = os.path.join(
            'eod_data_bulk',
            exchange,
            str(date.year),
            str(date.month),
            "%s.json" % date.day
        )
        return self.cached_op(rel_path, op)

    """
    This is cached as
        <cache_dir>
            tickers
                <exchange>.json

    TODO: Refactor ^ to auto-update periodically, e.g. maybe once every
    week. We can do this by storing it as tickers-<date>.json.
    """
    def tickers(self, exchange):
        def op():
            raw_data = self.eodhd_get(
                "exchange-symbol-list/%s" % exchange
            )
            data = {}
            for d in raw_data:
                ticker = d.pop('Code')
                data[ticker] = d
            return data

        rel_path = os.path.join('tickers', "%s.json" % exchange)
        return self.cached_op(rel_path, op)

    def cached_op(self, rel_path, op):
        abs_path = os.path.join(self._cache_dir, rel_path)
        if os.path.isfile(abs_path):
            with open(abs_path) as f:
                return json.load(f)
        dir_name = os.path.dirname(abs_path)
        data = op()
        os.makedirs(dir_name, exist_ok = True)
        with open(abs_path, 'w') as f:
            json.dump(data, f)
        return data

    def eodhd_get(self, endpoint, query_params = {}):
        query_params['api_token'] = self._api_token
        query_params['fmt'] = 'json'
        query_str = '&'.join(["%s=%s" % (param, value) for (param, value) in query_params.items()])
        url = "https://eodhistoricaldata.com/api/%s?%s" % (endpoint, query_str)
        resp = requests.get(url)
        if resp.status_code >= 400:
            raise RuntimeError("request to %s failed:\nstatus: %s\nbody:\n%s" % (url, resp.status_code, resp.text))
        return resp.json()
