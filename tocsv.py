# python 3 only script
# needs openpyxl, pandas and their dependencies
# run it at the root level of the repository that contains the results

import os 
import os.path

import openpyxl
import pandas as pd

def process(directory, filename, force=False, noheader=False):
    fin = os.path.join(directory, filename)
    folderout = os.path.join('./csvout',directory[2:])
    if not os.path.exists(folderout) : 
        os.makedirs(folderout)
    fout = os.path.join(folderout, filename[:-5]+ '.csv')
    if os.path.exists(fout) and not force:
        print ('not processing (%s,%s), because output file is already there %s'%(directory, filename, fout))
        return
    print('processing: ', directory, filename)
    wb=openpyxl.load_workbook(fin)
    ws=wb.get_active_sheet()
    nums = [str(e) for e in range(10)]
    data = []
    headers = []
    FIRST_ROW = 6 if noheader else 7  
    for row in ws.rows[:-1]: # it brings a new method: iter_rows()

        if row[0].row < FIRST_ROW or (row[0].row > FIRST_ROW and (row[1].value is None or (len(str(row[1].value)) == 0))) or (row[1].value=='مجموع أصوات القائمة'): 
            continue

        line = [cell.value for cell in row if cell.value is not None and cell.value != '']
        if not noheader and row[0].row == FIRST_ROW:
            headers = ['#', 'مكتب' ] + line
            headers = headers + ['مجموع الأصوات حسب المكتب']
        else:
            data.append(line)
    df = pd.DataFrame(data=data) if noheader else pd.DataFrame(data=data,columns=headers)
    df.to_csv(fout, index=False)
def run():
    print('START')
    WITH_NOHEADER = ['ElMourouj.xlsx']#, 'Amdoun.xlsx']
    for dirpath , dirnames, files in os.walk('.'):
        fs = [f for f in files if f[-5:] == '.xlsx']
        if len(fs) == 0 : continue

        for f in fs:
            noheader = f in WITH_NOHEADER
            process(dirpath,f, noheader=noheader)
    print('END')

if __name__ == "__main__":
    run()