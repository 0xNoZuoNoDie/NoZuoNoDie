# -*- coding: utf-8 -*-
from __future__ import absolute_import

from config import CMS_DATA
from web.downloads import Download
from tasks.celery import app


def search(r, body):
    # 正则匹配
    if body.find(r) != -1:
        return True
    else:
        return False


@app.task
def cms_search(url):
    # cms 识别
    for data in CMS_DATA:
        d = Download(url, path=data['url'])
        result = d.result()
        print(d)
        if result is None:
            return

        if len(data['re']) != 0:
            if isinstance(data['re'], list):
                for r in data['re']:
                    if search(r, result['html']):
                        return data['name'], data['url']
                    continue
            else:
                if search(data['re'], result['html']):
                    return data['name'], data['url']
                continue
        else:
            # md5 验证
            pass

    return None
