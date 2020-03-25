#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
from shapely.geometry import Point, shape
from flask import Flask
from flask import render_template, request, jsonify
import json
import sqlite3

df_clean = pd.read_csv('bees.csv').iloc[:, 1:]

app = Flask(__name__)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/data")
def get_data():

    df_clean = pd.read_csv('bees.csv').iloc[:, 1:]

    return df_clean.to_json(orient='records')


@app.route("/api/v1/resources/bees/all", methods=['GET'])
def api_all_bees():
    conn = sqlite3.connect('resources.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_bees = cur.execute('SELECT * FROM BEES;').fetchall()

    return jsonify(all_bees)


@app.route("/api/v1/resources/temperature/all", methods=['GET'])
def api_all_temps():
    conn = sqlite3.connect('resources.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_temps = cur.execute('SELECT * FROM TEMPS;').fetchall()

    return jsonify(all_temps)


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/resources/bees', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
        if id >= len(df_clean.index):
            return " Error: the highest index is " + str(len(df_clean.index)-1) + ". Try a lower index."
    else:
        return "Error: No id field provided. Please specify an id."

    return df_clean.iloc[[id]].to_json(orient='records')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
