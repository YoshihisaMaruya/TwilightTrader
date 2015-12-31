__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

from crawler.economic_indicator import YahooFinance
from common.util import IO
import os

config = IO.read_config_all()
yahoo_finance = config["yahoo_finance"]

for key in yahoo_finance:
	print(yahoo_finance[key] + ":" + key)
	YahooFinance.create(key,yahoo_finance[key])
