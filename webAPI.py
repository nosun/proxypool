#!/usr/bin/env python
# encoding: utf-8
import json

import time

import web
from log import logger
from proxy import Proxy_IP

urls = (
    '/', 'index'
)

app = web.application(urls, globals())


class index:
    def GET(self):
        get_input = web.input(_method='get')
        query_country = query_anonymity = None
        query_number = 100
        try:
            query_country = get_input.country
        except:
            pass
        try:
            query_anonymity = get_input.anonymity
        except:
            pass
        try:
            query_number = get_input.number
        except:
            pass
        proxies = Proxy_IP.select().order_by(Proxy_IP.timestamp)
        updatetime = str(proxies[0].timestamp).split('.')[0]
        data = []
        anonymity_level = {
            "transparent": 0,
            "anonymity": 1,
            "normal_anonymity": 1,
            "high_anonymity": 2
        }
        for proxy in proxies:
            if query_country:
                if proxy.country != query_country:
                    continue
            if query_anonymity:
                print(query_anonymity)
                if anonymity_level[proxy.anonymity] < anonymity_level[query_anonymity]:
                    continue
            one_proxy_data_dic = {"ip_and_port": proxy.ip_and_port, "country": proxy.country, "type": proxy.type,
                                  "anonymity": proxy.anonymity, "round_trip_time": proxy.round_trip_time}
            data.append(one_proxy_data_dic)
        if query_number < len(data):
            data = data[0:query_number]
        return_dic = {"num": len(data), "updatetime": updatetime, "data": data}
        return json.dumps(return_dic)


if __name__ == "__main__":
    app.run()
