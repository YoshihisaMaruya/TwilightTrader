__author__ = 'rv'
import pytz
import configparser
import logging

logging.basicConfig(filename='/var/log/twilight_trader.log', level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

project_path = '/Users/rv/workspace/TwilightTrader'
common_config_path = project_path + '/config/common.ini'
economic_indicators_path = project_path + '/data/economic_indicator'

def is_summertime(d):
    tz_jst = pytz.timezone("Asia/Tokyo")
    tz_est = pytz.timezone("US/Eastern")
    t_jst = tz_jst.localize(d)
    t_jst.astimezone(tz_est)
    tm_isdst = t_jst.astimezone(tz_est).timetuple().tm_isdst
    return tm_isdst

def log_info(tag,message):
    logging.info("INFO:crawler:" + message)

def log_error(tag,message):
    logging.error("INFO:crawler:" + message)

def read_config(key1,key2):
    config = configparser.ConfigParser()
    try:
        config.read(common_config_path)
    except:
        log_info("read_config","TT_HOME don't find")
    return config[key1][key2]

#
def save_economic_indicators(filename,data,seq='\t'):
    f = open(economic_indicators_path + "/" + filename + ".txt", 'w')
    # {"date" : expect[0], "time" : time, "expect" : expect[1], "result" : result[1], "is_summertime" : is_summertime}
    f.write("date"+seq+"time"+seq+"expect"+seq+"result\n")
    for x in data:
        f.write(str(x["date"].strftime('%Y/%m/%d'))+seq+str(x["time"])+seq+str(x["expect"])+seq+str(x["result"])+"\n")
    f.close