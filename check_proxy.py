#!/usr/bin/env python
# encoding: utf-8
import time
from simplejson import JSONDecodeError

import requests
from bs4 import BeautifulSoup
from gevent import monkey
from requests.exceptions import ProxyError
from db import delete_proxy_from_db, save_proxy_to_db
from proxy import Proxy_IP
from tool import fetch

monkey.patch_all()
from gevent.pool import Pool


class Check_proxy:
    def __init__(self):
        self.pool = Pool(20)
        self.recheck = False
        self.proxies = []

    def _check_one_proxy(self, proxy):
        check_anonymity_url = "http://www.xxorg.com/tools/checkproxy/"
        fetch_result = fetch(check_anonymity_url, proxy)
        response = fetch_result['response']
        if response is None:
            if self.recheck:
                delete_proxy_from_db(proxy)
            return
        response.encoding = 'utf-8'
        html = response.text
        result = BeautifulSoup(html, "html5lib").find("div", id="result")
        anonymities = {"透明": "transparent",
                       "普通匿名": "normal_anonymity",
                       "高匿名": "high_anonymity"
                       }
        for anonymity in anonymities.keys():
            if anonymity in str(result):
                proxy.anonymity = anonymities[anonymity]
                check_address_url = "http://ip-api.com/json/"
                fetch_result = fetch(check_address_url, proxy)
                response = fetch_result['response']
                if response is None:
                    if self.recheck:
                        delete_proxy_from_db(proxy)
                    return
                try:
                    proxy.country = response.json()['country']
                    proxy.round_trip_time = fetch_result['round_trip_time']
                    save_proxy_to_db(proxy)
                except JSONDecodeError:
                    delete_proxy_from_db(proxy)
                    return
                break

    def run(self, ):
        for proxy in self.proxies:
            self.pool.spawn(self._check_one_proxy, proxy)
        self.pool.join()


if __name__ == "__main__":
    logger.info("-------Recheck Start-------")
    check_proxy = Check_proxy()
    check_proxy.recheck = True
    proxies = Proxy_IP.select()
    check_proxy.proxies.extend(proxies)
    check_proxy.run()
    logger.info("-------Recheck Finish-------")
