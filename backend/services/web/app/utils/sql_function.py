from app.base import sql_queries, base_sql
from app.utils.parsers import parse_egrul_egrip as pee
import datetime
from app.utils.clients.egrul_nalog import EgrulNalogClient
from app.utils.parsers.parser_terrorist import check_on_terror


def add_user(params):
    answer = base_sql.Sql.exec(sql_queries.INSERT_CLIENT.format(**params))
    return answer[0]["client_id"]


def add_user_for_parse(json):
    params = {}
    params["name"] = json["USER"]["first_name"]
    params["surname"] = json["USER"]["last_name"]
    params["patronymic"] = ""
    params["nationality"] = ""
    params["country"] = ""
    params["inn"] = "NULL"
    params["sex"] = ""
    params["site"] = ""
    if "sex" in json["USER"].keys():
        params["sex"] = json["USER"]["sex"]
    if "site" in json["USER"].keys():
        params["site"] = json["USER"]["site"]
    try:
        years = json["USER"]["bdate"].split(".")
        params["bdate"] = datetime.date(int(years[2]), int(years[1]), int(years[0]))
    except:
        params["bdate"] = "NULL"
    try:
        phone = json["USER"]["phone"].replace("-", "").replace(" ", "").replace("+", "")
        params["phone"] = phone
    except:
        params["phone"] = "NULL"
    client_id = add_user(params)
    if params["bdate"] == "NULL":
        params["bdate"] = None
    if params["phone"] == "NULL":
        params["phone"] = None
    name = "{0} {1}".format(params["surname"], params["name"])
    client = EgrulNalogClient()
    inn = client.get_inn(name, "on")
    if inn is not None:
        add_organiztion_by_inn_fl(inn, client_id)
    return True


def add_organization(params):
    answer = base_sql.Sql.exec(sql_queries.SELECT_ORGANIZATION_BY_INN.format(**params))
    if answer is None or answer == []:
        years = params["organization_date_reg"].split(".")
        params["organization_date_reg"] = datetime.date(int(years[2]), int(years[1]), int(years[0]))
        answer = base_sql.Sql.exec(sql_queries.INSERT_ORGANIZATION.format(**params))
    if answer is not None and answer != []:
        params.update({'organization_id': answer[0]['organization_id']})
        answer = base_sql.Sql.exec(sql_queries.INSERT_LINK_CLIENT_ORGANIZATION.format(**params))
    return answer


def get_all_client_info(client_id):
    client_info = base_sql.Sql.exec(sql_queries.SELECT_CLIENT.format(client_id=client_id))
    if client_info == [] or client_info is None:
        return None
    organizations = base_sql.Sql.exec(sql_queries.SELECT_ORGANIZATIONS_BY_CLIENT.format(client_id=client_id))
    if organizations != [] and organizations is not None:
        client_info[0]["organizations"] = organizations
    interests = base_sql.Sql.exec(sql_queries.SELECT_INTERESTS_BY_CLIENT.format(client_id=client_id))
    if interests != [] and interests is not None:
        client_info[0]["interests"] = interests
    try:
        if check_on_terror(client_info[0]["surname"], client_info[0]["name"], client_info[0]["patronymic"], client_info[0]["bdate"]) != []:
            client_info[0]["status_terrorist"] = True
        else:
            client_info[0]["status_terrorist"] = False
    except:
        client_info[0]["status_terrorist"] = False
    return client_info[0]


def add_organiztion_by_inn_fl(inn, client_id):
    answer = pee.parse_egrul_egrip(inn)
    if "list_ip" in answer.keys():
        for i in answer["list_ip"]:
            i["status_client"] = "list_ip"
            i["client_id"] = client_id
            add_organization(i)
    if "list_leader" in answer.keys():
        for i in answer["list_leader"]:
            i["client_id"] = client_id
            i["status_client"] = "list_leader"
            add_organization(i)
    if "list_founder" in answer.keys():
        for i in answer["list_founder"]:
            i["client_id"] = client_id
            i["status_client"] = "list_founder"
            add_organization(i)
    return True

#print(get_all_client_info(1))