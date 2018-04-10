#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import web.URL as Url
from logManager import log


def retry_action(retry_num=3):
    # 错误自动重试, retry_num 重试次数
    def decorator(fun):

        def wrapper(self, count=0, *args, **kwargs):
            try:
                return fun(self, *args, **kwargs)
            except requests.exceptions.ConnectionError:
                log.error('{} 不存在'.format(self._url))
            except Exception as e:
                if count < retry_num:
                    count += 1
                    log.info("{}: 第{}次重试".format(self._url, count))
                    time.sleep(1)
                    return wrapper(self, count, *args, **kwargs)
                else:
                    raise Exception(e)

        return wrapper

    return decorator


class Download:
    # _UA = 'Mozilla/5.0 (compatible; Baiduspider/2.0;+http://www.baidu.com/search/spider.html)'
    _UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'

    def __init__(self, url, path='', headers=None, timeout=10):
        self._url = url
        self._path = path
        if headers is None:
            self._headers = {'User-Agent': self._UA}
        else:
            self._headers = headers

        self._timeout = timeout
        self._response = self.__get()

    # @retry_action()
    def __download(self):
        return requests.get(self._url, headers=self._headers, timeout=self._timeout)

    def __get(self):
        self._url = Url.check(self._url)
        if self._url is None:
            return False
        self._url = self._url + self._path

        # log.info('正在获取 {}'.format(self._url))
        try:
            return self.__download()
        except Exception as e:
            log.error('{} 获取失败! 错误信息: {}'.format(self._url, e.args))

    def get_response(self):
        return self._response

    def get_status_code(self):
        if self._response is None:
            return None
        return self._response.status_code

    def result(self):
        if self.get_status_code() != 200:
            return

        return {'html': self._response.text, 'status_code': self.get_status_code()}

    def __str__(self):
        if self._response is None:
            return '{} 获取失败'.format(self._url)
        return '{} 状态码: {}'.format(self._url, self._response.status_code)


if __name__ == '__main__':
    print(Download('www.baidu.com').get_response())
