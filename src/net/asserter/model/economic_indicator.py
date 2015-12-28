__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

import os
import sqlite3
from net.asserter.common.util import Log
from net.asserter.model.common import DB

db_filename = os.getenv('TT_HOME') + '/db/economic_indicator.db'
schema_filename = os.getenv('TT_HOME') + '/db/economic_indicator.sql'

connect = DB.load(db_filename,schema_filename)

class EconomicIndicatorDatabase:
    @staticmethod
    def insert(data):
        for key,d in data.items():
            sql_cmd = """
            insert into economic_indicator (date, expect, result)
            values ('{date}', '{expect}', '{result}')
            """.format(date=key, expect=d['expect'], result=d["result"])

            Log.info("sql_cmd: " + sql_cmd)
            connect.execute(sql_cmd)
        connect.commit()