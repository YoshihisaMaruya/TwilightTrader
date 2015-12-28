__author__ = 'rv'

import os
import sqlite3
from net.asserter.common.util import Log

class DB:
    @staticmethod
    def load(db_filename, schema_filename):
        connect = sqlite3.connect(db_filename)
        f = open(schema_filename, 'rt')
        schema = f.read()
        f.close()
        Log.info("sql_cmd: " + schema)
        try:
            connect.executescript(schema)
        except sqlite3.OperationalError:
            Log.info("table is already exsisted")
        return connect
