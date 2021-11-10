from flask import g, jsonify

from . import views as v


class CloudSQL():

    def __init__(self, dbpath, url_prefix=''):
        self.url_prefix = url_prefix
        self.db_context = {'sqlitepath': dbpath}


    def serve(self, app):
        
        @app.route(f'{self.url_prefix}/tables', methods=['GET', 'POST'])
        def tables():
            return v.tables(self.db_context)

        @app.route(f'{self.url_prefix}/table/<name>', methods=['GET', 'POST', 'DELETE'])
        def table(name):
            return v.table(name, self.db_context)

        @app.teardown_appcontext
        def close_connection(exception):
            db = getattr(g, '_database', None)
            if db is not None:
                db.close()

        @app.errorhandler(Exception)
        def handle_error(e):
            print(e)
            return jsonify(error=str(e))
