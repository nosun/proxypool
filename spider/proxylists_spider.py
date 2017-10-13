#!/usr/bin/env python
# encoding: utf-8
import re

from log import logger
from proxy import Proxy_IP
from setting import IP_PROXY_REGEX
from spider.base_spider import BaseSpider
from tool import fetch


class ProxylistSpider(BaseSpider):
    """
    http://www.proxylists.net/
    """

    def __init__(self):
        super(ProxylistSpider, self).__init__()
        self.start_url = "http://www.proxylists.net/"

    def parse_ip_proxy(self, response):
        html = response.text
        for proxy in re.findall(IP_PROXY_REGEX, html):
            self.proxy_list.add(Proxy_IP(ip_and_port=proxy[0]))
            logger.info(self.__class__.__name__ + " " + proxy[0])

    def run(self):
        fetch_result = fetch(self.start_url)
        response = fetch_result['response']
        if response:
            self.parse_ip_proxy(response)


if __name__ == "__main__":
    proxylistSpider = ProxylistSpider()
    proxylistSpider.run()
    print(len(proxylistSpider.proxy_list))
