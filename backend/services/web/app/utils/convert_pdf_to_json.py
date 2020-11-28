from pdf2docx import extract_tables


def parse_ogrn(pdf_file):
    inn = None
    for i in range(4):
        try:
            for table in extract_tables(pdf_file, start=i, end=i+1):
                for tabl in table:
                    if tabl[1] is None:
                        continue
                    f = tabl[1].lower()
                    if "идентификационный номер\nналогоплательщика (инн)" == f:
                        inn = tabl[2]
                    elif "инн" == f:
                        inn = tabl[2]
                    elif "идентификационный номер\nналогоплательщика (инн)" in f and "дата постановки на учет" in f:
                        inn = tabl[2].split("\n")[0]
                    if inn is not None:
                        return inn
                i += 1
        except:
            break
    return inn
