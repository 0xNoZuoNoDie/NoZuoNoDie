# -*- coding: utf-8 -*-
from config import THREAD_NUM, REDIS_POOL
from logManager import log
from threading import Thread
import redis
from tasks.cms_search import cms_search


class Spider(Thread):
    def __init__(self):
        self.conn = redis.Redis(connection_pool=REDIS_POOL)
        super(Spider, self).__init__()

    def save_to_db(self, url, r):
        while True:
            if r.ready():
                result = r.result
                log.info('{:30} 查询结果: {}'.format(url, result.__repr__()))
                break
                # if result:
                #     log.info('{:30} CMS为: {}'.format(url, result))

    def run(self):
        while True:
            task = self.conn.blpop('cms_task', 0)[1]
            # log.info('启动任务: {}'.format(task))
            if task:
                r = cms_search.delay(task)
                self.save_to_db(task, r)


def run():
    all_thd = []
    for _ in range(THREAD_NUM):
        log.info('正在启动线程 {}'.format(_))
        t = Spider()
        all_thd.append(t)
        t.daemon = True
        t.start()

    for t in all_thd:
        t.join()


if __name__ == '__main__':
    run()
