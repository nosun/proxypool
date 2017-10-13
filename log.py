#!/usr/bin/env python
# encoding: utf-8

import logging
from logging.handlers import SMTPHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 输出到控制台的log等级的开关
# 创建该handler的formatter
logger_format = logging.Formatter(
        fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
console_handler.setFormatter(logger_format)
logger.addHandler(console_handler)
mail_handler = SMTPHandler(
    mailhost='smtp.163.com',
    fromaddr='nghuyong@163.com',
    toaddrs='1013975672@qq.com',
    subject='这是一封proypool项目发来的邮件',
    credentials=('nghuyong', 'huyong199596'))

mail_handler.setLevel(logging.ERROR)
mail_handler.setFormatter(logger_format)
logger.addHandler(mail_handler)

