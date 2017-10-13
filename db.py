#!/usr/bin/env python
# encoding: utf-8
import datetime

from peewee import DoesNotExist

from log import logger
from proxy import Proxy_IP, proxypool_database


def db_init():
    proxypool_database.connect()
    proxypool_database.create_table(Proxy_IP, safe=True)


def save_proxy_to_db(proxy):
    try:
        saved_proxy = Proxy_IP.get(Proxy_IP.ip_and_port == proxy.ip_and_port)
        saved_proxy.round_trip_time = proxy.round_trip_time
        saved_proxy.anonymity = proxy.anonymity
        saved_proxy.country = proxy.country
        saved_proxy.timestamp = datetime.datetime.now()
        if saved_proxy.save() == 1:
            logger.info("{} updated into database".format(saved_proxy))
    except DoesNotExist:
        if proxy.save() == 1:
            logger.info("{} saved into database".format(proxy))


def delete_proxy_from_db(proxy):
    try:
        saved_proxy = Proxy_IP.get(Proxy_IP.ip_and_port == proxy.ip_and_port)
        if saved_proxy.delete_instance() == 1:
            logger.info("{} deleted from database".format(proxy))
    except DoesNotExist:
        pass


if __name__ == "__main__":
    pass
