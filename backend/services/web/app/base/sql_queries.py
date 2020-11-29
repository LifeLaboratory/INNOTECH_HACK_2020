SELECT_ORGANIZATIONS_BY_CLIENT = """
SELECT * FROM public.organization o
LEFT JOIN public.link_client_organization l ON (o.organization_id = l.organization_id)
WHERE l.client_id = {client_id};
"""

SELECT_INTERESTS_BY_CLIENT = """
SELECT interest_name FROM public.interests i
LEFT JOIN public.link_client_interest l ON (i.interest_id = l.interest_id)
WHERE l.client_id = {client_id};
"""

SELECT_ORGANIZATION_BY_INN = """
SELECT organization_id FROM public.organization
WHERE organization_inn = {organization_inn};
"""

SELECT_CLIENT = """
SELECT * FROM public.client
WHERE client_id={client_id};
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
INSERT INTO public.client (surname, name, patronymic, nationality, country, inn, inn_reg, sex, city, bdate, phone)
VALUES ('{surname}', '{name}', '{patronymic}', '{nationality}', '{country}', {inn}, '{inn_reg}', {sex}, '{city}', '{bdate}', {phone})
RETURNING client_id;
"""

INSERT_ORGANIZATION = """
INSERT INTO public.organization (organization_name, organization_url, organization_status, organization_leader, organization_date_reg, organization_inn)
VALUES ('{organization_name}', '{organization_url}', '{organization_status}', '{organization_leader}', {organization_date_reg}, {organization_inn})
RETURNING organization_id;
"""

INSERT_LINK_CLIENT_ORGANIZATION = """
INSERT INTO public.link_client_organization (client_id, organization_id, status_client)
VALUES ({client_id}, {organization_id}, '{status_client}')
RETURNING client_id;
"""
