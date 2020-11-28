import os
import secrets

DATABASE = {
    "dbname": os.environ.get('POSTGRES_DB'),
    "user": os.environ.get('POSTGRES_USER'),
    "host": 'postgres',
    "password": os.environ.get('POSTGRES_PASSWORD')
}


REPO_NAME = 'backend_server_init'
HOST = '46.148.224.125'

class Config:
    JSON_AS_ASCII = False