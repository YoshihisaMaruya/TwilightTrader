__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

from net.asserter.crawler.economic_indicator import YahooFinance

yahoo_finance = YahooFinance()

cec = yahoo_finance.cec()
print("cec => ")
print(cec)

#cpi_usa = yahoo_finance.cpi_usa()
#print("cpi => ")
#print(cpi_usa)

#retail_sales = yahoo_finance.retail_sales()
#print("retail_sales => ")
#print(retail_sales)
