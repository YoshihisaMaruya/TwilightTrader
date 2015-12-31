__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

from crawler.economic_indicator import YahooFinance
import os
import shutil

print("init script start...")

YahooFinance.cec()
YahooFinance.cpi()
YahooFinance.retail_sales()

print("init script end")