# -*- coding: utf-8 -*-
from tasks.tasks import get_urls
import time
import redis
from config import REDIS_POOL, THREAD_NUM, POOL
from logManager import log
from threading import Thread


class Spider(Thread):
    def __init__(self):
        self.conn = redis.Redis(connection_pool=REDIS_POOL)
        super(Spider, self).__init__()

    def get_result(self, url, r):
        while True:
            if r.ready():
                try:
                    result = r.result
                    log.info('{:30} 查询共获取到: {}'.format(url, len(result)))
                    for new_url in result:
                        self.conn.lpush('task', new_url)
                    conn = POOL.connection()
                    cursor = conn.cursor()
                    _sql = 'INSERT INTO Domain (domain) VALUES (%s);'
                    cursor.executemany(_sql, result)
                    conn.commit()
                    conn.close()
                finally:
                    break
            time.sleep(1)

    def run(self):
        while True:
            task = self.conn.blpop('task', 0)[1]
            # log.info('启动任务: {}'.format(task))
            if task:
                r = get_urls.delay(task)
                self.get_result(task, r)


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
