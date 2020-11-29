import requests as req
from bs4 import BeautifulSoup
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from app.base import sql_queries, base_sql


def sql_execute(sql_give):
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='PINLOX!@#', host='46.148.224.125')
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    answer = None

    print(sql_give)
    cursor.execute(sql_give)
    conn.commit()
    try:
        answer = cursor.fetchall()
    except:
        pass
    finally:
        conn.close()
        cursor.close()
        return answer


URL = 'http://www.fedsfm.ru/documents/terrorists-catalog-portal-act'


def func_filt(elem):
    elems = elem.text.split(',')
    l = len(elems)
    elems[0] = elems[0][3:-1].split()
    birthday = ''
    city = ''
    if l > 1:
        if elems[1].split():
            birthday = elems[1].split()[0]
            print(birthday)
            try:
                birthday = datetime.strptime(birthday, '%d.%m.%Y').strftime('%m-%d-%Y')
            except:
                try:
                    birthday = elems[2].split()[0]
                    birthday = datetime.strptime(birthday, '%d.%m.%Y').strftime('%m-%d-%Y')
                except:
                    pass
                print('ERROR')
                birthday = ''

    if l > 2:
        city = elems[-1][:-1]
    if elems[0][0] == '.':
        elems[0] = elems[0][1:]
    if len(elems[0]) > 3:
        elems[0] = elems[0][:3]
    elif len(elems[0]) == 2:
        elems[0] += ['']
    res = elems[0] + [birthday, city]
    return res


def get_terrorist():
    resp = req.get(URL)
    soup = BeautifulSoup(resp.text)
    terrs = soup.find(id='russianFL').find_all('li')
    terrs = list(map(func_filt, terrs))
    return terrs


def insert_into_db():
    terrs = get_terrorist()
    for terr in terrs:
        print(terr)

        if not terr[3]:
            terr[3] = '1-1-1910'

        sql_query = """
        INSERT INTO terrorists(surname, name, patronymic, date_birth, place_birth)
        VALUES('{}','{}', '{}','{}', '{}')
        returning id
        """.format(*terr)
        try:
            _id = sql_execute(sql_query)[0]['id']
        except:
            from time import sleep
            sleep(10)
            _id = sql_execute(sql_query)[0]['id']

        sql_query = """
                update terrorists set date_birth = NULL where id = {}
                """.format(_id)
        try:
            sql_execute(sql_query)
        except:
            from time import sleep
            sleep(10)
            sql_execute(sql_query)


def check_on_terror(surname: str, name: str, patr: str, date: str) -> dict:
    """
    Возвращает None в случае, если не нашел террориста и dict с его данными, если нашел
    date в формате строки понятной sql (12-31-2020)
    """

    sql_query = """
    select *
    from terrorists
    where 
    date_birth = '{}'
    and name = '{}'
    and surname = '{}'
    and patronymic = '{}'
    """.format(date, name, surname, patr)

    data = base_sql.Sql.exec(sql_query)
    #data = sql_execute(sql_query)
    print(data)
    if data:
        res = dict(data[0])
    else:
        res = None

    return res


def update_db():
    sql_query = """
               delete from terrorists
               """
    sql_execute(sql_query)
    insert_into_db()


if __name__ == '__main__':
    #update_db()
    res = check_on_terror('АБАЕВ', 'ИДРИС', 'МОВСАРОВИЧ', '01-02-1986')
    print(res)
