__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

import PyV8
import urllib.request
import re
from common.util import Log, IO
from model.economic_indicator import EconomicIndicatorDatabase

# Yahoo Financeから情報を取得する
# TODO : 1. 一つのページに２つの情報がある場合(Ex. 雇用統計と失業保険), 2. expectAllの2013/9/1が２つある場合(Ex. 小売売上高)
class YahooFinance:
    # ページをパーズし、経済指標データを取得
    @staticmethod
    def __parse_page(page):
        s = ''
        for line in page.readlines():
            s = s + line.decode('utf-8')
        Log.info('html: ' + s)
        expect_all_js = re.search(r'var expectAll((.|\n)*?)};', s).group()
        result_all_js = re.search(r'var resultAll((.|\n)*?)};', s).group()
        js = expect_all_js + "\n" + result_all_js
        Log.info("js: " + js)
        return YahooFinance.__to_python_format(js)

    # javascriptの配列からpythonの配列に変換
    @staticmethod
    def __to_python_format(js):
        ctx = PyV8.JSContext()
        ctx.enter()
        ctx.eval(js)
        expect_all = dict((d[0].strftime('%Y/%m/%d'), d[1]) for d in PyV8.convert(ctx.locals["expectAll"]["data"]))
        result_all = dict((d[0].strftime('%Y/%m/%d'), d[1]) for d in PyV8.convert(ctx.locals["resultAll"]["data"]))
        return {"expectAll": expect_all, "resultAll":  result_all}

    @staticmethod
    def __get(url):
        with urllib.request.urlopen(url=url) as page:
            data = YahooFinance.__parse_page(page)
            result = dict((date, {'expect': data["expectAll"].get(date), 'result': data["resultAll"].get(date)})
                 for date in data["expectAll"].keys() if data["resultAll"].get(date) != None)
            Log.info(result)
            return result

    @staticmethod
    def create(key,url):
        EconomicIndicatorDatabase.create_table(key)
        result = YahooFinance.update(key,url)
        return result

    @staticmethod
    def update(key,url):
        Log.info("key: " + key)
        Log.info("access_to: " + url)
        result = YahooFinance.__get(url)
        EconomicIndicatorDatabase.insert(key,result)
        return result

        