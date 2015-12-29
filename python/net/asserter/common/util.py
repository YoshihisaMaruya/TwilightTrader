__author__ = 'rv'
__author_email__ = "m0029.swim@gmail.com"
__date__ = "2015-12-28"
__version__ = "0.1"

import pytz
import configparser
import logging
import os
import inspect

logging.basicConfig(filename=os.getenv('TT_HOME') + '/log/twilight_trader.log', level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')
economic_indicators_path = os.getenv('TT_HOME') + '/data/economic_indicator'
common_config_path = os.getenv('TT_HOME') + '/config/common.ini'

class Log:
    @staticmethod
    def __get_frame_info():
      callerframerecord = inspect.stack()[2]    # 0 represents this line
                                                # 1 represents line at caller
      frame = callerframerecord[0]
      info = inspect.getframeinfo(frame)
      return '"filename": {filename}, "function": {function}, "lineno": {lineno}"'.\
          format(filename=info.filename,function=info.function,lineno=info.lineno)

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def error(tag, message):
        logging.error(Log.__get_frame_info() + "," + message)


class IO:
    @staticmethod
    def read_config(key1, key2):
        Log.info("load config from: " + common_config_path)
        Log.info("key1, key2: " + key1 + "," + key2)
        config = configparser.ConfigParser()
        config.read(common_config_path)
        return config[key1][key2]


class Datetime:
    @staticmethod
    def is_summertime(d):
        tz_jst = pytz.timezone("Asia/Tokyo")
        tz_est = pytz.timezone("US/Eastern")
        t_jst = tz_jst.localize(d)
        t_jst.astimezone(tz_est)
        tm_isdst = t_jst.astimezone(tz_est).timetuple().tm_isdst
        return tm_isdst
