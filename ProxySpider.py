#!/usr/bin/env python
# encoding: utf-8
from gevent import monkey

monkey.patch_all()
from check_proxy import Check_proxy
from log import logger
from db import db_init
from spider.proxylists_spider import ProxylistSpider
from spider.sixsixip_spider import SixsixipSpider
from gevent.pool import Pool


class ProxySpider:
    def __init__(self):
        self.pool = Pool(size=100)
        self.proxies = set()
        self.spider_list = [ProxylistSpider, SixsixipSpider]

    def add_spider(self, Spider):
        spider = Spider()
        spider.run()
        for proxy in spider.proxy_list:
            self.proxies.add(proxy)
        logger.info("{}抓取完毕，抓取proxy{}个".format(spider.__class__.__name__, len(spider.proxy_list)))

    def run(self):
        for Spider in self.spider_list:
            self.pool.spawn(self.add_spider, Spider)
        self.pool.join()


if __name__ == "__main__":
    db_init()
    proxyspider = ProxySpider()
    proxyspider.run()
    check_proxy = Check_proxy()
    check_proxy.proxies.extend(proxyspider.proxies)
    check_proxy.run()
