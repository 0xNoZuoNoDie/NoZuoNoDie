# -*- coding: utf-8 -*-
from __future__ import absolute_import
import redis
import os
import pymysql
import json
from DBUtils.PooledDB import PooledDB

REDIS_MD5_TEMP_NAME = 'old_urls'

CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
BROKER_URL = 'redis://127.0.0.1:6379/0'

CELERY_IMPORTS = ('tasks.tasks', 'tasks.cms_search')

# 数据库配置
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'qweasd',
    'charset': 'utf8'
}

REDIS_CONFIG = {
    'host': 'localhost',
    'port': 6379,
    'decode_responses': True,
    'db': 0
}

POOL = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=5,  # 链接池中最多闲置的链接，0和None不限制
    maxshared=3,
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    ping=0,
    host='127.0.0.1',
    port=3306,
    user='root',
    password='qweasd',
    database='Domain',
    charset='utf8'
)

# host是redis主机，需要redis服务端和客户端都起着 redis默认端口是6379
REDIS_POOL = redis.ConnectionPool(**REDIS_CONFIG)

# 线程配置
THREAD_NUM = 20  # 线程数

# 项目根目录配置
ROOT_DIR = os.path.dirname(os.path.abspath(__name__))

# start CMS指纹配置
# CMS识别指纹 文件路径
CMS_FILE_PATH = os.path.join(ROOT_DIR, 'data/cms.json')
# 读取指纹数据
file_hand = open(CMS_FILE_PATH, 'r')
CMS_DATA = json.loads(file_hand.read())
file_hand.close()
# end CMS指纹配置
