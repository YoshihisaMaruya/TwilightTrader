__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

import os
from net.asserter.common.util import Log
from net.asserter.model.common import DB
from datetime import datetime

db_filename = os.getenv('TT_HOME') + '/db/economic_indicator.db'

class EconomicIndicatorDatabase:
    @staticmethod
    def create_table(economic_indicator):
        schema = """create table {economic_indicator} (
                 date         int primary key not null,
                 expect       text,
                 result       text
                );""".format(economic_indicator=economic_indicator)
        DB.create_table(db_filename, schema)

    @staticmethod
    def insert(economic_indicator, data):

        def func(connect):
            for date, value in data.items():
                sql_cmd = """
                insert into {economic_indicator} (date, expect, result)
                values ('{date}', '{expect}', '{result}')
                """.format(economic_indicator=economic_indicator, date="".join(date.split("/")), expect=value['expect'], result=value["result"])

                Log.info("sql_cmd: " + sql_cmd)
                connect.execute(sql_cmd)

        DB.execute(db_filename,func)