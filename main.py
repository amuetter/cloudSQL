from flask import Flask
from cloudsql.core import CloudSQL

app = Flask(__name__)

cs = CloudSQL(db_type='sqlite', db_conn_string='data/data.db', url_prefix='/database', api_key='adminadmin')
cs.serve(app)


