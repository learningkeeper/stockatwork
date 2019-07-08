# -*- coding: utf-8 -*-
import sys
sys.path.append('/anaconda3/lib/python3.7/site-packages')
import twstock
import requests
import s0056 

def getpw(file):
    with open(file) as fh:
        fh = fh.read()
        return fh.strip()

def get_setting():
    res = []
    try:
        with open('./stock.txt') as fh:
            for i in fh:
                s = i.split(',')
                res.append([s[0].strip(), s[1].strip(), s[2].strip()])
    except :
        print('Fail to open stock.txt ')
    return res

def get_price(stockid):
    rt = twstock.realtime.get(stockid)
    if rt['success']:
        return (rt['info']['name'], float(rt['realtime']['latest_trade_price']))
    else:
        return (False, False)

def get_best(stockid):
    stock = twstock.Stock(stockid)
    bp = twstock.BestFourPoint(stock).best_four_point()
    if(bp):
        return ('買進' if bp[0] else '賣出', bp[1])
    else:
        return (False, False)

def send_ifttt(v1, v2, v3):
    url = ( 'https://maker.ifttt.com/trigger/stockgo/with/key/' + 
            getpw('stockgotoken.passwd') + 
            '?value1=' + str(v1) +
            '&value2=' + str(v2) +
            '&value3=' + str(v3))
    r = requests.get(url)
    if r.text[:5] == 'Congr':
        print('send out')
    return r.text

def check_stock_send():
    log1 = []
    log2 = []
    slist = get_setting()
    cnt = len(slist)
    for i in range(cnt):
        log1.append('')
        log2.append('')
    
    for i in range(cnt):
        sid, low, high = slist[i]
        name, price = get_price(sid)
        #print(' Checking:', name, 'Price:', price, 'Price Range' ,low, '~', high)
        if float(price) <= float(low):
            if log1[i] != '買進':
                send_ifttt(name, price, '買進 （股價低於' + str(low) + ')')
                log1[i] = '買進'
        elif float(price) >= float(high):
            if log1[i] != '賣出':
                send_ifttt(name, price, '買進 （股價高於' + str(high) + ')')
                log1[i] = '賣出'
        act, why = get_best(sid)
        log2.append(name + str(price) + act + ' (' + why + ')')
    flag, msg1, msg2 = s0056.send_info(2)
    if flag == 1:
        send_ifttt('0056爆大量', msg1, msg2)
    return log2

