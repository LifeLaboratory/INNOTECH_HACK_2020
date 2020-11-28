SQL_SELECT_INFO_CLIENT = """
SELECT *
FROM raifhack.clients
WHERE id={id}
"""

SQL_SELECT_INFO_CLIENTS = """
SELECT *
FROM raifhack.clients
"""

SQL_SELECT_INFO_COURIER = """
SELECT *
FROM raifhack.couriers
WHERE id={id}
"""

SQL_SELECT_INFO_COURIERS = """
SELECT *
FROM raifhack.couriers
ORDER BY id
"""

SQL_SELECT_ORDERS_COURIER = """
SELECT *
FROM raifhack.orders
WHERE number_courier={id}
ORDER BY id DESC
"""

SQL_SELECT_COMPANY_INFO = """
SELECT *
FROM raifhack.companies
"""

SQL_SELECT_INFO_COURIER_IN_COMPANY = """
SELECT *
FROM raifhack.couriers
WHERE num_company={id}
ORDER BY id
"""

SQL_SELECT_ALL_COURIERS = """
SELECT *
FROM raifhack.couriers
"""

SQL_SELECT_ACTIVE_ORDERS = """
SELECT *
FROM raifhack.orders AS ord
LEFT JOIN raifhack.couriers AS co ON (co.id = ord.number_courier)
LEFT JOIN raifhack.clients AS cl ON (cl.id = ord.number_client)
WHERE ord.status_order is NULL
"""

SQL_UPDATE_COURIER_GPS = """
UPDATE raifhack.couriers
SET lat={lat}, lon={lon}
WHERE id={id}
RETURNING TRUE 
"""

SQL_INSERT_ORDER_CREATE = """
INSERT INTO raifhack.orders (cost, number_client, address, qr_code, url_payload, qr_id, number_courier)
VALUES ({cost}, {number_client}, '{address}', '{qr_code}', '{url_payload}', '{qr_id}', {number_courier})
RETURNING id
"""

SQL_SELECT_ORDER_STATUS = """
SELECT *
FROM raifhack.orders
WHERE paymentstatus != 'ACWP' or paymentstatus is NULL
"""

SQL_UPDATE_OREDER_STATUS = """
UPDATE raifhack.orders
SET paymentstatus = '{pays}', status_order = TRUE 
WHERE id = {id}
RETURNING number_courier
"""

SQL_UPDATE_STATUS_COURIER = """
UPDATE raifhack.couriers
SET status = {status}
WHERE id = {id}
RETURNING id
"""