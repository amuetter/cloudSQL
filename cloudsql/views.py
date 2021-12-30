from flask import request, jsonify, abort
import json

from . import sql as db
from . import utilities as ut

from . import auth


@auth.request_is_authenticated
def tables():
    conn = db.get_db()
    
    if request.method == 'GET':
        tables = conn.get_tables()
        return jsonify(tables)

    if request.method == 'POST':
        data = json.loads(request.data)
        name = data['name']
        schema = data['schema']
        conn.create(name, schema)

        return '', 200


@auth.request_is_authenticated
def table(name):
    
    conn = db.get_db()

    if name in conn.get_tables():

        if request.method == 'GET':

            columns, args = ut.parse_args(request.args)
            result = conn.select(name, columns, args)
            
            return jsonify(result)

        if request.method == 'POST':
            data = json.loads(request.data)
            conn.insert(name, data)
            return '', 200

        if request.method == 'DELETE':
            conn.drop(name)
            return ''

    else:
        abort(404)

