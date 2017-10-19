#!/usr/bin/env python
# encoding: utf-8
import random

from bs4 import BeautifulSoup
from peewee import fn

from log import logger
from proxy import Proxy_IP
from spider.base_spider import BaseSpider
from tool import fetch


class XicidailiSpider(BaseSpider):
    def __init__(self):
        super(XicidailiSpider, self).__init__()
        urls = ["http://www.xicidaili.com/wn/{}".format(k) for k in range(1, 100)]
        for url in urls:
            self.url_list.put(url)
        self.proxypool = Proxy_IP.select().where(Proxy_IP.type == 'http')

    def parse_ip_proxy(self, url):
        proxy = random.choice(self.proxypool)
        fetch_result = fetch(url, proxy)
        response = fetch_result['response']
        if not response:
            logger.info('response is None , url:{}'.format(url))
            return
        response.encoding = 'utf-8'
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        trs = soup.find('table', id="ip_list").find('tbody').find_all('tr')[1:]
        for tr in trs:
            tds = tr.find_all('td')
            ip_and_port = tds[1].string + ":" + tds[2].string
            proxy = Proxy_IP(ip_and_port=ip_and_port, type='https')
            if tds[4].string == '高匿':
                proxy.anonymity = 'high_anonymity'
            elif tds[4].string == '透明':
                proxy.anonymity = 'transparent'
            proxy.country = 'China'
            self.proxy_list.add(proxy)
            logger.info(self.__class__.__name__ + " " + ip_and_port + " " + proxy.anonymity)

    def run(self):
        self.pool.spawn(self.list_loop)
        self.pool.join()


if __name__ == "__main__":
    spider = XicidailiSpider()
    spider.run()
