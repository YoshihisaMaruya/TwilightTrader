__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

import PyV8
import urllib.request
import re
from net.asserter.common.util import Log, IO
from net.asserter.model.economic_indicator import EconomicIndicatorDatabase

# Yahoo Financeから情報を取得する
# TODO : 1. 一つのページに２つの情報がある場合(Ex. 雇用統計と失業保険), 2. expectAllの2013/9/1が２つある場合(Ex. 小売売上高)
class YahooFinance:

    # ページをパーズし、経済指標データを取得
    def __parse_page(self, page):
        s = ''
        for line in page.readlines():
            s = s + line.decode('utf-8')
        Log.info('html: ' + s)
        expect_all_js = re.search(r'var expectAll((.|\n)*?)};', s).group()
        result_all_js = re.search(r'var resultAll((.|\n)*?)};', s).group()
        js = expect_all_js + "\n" + result_all_js
        Log.info("js: " + js)
        return self.__to_python_format(js)

    # javascriptの配列からpythonの配列に変換
    def __to_python_format(self, js):
        ctx = PyV8.JSContext()
        ctx.enter()
        ctx.eval(js)
        expect_all = dict((d[0].strftime('%Y/%m/%d'), d[1]) for d in PyV8.convert(ctx.locals["expectAll"]["data"]))
        result_all = dict((d[0].strftime('%Y/%m/%d'), d[1]) for d in PyV8.convert(ctx.locals["resultAll"]["data"]))
        return {"expectAll": expect_all, "resultAll":  result_all}

    def __get(self, url):
        with urllib.request.urlopen(url=url) as page:
            data = self.__parse_page(page)
            result = dict((date, {'expect': data["expectAll"].get(date), 'result': data["resultAll"].get(date)})
                 for date in data["expectAll"].keys() if data["resultAll"].get(date) != None)
            Log.info(result)
            return result

    def get(self, key1, key2, save):
        url = IO.read_config(key1, key2)
        Log.info("access_to: " + url)
        result = self.__get(url)
        return result

    # 雇用統計
    def cec(self, save=True):
        result = self.get(key1="yahoo", key2="cec", save=save)
        if save:
            EconomicIndicatorDatabase.insert(result)
        return result

    # CPI
    def cpi_usa(self,save = True):
        result = self.get(key1="yahoo", key2="cpi_usa", save=save)
        return result

    # 小売売上高
    def retail_sales(self,save = True):
        result = self.get(key1="yahoo", key2="retail_sales", save=save)
        return result