# -*- coding: utf-8 -*-

from __future__ import absolute_import

from tasks.celery import app
from web.downloads import Download
from lxml import etree
import web.URL as URL
from config import REDIS_POOL, REDIS_MD5_TEMP_NAME
from datetime import timedelta
from db import OpenMysqlConn
import redis
import time

r = redis.Redis(connection_pool=REDIS_POOL)


@app.task
def get_urls(url):
    new_urls = []
    d = Download(url)
    result = html_parse(d.get_response())

    for url in result:
        status, url = url_is_exist(url)
        if status:
            continue
        new_urls.append(url)
    return new_urls


def html_parse(res):
    # html 解析获取url
    result = []
    try:
        html = etree.HTML(res.text)
        for new_url in html.xpath('//a/@href'):
            result.append(URL.clean(new_url))
    except AttributeError:
        return list()
    except ValueError:
        return list()

    return list(set(result))


def url_is_exist(url):
    url, md5 = URL.get_md5(url)
    if md5 is None:
        return True, url

    # print('{:50}{}'.format(url, md5))
    if r.hget(REDIS_MD5_TEMP_NAME, md5) == 'True':
        return True, url

    domain = URL.get_domain(url)
    if domain is None:
        return True, url

    if not r.hexists('domain', domain):
        r.hset('domain', domain, 1)
        return False, url

    if int(r.hget('domain', domain)) > 50:
        return True, url

    r.hset('domain', domain, int(r.hget('domain', domain)) + 1)
    # print('domain: {}, num: {}'.format(domain, r.hget('domain', domain)))
    r.hset(REDIS_MD5_TEMP_NAME, md5, True)
    return False, url


@app.task
def save_to_db():
    r = redis.Redis(connection_pool=REDIS_POOL)
    num = r.hlen(REDIS_MD5_TEMP_NAME)
    # 获取系统时间（只取分:秒）
    t = time.strftime('%H:%M:%S', time.localtime())
    sql = 'INSERT INTO `spider` (`id`, `insert_time`, `num`) VALUES (NULL, \'{}\', \'{}\'); '
    query = 'SELECT * from spider ORDER BY id DESC limit 1;'
    with OpenMysqlConn('echart') as cursor:
        if cursor.execute(query) == 0:
            cursor.execute(sql.format(t, num))
        else:
            temp_num = r.get('mysql_temp')
            result = num - (0 if temp_num is None else int(temp_num))
            cursor.execute(sql.format(t, result))
    r.set('mysql_temp', num)


app.conf.update(
    timezone='Asia/Shanghai',
    enable_utc=True,
    CELERYBEAT_SCHEDULE={
        'save_to_db_1': {
            'task': 'tasks.tasks.save_to_db',
            'schedule': timedelta(seconds=5),
        }
    }
)
