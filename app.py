# -*- coding: utf-8 -*-
from __future__ import absolute_import

from db import OpenMysqlConn
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)


def query_db(query, one=False):
    with OpenMysqlConn('echart') as cursor:
        cur = cursor.execute(query)
        rv = cursor.fetchall()
        return (rv[0] if rv else None) if one else rv


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/get_urls_number", methods=["POST"])
def get_urls_number():

    if request.method == "POST":
        res = query_db("SELECT * FROM spider WHERE id>=({})".format(int(request.form['id']) + 1, ))  # 返回1条或多条数据

    return jsonify(insert_time=[x[1] for x in res], num=[x[2] for x in res], )


if __name__ == '__main__':
    app.run(debug=True)
