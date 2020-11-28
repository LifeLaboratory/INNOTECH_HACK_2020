import os

DATABASE = {
    "dbname": os.environ.get('POSTGRES_DB'),
    "user": os.environ.get('POSTGRES_USER'),
    "host": 'postgres',
    "password": os.environ.get('POSTGRES_PASSWORD')
}


REPO_NAME = 'INNOTECH_HACK_2020'
HOST = '46.148.224.125'


class Config:
    JSON_AS_ASCII = False