# -*- coding: utf-8 -*-

# ------------------ Python2/3兼容 -----------------------
from __future__ import unicode_literals

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import six
# ------------------ Python2/3兼容 -----------------------

import tldextract
import hashlib


def is_empty(fun):
    def wrapper(url, *args, **kwargs):
        # url 是否为空, 为空返回真, 不为空返回假
        if url is None:
            return None
        return fun(url, *args, **kwargs) if isinstance(url + '', six.text_type) and len(url) != 0 else None

    return wrapper


def clean(url):
    url = check(url)

    if url is None:
        return
    tld = tldextract.extract(url)
    if tld.suffix == '':
        return
    if tld.subdomain == '':
        return '{}.{}'.format(tld.domain, tld.suffix)
    return '{}.{}.{}'.format(tld.subdomain, tld.domain, tld.suffix)


@is_empty
def check(url):
    if not url.startswith('http://') and not url.startswith('https://'):
        # 默认为 http://
        url = 'http://' + url

    if not url.endswith('/'):
        url = url + '/'
    return url


def get_domain(url):
    # 获取顶级域名
    url = clean(url)

    if url is None:
        return None

    tld = tldextract.extract(url)
    return '{}.{}'.format(tld.domain, tld.suffix)


def get_md5(url):
    # 获取 URL 的md5 值
    # url 格式统一
    url = clean(url)

    if url is None:
        return None, None

    try:
        return url, hashlib.md5(url).hexdigest()
    except TypeError:
        return url, hashlib.md5(url.encode('utf8')).hexdigest()
    except UnicodeEncodeError:
        return url, hashlib.md5(url.encode('utf8')).hexdigest()


if __name__ == '__main__':
    print(get_md5('javascript:void(0);'))
