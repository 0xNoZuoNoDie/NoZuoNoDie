# -*- coding: utf-8 -*-

import pymysql
from logManager import log
from config import MYSQL_CONFIG


class OpenMysqlConn:
    def __init__(self, db=None):
        self._db = db
        self.conn = None

    def __enter__(self):
        try:
            self.conn = pymysql.connect(db=self._db, **MYSQL_CONFIG)
            if self.conn:
                return self.conn.cursor()
        except (AttributeError, pymysql.OperationalError) as e:
            log.exception('连接数据库失败')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.commit()
            self.conn.close()


def file_import(file_path, db=None):
    log.info('正在向数据库导入 {} 文件'.format(file_path))
    with OpenMysqlConn(db) as cursor:
        with open(file_path, 'r') as file_hand:
            for sql in file_hand.read().split(';'):
                if sql == '\n':
                    continue
                log.info('执行SQL: {}'.format(sql))
                cursor.execute(sql)


if __name__ == '__main__':
    file_import('./sql/echart.sql')
