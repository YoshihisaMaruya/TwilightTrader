__author__ = 'rv'

from net.asserter.crawler import economic_indicators

if __name__ == "__main__":
    print("Hello")
    economic_indicators.cec(from_yahoo=True,is_save=True)
    economic_indicators.unemployment_rate(from_yahoo=True,is_save=True)
    economic_indicators.retail_sales(from_yahoo=True,is_save=True)
    economic_indicators.cpi_usa(from_yahoo=True,is_save=True)