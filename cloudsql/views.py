from flask import request, jsonify, abort
import json
import sqlite3

from . import sqlite as db


def tables(context):

    conn = db.get_db(context['sqlitepath'])
    
    if request.method == 'GET':
        tables = db.get_tables(conn)
        return jsonify(tables)

    if request.method == 'POST':
        data = json.loads(request.data)
        name = data['name']
        schema = data['schema']
        string_schema = ", ".join(list(map(lambda x: f"{x[0]} {x[1]}", schema)))
        query = f"CREATE TABLE {name} ({string_schema});"
        conn.execute(query)
        return '', 200


def table(name, context):
    
    conn = db.get_db(context['sqlitepath'])

    if name in db.get_tables(conn):

        if request.method == 'GET':
            query = f"SELECT * FROM {name};"

            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(query)
            
            result = []
            for row in c.fetchall():
                result.append(dict(row))
            
            return jsonify(result)

        if request.method == 'POST':
            data = json.loads(request.data)
            values = data['values']
            query = f'''INSERT INTO {name} ({", ".join([k for k in values.keys()])}) VALUES ({", ".join(['?' for _ in values])})'''
            c = conn.cursor()
            c.execute(query, list(values.values()))
            conn.commit()
            return '', 200

        if request.method == 'DELETE':
            query = f"DROP TABLE {name};"
            c = conn.cursor()
            c.execute(query)
            return ''

    else:
        abort(404)

