__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

from net.asserter.crawler.economic_indicator import YahooFinance
import os
import shutil
from net.asserter.model.commodity import CommodityDatabase
from net.asserter.model.exchange import ExchangeDatabase

print("init script start...")

shutil.rmtree(os.getenv('TT_HOME') + '/db')
os.mkdir(os.getenv('TT_HOME') + '/db')
shutil.rmtree(os.getenv('TT_HOME') + '/log')
os.mkdir(os.getenv('TT_HOME') + '/log')

YahooFinance.cec(create=True)
YahooFinance.cpi(create=True)
YahooFinance.retail_sales(create=True)

ExchangeDatabase.create_table()
CommodityDatabase.create_table()

print("init script end")