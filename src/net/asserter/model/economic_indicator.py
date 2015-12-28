__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

import os
import sqlite3
from net.asserter.common.util import Log

db = sqlite3.connect(os.getenv('TT_HOME') + '/data/economic_indicator.db')
cur = db.cursor()

class EconomicIndicatorDatabase:
    @staticmethod
    def create_table(table_name):
        sql_cmd = "CREATE TABLE test(id INTEGER, name TEXT)"
        Log.info("sql_cmd: " + sql_cmd)
        cur.execute(sql_cmd)
        db.commit()