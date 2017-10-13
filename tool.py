#!/usr/bin/env python
# encoding: utf-8
import random

import requests
import time

from proxy import Proxy_IP
from setting import USER_AGENT_LIST, TIME_OUT, RETRY_NUM


def fetch(url, proxy=None):
    kwargs = {
        "headers": {
            "User-Agent": random.choice(USER_AGENT_LIST),
        },
        "timeout": TIME_OUT,
    }
    response = None
    retry_num = start = end = 0
    for i in range(RETRY_NUM):
        try:
            if proxy is not None:
                kwargs["proxies"] = {
                    "http": str(proxy)}
            start = time.time()
            response = requests.get(url, **kwargs)
            end = time.time()
            break
        except Exception as e:
            time.sleep(1)
            retry_num += 1
            continue
    return {"response": response, "retry_num": retry_num, "round_trip_time": round((end - start), 2)}


if __name__ == "__main__":
    check_anonymity_url = "http://www.xxorg.com/tools/checkproxy/"
    fetch_result = fetch(check_anonymity_url, Proxy_IP(ip_and_port="194.246.105.52:53281"))
    print(fetch_result)
