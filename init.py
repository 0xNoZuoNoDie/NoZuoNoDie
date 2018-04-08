# -*- coding: utf-8 -*-
from db import file_import
from config import ROOT_DIR
import os


def create_echart_db():
    file_import(os.path.join(ROOT_DIR, 'sql/echart.sql'))


def create_domain_db():
    pass


if __name__ == '__main__':
    create_echart_db()
