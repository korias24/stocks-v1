# -*- coding: utf-8 -*-

import json
import os.path

from stocks.data_provider.interface import Interface

# TODO: Update this with the new API changes!

"""
This class provides data from a fixture. It takes-in a fixture directory that contains
the result of each method call, segmented by argument (so kind of like a cache). The data
should be stored as:

<fixture_dir>
  <method_name>_<posn_arg1>...<posn_argn>...<kw_arg1>:<kw_arg1_v>.json

For example,

<fixture_dir>
  eod_data_bulk_<date>.json

^ This should be good enough.

Now how can I figure out the path from the method call? Probably want something like
data_path(method, ...) and do it that way?
"""
# This class fetches its data from static files. 
# tests as well as local testing. Should probably take a data_dir
class Fixture(Interface):
    def __init__(self, fixture_dir):
        if not os.path.isdir(fixture_dir):
            raise RuntimeError("fixture directory %s does not exist" % fixture_dir)
        self.fixture_dir = fixture_dir

    def eod_data_bulk(self, date, exchange):
        return self.read_data('eod_data_bulk', date)

    def data_path(self, method, *args):
        basename = '_'.join([str(x) for x in [method, *args]]) + '.json'
        return str(os.path.join(self.fixture_dir, basename))

    def read_data(self, method, *args):
        path = self.data_path(method, *args)
        if not os.path.isfile(path):
            # TODO: Raise more specific error here?
            raise RuntimeError("fixture file %s does not exist" % path)
        with open(path) as f:
            data = json.load(f)
        return data
