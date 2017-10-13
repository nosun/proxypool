#!/usr/bin/env python
# encoding: utf-8
from gevent import monkey
monkey.patch_all()
import random
import requests
from setting import USER_AGENT_LIST, TIME_OUT
import abc
from gevent.pool import Pool
from gevent.queue import Queue


class BaseSpider:
    def __init__(self, start_url=None):
        self.start_url = start_url
        self.proxy_list = set()
        self.pool = Pool(size=10)
        self.url_list = Queue()

    def list_loop(self):
        while not self.url_list.empty():
            url = self.url_list.get()
            self.pool.spawn(self.parse_ip_proxy, url)

    @abc.abstractmethod
    def parse_ip_proxy(self, url):
        pass

    @abc.abstractmethod
    def run(self):
        pass
