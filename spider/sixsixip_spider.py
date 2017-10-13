#!/usr/bin/env python
# encoding: utf-8
from bs4 import BeautifulSoup

from log import logger
from proxy import Proxy_IP
from spider.base_spider import BaseSpider
from tool import fetch


class SixsixipSpider(BaseSpider):
    def __init__(self):
        super(SixsixipSpider,self).__init__()
        urls = ["http://www.66ip.cn/{}.html".format(k) for k in range(1, 10)]
        for url in urls:
            self.url_list.put(url)

    def parse_ip_proxy(self, url):
        fetch_result = fetch(url)
        response = fetch_result['response']
        response.encoding = 'gbk'
        html = response.text
        soup = BeautifulSoup(html, "html5lib")
        trs = soup.find('div', id="main").find('tbody').find_all('tr')[1:]
        for tr in trs:
            tds = tr.find_all('td')
            ip_and_port = tds[0].string + ":" + tds[1].string
            self.proxy_list.add(Proxy_IP(ip_and_port=ip_and_port))
            logger.info(self.__class__.__name__+" "+ip_and_port)

    def run(self):
        self.pool.spawn(self.list_loop)
        self.pool.join()


if __name__ == "__main__":
    spider = SixsixipSpider()
    spider.run()
