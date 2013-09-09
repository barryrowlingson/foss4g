#utilities

# populate table from xls

from .models import Map

import xlrd

# 0 Timestamp
# 1	Full Name
# 2	Organisation
# 3	Associated authors
# 4	Tell us about the map
# 5	Competition category
# 6	Map Format
# 7	Full name
# 8	URL

def fillfrom(filepath):
    book = xlrd.open_workbook(filepath)
    sheet = book.sheets()[0]
    nrecs = sheet.nrows-1
    row = 1 # skip head

    while row <= nrecs:
        cellData=sheet.row(row)
        rowData=[c.value for c in cellData]
        m = Map(
            row = row+1,
            author = rowData[1],
            org = rowData[2],
            assoc = rowData[3],
            tellus=rowData[4],
            category = rowData[5],
            mapformat=rowData[6],
            fullname=rowData[7],
            URL=rowData[8],
            title = rowData[4][:30]+"...",
            vcount = 0,
            )
        m.save()
        

        row = row + 1
