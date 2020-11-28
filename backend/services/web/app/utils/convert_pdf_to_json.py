from pdf2docx import extract_tables


def parse_ogrn(pdf_file):
    tables = []
    i = 0
    while True:
        try:
            tables.append(extract_tables(pdf_file, start=i, end=i+1))
            i += 1
        except:
            break
    json_ogrn = {}
    json_ogrn["activities"] = []
    for tableses in tables:
        for table in tableses:
            for tabl in table:
                if tabl[1] is None:
                    continue
                f = tabl[1].lower()
                if "полное наименование" == f:
                    json_ogrn["company_name"] = tabl[2]
                elif "сокращенное наименование" == f:
                    json_ogrn["surname"] = tabl[2]
                elif "фамилия" == f:
                    json_ogrn["surname"] = tabl[2]
                elif "имя" == f:
                    json_ogrn["name"] = tabl[2]
                elif "отчество" == f:
                    json_ogrn["patronymic"] = tabl[2]
                elif "пол" == f:
                    json_ogrn["gender"] = tabl[2]
                elif "огрнип" == f:
                    json_ogrn["ogrn"] = tabl[2]
                elif "дата регистрации" == f:
                    json_ogrn["ogrn_reg"] = tabl[2]
                elif "огрн" == f:
                    json_ogrn["ogrn"] = tabl[2]
                elif "дата присвоения огрн" == f:
                    json_ogrn["ogrn_reg"] = tabl[2]
                elif "гражданство" == f:
                    json_ogrn["nationality"] = tabl[2]
                elif "гражданство" == f:
                    json_ogrn["nationality"] = tabl[2]
                elif "государство гражданства иностранного" in f:
                    json_ogrn["country"] = tabl[2]
                elif "идентификационный номер\nналогоплательщика (инн)" == f:
                    json_ogrn["inn"] = tabl[2]
                elif "инн" == f:
                    json_ogrn["inn"] = tabl[2]
                elif "кпп" == f:
                    json_ogrn["kpp"] = tabl[2]
                elif "дата постановки на учет" == f:
                    json_ogrn["inn_reg"] = tabl[2]
                elif "идентификационный номер\nналогоплательщика (инн)" in f and "дата постановки на учет" in f:
                    json_ogrn["inn"] = tabl[2].split("\n")[0]
                    json_ogrn["inn_reg"] = tabl[2].split("\n")[-1]
                elif "код и наименование вида деятельности" == f:
                    json_ogrn["activities"].append(tabl[2])
    if json_ogrn["activities"] == []:
        del json_ogrn['activities']
    return json_ogrn

#print(parse_ogrn("fl-317470400051557-20201128130033.pdf"))
#print(parse_ogrn("fl-317470400051557-20201128130052.pdf"))
#print(parse_ogrn("ul-1175000005003-20201128130115.pdf"))
#print(parse_ogrn("ul-5067746830432-20201128130122.pdf"))

