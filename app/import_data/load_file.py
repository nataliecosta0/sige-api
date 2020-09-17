# import pandas as pd
from xlrd import open_workbook
from datetime import datetime, timedelta

def loadfile(path):
    book = open_workbook(path, on_demand=True)
    alunos = []
    for name in book.sheet_names():
        sheet = book.sheet_by_name(name)
        n_col = sheet.ncols
        n_lines = sheet.nrows
        columns_name = [each.value.strip() for each in sheet.row(0)]
        for current_line in range(1, n_lines):
            aluno = {}
            for current_column in range(n_col):
                col_name = columns_name[current_column]
                cell_info = sheet.cell(current_line, current_column).value
                if isinstance(cell_info, str):
                    cell_info = cell_info.strip()
                aluno.update({col_name: cell_info})
            alunos.append(aluno)

    print(alunos)
    # return alunos
