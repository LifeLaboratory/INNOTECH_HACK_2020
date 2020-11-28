SELECT_ORGANIZATIONS_BY_CLIENT = """
SELECT * FROM public.organization o
LEFT JOIN public.link_client_organization l ON (o.id = l.organization_id)
WHERE l.client_id = {client_id};
"""

SELECT_ORGANIZATION_BY_INN = """
SELECT id FROM public.organization
WHERE inn_org = {inn_org};
"""

SELECT_CLIENT = """
SELECT * FROM public.client
WHERE id={id};
"""

SELECT_TERRORIST = """
SELECT * FROM public.terrorists
WHERE surname='{surname}' AND name='{name}' AND patronymic='{patronymic}';
"""

SELECT_COUNT_USERS = """
SELECT count(*)
FROM public.client;
"""

INSERT_CLIENT = """
INSERT INTO public.client (surname, name, patronymic, nationality, country, inn, inn_reg)
VALUES ('{surname}', '{name}', '{patronymic}', '{nationality}', '{country}', {inn}, '{inn_reg}')
RETURNING id;
"""

INSERT_ORGANIZATION = """
INSERT INTO public.organization (name_org, url_org, status_org, leader_org, date_reg_org, inn_org)
VALUES ('{name_org}', '{url_org}', '{status_org}', '{leader_org}', '{date_reg_org}', {inn_org})
RETURNING id;
"""

INSERT_LINK_CLIENT_ORGANIZATION = """
INSERT INTO public.link_client_organization (client_id, orgabization_id, status_client)
VALUES ({client_id}, {organization_id}, '{status_client}')
RETURNING id;
"""
