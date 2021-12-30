from flask import g, jsonify

from cloudsql.sql import set_db_context

from . import views as v



class CloudSQL():

    def __init__(self, db_type, db_conn_string, url_prefix='', api_key=None):
        self.url_prefix = url_prefix
        self.db_context = {'db_type': db_type, 'db_conn_string': db_conn_string}
        if api_key:
            self.db_context['api_key'] = api_key


    def serve(self, app):
        
        @app.route(f'{self.url_prefix}/tables', methods=['GET', 'POST'])
        def tables():
            set_db_context(self.db_context)
            return v.tables()

        @app.route(f'{self.url_prefix}/table/<name>', methods=['GET', 'POST', 'DELETE'])
        def table(name):
            set_db_context(self.db_context)
            return v.table(name)

        @app.teardown_appcontext
        def close_connection(exception):
            db = getattr(g, '_database', None)
            if db is not None:
                db.close()

        @app.errorhandler(Exception)
        def handle_error(e):
            print(e)
            return jsonify(error=str(e))
