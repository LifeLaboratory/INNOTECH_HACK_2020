import requests as r
import json
from bs4 import BeautifulSoup


def parse_table_org(answer_table):
    list = []
    for company in answer_table:
        json_answer = {}
        user_info = company.find_all('td')
        json_answer["url"] = 'https://zachestnyibiznes.ru' + str(user_info[0]).split('href="')[1].split('"')[
            0].replace('\n', '').replace('\t', '')
        json_answer["name"] = user_info[0].span.string.replace('\n', '').replace('\t', '')
        json_answer["status"] = user_info[1].span.string.replace('\n', '').replace('\t', '')
        json_answer["inn_org"] = str(user_info[2]).split('>')[1].split('</')[0].replace('\n', '').replace('\t', '')
        json_answer["leader"] = str(user_info[3]).split('>')[1].split('</')[0].replace('\n', '').replace('\t', '')
        json_answer["date_reg"] = str(user_info[4]).split('>')[1].split('</')[0].replace('\n', '').replace('\t', '')
        list.append(json_answer)
    return list


def parse_egrul_egrip(inn):
    url = "https://zachestnyibiznes.ru/fl/{}".format(inn)
    answer = r.get(url).content
    answer_soup = BeautifulSoup(answer, 'html.parser')
    answer_soup = answer_soup.find('div', {'class': 'col-md-12 m-b-10 m-t-10'})
    answer_table = answer_soup.find_all('table', {'class': 'table table-bordered table-striped rwd-table'})
    lists = {}
    if len(answer_table) == 3:
        lists["list_ip"] = parse_table_org(answer_table[0].find('tbody').find_all('tr'))
        lists["list_leader"] = parse_table_org(answer_table[1].find('tbody').find_all('tr'))
        lists["list_founder"] = parse_table_org(answer_table[2].find('tbody').find_all('tr'))
    elif len(answer_table) == 2:
        if "Числится в Едином государственном реестре индивидуальных предпринимателей:" in str(answer_soup):
            lists["list_ip"] = parse_table_org(answer_table[0].find('tbody').find_all('tr'))
            if "Числится в Едином государственном реестре юридических лиц:" in str(answer_soup):
                lists["list_leader"] = parse_table_org(answer_table[1].find('tbody').find_all('tr'))
            else:
                lists["list_founder"] = parse_table_org(answer_table[1].find('tbody').find_all('tr'))
        else:
            lists["list_leader"] = parse_table_org(answer_table[0].find('tbody').find_all('tr'))
            lists["list_founder"] = parse_table_org(answer_table[1].find('tbody').find_all('tr'))
    elif len(answer_table) == 1:
        if "Числится в Едином государственном реестре индивидуальных предпринимателей:" in str(answer_soup):
            lists["list_ip"] = parse_table_org(answer_table[0].find('tbody').find_all('tr'))
        elif "Числится в Едином государственном реестре юридических лиц:" in str(answer_soup):
            lists["list_leader"] = parse_table_org(answer_table[0].find('tbody').find_all('tr'))
        else:
            lists["list_founder"] = parse_table_org(answer_table[0].find('tbody').find_all('tr'))
    return lists


#print(parse_egrul_egrip(773370633582))