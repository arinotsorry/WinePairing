"""
Well, I already wrote the xlsx file writer, but to convert the tables to a database, I need to convert the xlsx files
to csv files. I still want to keep the xlsx counterparts for my own readability.
"""
import openpyxl
import csv

# open workbook
wb = openpyxl.load_workbook('./ExcelFiles/Flavors.xlsx')

# get worksheets
sheets = wb.sheetnames
length = len(sheets)

for sheet_name in sheets:
    sheet = wb[ sheet_name ]
    
    # create writer object
    col = csv.writer(open('./CsvFiles/' + sheet_name + '.csv', 'w', newline=""))
    
    # write data in csv file
    for row in sheet.rows:
        col.writerow([cell.value for cell in row])
    
    print( "{:.2f}".format( 100 * ( sheets.index(sheet_name) + 1 ) / length ) + ' %' )
