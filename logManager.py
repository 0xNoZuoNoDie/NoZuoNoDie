# -*- coding=utf-8 -*-
import logging

logging.basicConfig(
    format='%(name)s[%(levelname)s/%(process)d]:%(asctime)s:%(module)s.%(funcName)s.%(lineno)d - %(message)s')

log = logging.getLogger("Scanner")
log.setLevel(logging.INFO)
flask_log = logging.getLogger("werkzeug")
flask_log.setLevel(logging.INFO)
# log.addHandler(logging.StreamHandler())
