import twstock
import json
import datetime
import logging
import logging.config
import time
import re
#logging.config.fileConfig(fname='logging_config.ini',
#                          disable_existing_loggers=False)
#logger = logging.getLogger(__name__)

currentmonth = datetime.datetime.now().month
startmonth = datetime.datetime.now().month - 1
currentyear= datetime.datetime.now().year
lastyear = currentyear -1


class RoundTripEncoder(json.JSONEncoder):
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return {
                "_type": "datetime",
                "value": obj.strftime("%s %s" % (
                    self.DATE_FORMAT, self.TIME_FORMAT
                ))
            }
        return super(RoundTripEncoder, self).default(obj)

def fetch_data(year, month):
    data = twstock.Stock('0056')
    with open('0056.txt', 'a+') as fh:
        content = json.dumps(data.fetch(year, month), cls=RoundTripEncoder)
        #logger.info(f"Fetch {year} {month}")
        fh.write(content)
        fh.write('\n')

def past_year_data():
    with open('0056.txt', 'w') as fh:
        fh.write('')
    for i in range(startmonth, 13):
        fetch_data(lastyear, i)
        time.sleep(60)
    for i in range(1, currentmonth):
        fetch_data(currentyear, i)
        time.sleep(60)

def check_update_data():
    with open('0056.txt') as fh:
        content = json.loads(fh.readlines()[-1])[0][0]['value']
        content = datetime.datetime.strptime(content, "%Y-%m-%d %H:%M:%S")
        if content.year !=  currentyear and content.month + 1 != curent.month:
            past_year_data()

def get_capacity_average(base=2):
    with open('0056.txt') as fh:
        days = 0
        capacity = 0
        for month in fh.readlines():
            content = json.loads(month)
            days += len(content)
            for day in content:
                capacity +=  int(day[1])
    return int(capacity/days/1000) * base

def send_info(base):
    check_update_data()
    now_p = twstock.realtime.get('0056')['realtime']['latest_trade_price']
    now_c = twstock.realtime.get('0056')['realtime']['accumulate_trade_volume']
    average_c = get_capacity_average(base)
    msg1 = f"0056 目前價位{now_p}"
    msg2= f"今天成交量{now_c}\n ，{base} 倍成交量{average_c}"
    if int(now_c) > average_c :
        return 1, msg1, msg2
    return 0, msg1, msg2

if __name__ == '__main__':
    print(send_info(2))

