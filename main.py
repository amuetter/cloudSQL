from flask import Flask, jsonify, g, abort, request
import json

import DBInterface as db
import settings


app = Flask(__name__)


@app.route("/")
def base():
    return "source"


@app.route("/tables", methods=['GET', 'POST'])
def tables():
    conn = db.get_db(settings.DATABASE)
    if request.method == 'GET':
        tables = db.get_tables(conn)
        return jsonify(tables)

    if request.method == 'POST':
        data = json.loads(request.data)
        name = data['name']
        schema = data['schema']
        string_schema = ", ".join(list(map(lambda x: f"{x[0]} {x[1]}", schema)))
        query = f"CREATE TABLE {name} ({string_schema});"
        conn = db.get_db(settings.DATABASE)
        a = conn.execute(query)
        return '', 200


@app.route('/table/<name>', methods=['GET', 'PUT', 'DELETE'])
def table(name):
    conn = db.get_db(settings.DATABASE)
    if name in db.get_tables(conn):
        if request.method == 'GET':
            
            query = f"SELECT * FROM {name};"
            result = []
            for row in conn.execute(query).fetchall():
                result.append(row)
            return jsonify(result)

        if request.method == 'PUT':
            data = json.loads(request.data)
            # TODO insert into table values
            return '', 200

        if request.method == 'DELETE':
            query = f"DROP TABLE {name};"
            a = conn.execute(query)
            return ''

    else:   
        abort(404)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(Exception)
def handle_error(e):
    print(e)
    return jsonify(error=str(e))


"""
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_exception(e):
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == "__main__":
    app.run(debug=True)
"""