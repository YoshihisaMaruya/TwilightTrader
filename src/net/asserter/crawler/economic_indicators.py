__author__ = 'rv'
# Get economic indicators from yahoo finance

from net.asserter.common import util
from html.parser import HTMLParser
import urllib.request
import PyV8



tag="crawler"

# Parse Yahoo page, Get js
def parse_page(page,index = 0):
    ctx = PyV8.JSContext()
    s = ''
    js_flag = 0
    i = 0
    for line in page.readlines():
        l = line.decode('utf-8')
        if l.count('var expect ='):
            js_flag = 1
        if l.count('var plot = $.plot($("#placeholder' + str(i) + '"), [expect, result]'):
            if i == index:
                util.log_info(tag,s)
                return s
            s = ''
            js_flag = 0
            i = i + 1
        if js_flag:
            s = s + l

    return "JS Not found"

#javascript to python
def to_python_format(js):
    ctx = PyV8.JSContext()
    ctx.enter()
    ctx.eval(js)
    expectAll = []
    resultAll = []
    try:
        expectAll = PyV8.convert(ctx.locals["expectAll"]["data"])
        resultAll = PyV8.convert(ctx.locals["resultAll"]["data"])
    except:
        util.log_error(tag,"JS Array not found")
        util.log_error(tag,js)
        raise  Exception("JS Array not found")
    r = {"expectAll": PyV8.convert(expectAll), "resultAll":  PyV8.convert(resultAll)}
    return {"expectAll": expectAll, "resultAll":  resultAll}


# Yahoo financeのexpectAllの2013/9/1は二つある。後半が正しい
def get(url,std_tiem, sumemr_time,index = 0):
    data = []
    r = []

    with urllib.request.urlopen(url=url) as page:
        scripts = parse_page(page,index)
        pf = to_python_format(scripts)
        j = 0
        for i in range(0,len(pf["resultAll"])):
            expect = pf["expectAll"][i + j]
            result = pf["resultAll"][i]
            # Patch
            if expect[0] != result[0]:
                if str(expect[0].strftime('%Y/%m/%d')) ==  "2013/09/01":
                    j = 1
                    r[len(r) - 1]["expect"] = expect[1]
                    expect =  pf["expectAll"][i + j]
                    util.log_info(tag,"Add patch in " + url)
                else:
                    util.log_error(tag,"Datetime is not equaled : " + str(expect[0].strftime('%Y/%m/%d')) + " , " + str(result[0].strftime('%Y/%m/%d')))
                    util.log_info(tag,"Datetime is not equaled : " + scripts)
                    raise Exception("Datetime is not equaled")
            # End
            is_summertime = util.is_summertime(expect[0])
            if is_summertime:
                time = sumemr_time
            else:
                time = std_tiem
            x = {"date" : expect[0], "time" : time, "expect" : expect[1], "result" : result[1], "is_summertime" : is_summertime}
            r.append(x)
    return r

def cec(from_yahoo=False, is_save=False):
    util.log_info(tag,"Get cec")
    r = []
    if from_yahoo:
        url = util.read_config(key1="yahoo",key2="cec")
        util.log_info(tag,"Get form " + url)
        r = get(url,"21:30","22.30")
        if is_save:
            util.save_economic_indicators("cec",r)
    else:
        r = 0
    return r

def unemployment_rate(from_yahoo=False, is_save=False):
    util.log_info(tag,"Get unemployment_rate")
    r = []
    if from_yahoo:
        url = util.read_config(key1="yahoo",key2="cec")
        util.log_info(tag,"Get form " + url)
        r = get(url,"21:30","22.30",1)
        if is_save:
            util.save_economic_indicators("unemployment_rate",r)
    else:
        r = 0
    return r

def cpi_usa(from_yahoo=False, is_save=False):
    util.log_info(tag,"Get cpi_usa")
    r = []
    if from_yahoo:
        url = util.read_config(key1="yahoo",key2="cpi_usa")
        util.log_info(tag,"Get form " + url)
        r = get(url,"21:30","22.30")
        if is_save:
            util.save_economic_indicators("cpi_usa",r)
    else:
        r = 0
    return r

def  retail_sales(from_yahoo=False, is_save=False):
    util.log_info(tag,"Get retail_sales")
    r = []
    if from_yahoo:
        url = util.read_config(key1="yahoo",key2="retail_sales")
        util.log_info(tag,"Get form " + url)
        r = get(url,"21:30","22.30")
        if is_save:
            util.save_economic_indicators("retail_sales",r)
    else:
        r = 0
    return r