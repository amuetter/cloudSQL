from flask import Flask, jsonify, g, abort
import DBInterface as db

import settings


app = Flask(__name__)


@app.route("/")
def base():
    return "source"

@app.route("/tables")
def get_tables():
    conn = db.get_db(settings.DATABASE)
    tables = []
    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
       tables.append(row[0])
    return jsonify(tables)

@app.route('/table/<name>')
def table(name):
    print(get_tables().json)
    if name in get_tables().json:
        conn = db.get_db(settings.DATABASE)
        query = f"SELECT * FROM {name};"
        result = []
        for row in conn.execute(query).fetchall():
            result.append(row)
        return jsonify(result)
    else:
        abort(404)

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(Exception)
def handle_error(e):
    return jsonify(error=str(e))

if __name__ == "__main__":
    app.run(debug=True)