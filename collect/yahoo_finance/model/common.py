__author__ = 'rv'

import os
import sqlite3
from common.util import Log

class DB:
    @staticmethod
    def execute(db_filename,func):
        connect = sqlite3.connect(db_filename)
        func(connect)
        connect.commit()
        connect.close()

    @staticmethod
    def create_table(db_filename, schema):
        def func(connect):
            Log.info("sql_cmd: " + schema)
            connect.executescript(schema)

        DB.execute(db_filename,func)
