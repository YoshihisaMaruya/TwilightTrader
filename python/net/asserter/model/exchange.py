__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

import os
import sqlite3
from net.asserter.common.util import Log
from net.asserter.model.common import DB

db_filename = os.getenv('TT_HOME') + '/db/exchange.db'
tables = {"eurusd","usdjpy","eurjpy"}

class ExchangeDatabase:
    @staticmethod
    def create_table():
        for table in tables:
            schema = """create table {table} (
                     id integer primary key autoincrement not null,
                     timestamp         integer not null,
                     bid       text,
                     ask       text
                    );""".format(table=table)
            DB.create_table(db_filename, schema)