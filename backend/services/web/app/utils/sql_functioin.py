from app.base import sql_queries, base_sql
from app.utils.parsers import parse_egrul_egrip as pee


def add_user(params):
    answer = base_sql.Sql.exec(sql_queries.INSERT_CLIENT.format(**params))
    return answer[0]["client_id"]


def add_organization(params):
    answer = base_sql.Sql.exec(sql_queries.SELECT_ORGANIZATION_BY_INN.format(**params))
    if answer is None or answer == []:
        params["organization_date_reg"] = "NULL"
        answer = base_sql.Sql.exec(sql_queries.INSERT_ORGANIZATION.format(**params))
    if answer is not None and answer != []:
        params.update({'organization_id': answer[0]['organization_id']})
        answer = base_sql.Sql.exec(sql_queries.INSERT_LINK_CLIENT_ORGANIZATION.format(**params))
    return answer


def add_organiztion_by_inn_fl(inn):
    answer = pee.parse_egrul_egrip(inn)
    if "list_ip" in answer.keys():
        for i in answer["list_ip"]:
            i["status_client"] = "list_ip"
            i["client_id"] = 1
            add_organization(i)
    if "list_leader" in answer.keys():
        for i in answer["list_leader"]:
            i["client_id"] = 1
            i["status_client"] = "list_leader"
            add_organization(i)
    if "list_founder" in answer.keys():
        for i in answer["list_founder"]:
            i["client_id"] = 1
            i["status_client"] = "list_founder"
            add_organization(i)
    return True