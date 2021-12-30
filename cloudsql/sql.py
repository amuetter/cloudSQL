import sqlite3
import psycopg
from flask import g

# sql interfaces
def get_db():
    
    db = getattr(g, '_database', None)
    
    if db is None:
        
        db_context = getattr(g, '_db_context', None)
        db_type = db_context['db_type']
        db_conn_string = db_context['db_conn_string']

        if db_type == 'sqlite':
            db = g._database = sqlite3.connect(db_conn_string)
            db.row_factory = sqlite3.Row
        
        elif db_type == 'postgresql':
            db = g._database = psycopg.connect(db_conn_string)

    return sql_connection(db_type, db)


def set_db_context(db_context):
    g._db_context = db_context


class sql_connection():

    def __init__(self, db_type, db):
        self.db_type = db_type
        self.conn = db

    def execute(self, query):
        c = self.conn.cursor()

    def get_tables(self):
        tables = []

        if self.db_type == 'sqlite':
            query = "SELECT name FROM sqlite_master WHERE type='table';"
        elif self.db_type == 'postgresql':
            query = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname NOT IN ('pg_catalog', 'information_schema');"

        for row in self.conn.execute(query).fetchall():
            tables.append(row[0])
        return tables

    def create(self, name, schema):
        string_schema = ', '.join(list(map( lambda x: f'{x[0]} {x[1]}', schema.items())))
        query = f'CREATE TABLE {name} ({string_schema});'
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()

    def select(self, name, columns, args):

        c = self.conn.cursor()
        if not columns:
            columns = '*'
            
        if args:
            conditions = ' AND '.join(map(lambda x: f'{x}=:{x}', args.keys()))
            query = f'SELECT {columns} FROM {name} WHERE {conditions};'
            c.execute(query, args)

        else:
            query = f'SELECT {columns} FROM {name};'
            c.execute(query)
            
        result = []
        for row in c.fetchall():
            result.append(dict(row))

        return result

    def insert(self, name, data):
        query = f'''INSERT INTO {name} ({", ".join([k for k in data.keys()])}) VALUES ({", ".join(["?" for _ in data])})'''
        c = self.conn.cursor()
        c.execute(query, list(data.values()))
        self.conn.commit()

    def drop(self, name):
        query = f'DROP TABLE {name};'
        c = self.conn.cursor()
        c.execute(query)
        self.conn.commit()
        

def get_tables(conn):
    tables = []
    for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall():
        tables.append(row[0])
    return tables