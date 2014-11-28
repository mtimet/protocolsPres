# python 3 only script
# needs openpyxl, pandas and their dependencies
# run it at the root level of the repository that contains the results

import os 
import os.path

import openpyxl
import pandas as pd

ROOT_OUT_PATH = './csvout'
HEADERS = ['circonscription',
 'delegation',
 '#',
 'مكتب',
 'العربي  نصرة',
 'عبد الرحيم  الزواري',
 'كلثوم  كنو',
 'كمال\xa0  مرجان',
 'سالم\xa0  الشايبي',
 'عبد الرزاق  الكيلاني',
 'محمد الباجي القايد السبسي',
 'سليم\xa0 الرياحي',
 'عبد القادر اللباوي',
 'مصطفى كامل  النابلي',
 'أحمد الصافي السعيد',
 'ياسين\xa0 \xa0الشنوفي',
 'أحمد نجيب \xa0 الشابي',
 'حمودة\xa0 بن سلامة',
 'علي المولدي الشورابي',
 'محمد\xa0 فريخة',
 'محمد الحامدي',
 'المختار  الماجري',
 'عبد الرؤوف العيادي',
 'محرز بوصيان',
 'مصطفى\xa0 بن جعفر',
 'نور الدين حشاد',
 'محمد المنذر الزنايدي',
 'محمد المنصف المرزوقي',
 'سمير العبدلي',
 'محمد الهاشمي الحامدي',
 'حمة\xa0 الهمامي',
 'مجموع الأصوات حسب المكتب']

def process(directory, filename, force=False, noheader=False):
    delegation = filename[:-5]
    
    fin = os.path.join(directory, filename)
    
    circonscription = fin.split(os.sep)[-2]
    
    folderout = os.path.join(ROOT_OUT_PATH, directory[2:])
    
    if not os.path.exists(folderout) : 
        os.makedirs(folderout)
    fout = os.path.join(folderout, delegation + '.csv')
    if os.path.exists(fout) and not force:
        print ('not processing (%s,%s), because output file is already there %s'%(directory, filename, fout))
        return
    print('processing: ', directory, filename)
    
    wb=openpyxl.load_workbook(fin)
    ws=wb.get_active_sheet()
    nums = [str(e) for e in range(10)]
    firstcolumns = [circonscription, delegation]
    data = []
    headers = []
    FIRST_ROW = 6 if noheader else 7  
    for row in ws.rows[:-1]: # it brings a new method: iter_rows()

        if row[0].row < FIRST_ROW or (row[0].row > FIRST_ROW and (row[1].value is None or (len(str(row[1].value)) == 0))) or (row[1].value=='مجموع أصوات القائمة'): 
            continue

        line = [cell.value for cell in row if cell.value is not None and cell.value != '']
        if  row[0].row != FIRST_ROW:
            data.append(firstcolumns + line)
    df =  pd.DataFrame(data=data,columns=HEADERS)
    df.to_csv(fout, index=False)
    return df

def run():
    print('START')
    WITH_NOHEADER = ['ElMourouj.xlsx']
    agg = None
    for dirpath , dirnames, files in os.walk('.'):
        fs = [f for f in files if f[-5:] == '.xlsx']
        if len(fs) == 0 : continue

        for f in fs:
            noheader = f in WITH_NOHEADER
            df = process(dirpath,f, noheader=noheader)
            if agg is None:
                agg = df
            else:
                agg = pd.concat([agg, df])

    BUREAUX = ['مكتب' + ' ' + str(i) for i in range(1,10)]
    agg['center_name'] = agg['مكتب'].map(lambda s : s[:-6].strip() if s[-6:] in BUREAUX else s)
    filename = os.path.join(ROOT_OUT_PATH, 'aggregate.csv')
    agg.to_csv(filename, index=False)
    print('END')

if __name__ == "__main__":
    run()