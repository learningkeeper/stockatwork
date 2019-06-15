# -*- coding: utf-8 -*-
import time
import stockmodule as m
def sclick():
    slist = m.get_setting()
    cnt = len(slist)

    log1 = []
    for i in range(cnt):
        log1.append('')

    for i in range(cnt):
        time.sleep(0.5)
        sid, low, high = slist[i]
        name, price = m.get_price(sid)
        info =  str(name) + '  ' + str(price) 
        #act, why = m.get_best(sid)
        log1[i] = info  #+ str(act) + "\n" + str(why)
    return log1
        

