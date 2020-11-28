from app.base import sql_queries, base_sql


def add_user(params):
    answer = base_sql.Sql.exec(sql_queries.INSERT_CLIENT.format(**params))
    return answer[0]["id"]


def add_organization(params):
    answer = base_sql.Sql.exec(sql_queries.INSERT_ORGANIZATION.format(**params))
    if answer is not None:
        params.update({'organization_id': answer[0]['id']})
        answer = base_sql.sql.exec(sql_queries.INSERT_LINK_CLIENT_ORGANIZATION.format(**params))
    return answer

