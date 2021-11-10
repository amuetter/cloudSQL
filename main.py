from flask import Flask
from cloudsql.core import CloudSQL

app = Flask(__name__)

cs = CloudSQL(dbpath='data/data.db', url_prefix='/database')
cs.serve(app)


