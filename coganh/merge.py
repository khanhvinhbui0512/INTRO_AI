import pandas as pd
import xlsxwriter
def merge():
    Data = {}
    df1 = pd.read_excel('temp1.xlsx', sheet_name='Bayes')
    df1 = pd.DataFrame(df1, columns=['A', 'B', 'C', 'D'])
    df1 = df1.reset_index()  # make sure indexes pair with number of rows
    for index, row in df1.iterrows():
        if(int(row['A']) not in Data):
            Data[int(row['A'])] = [int(row['B']), int(row['C']), int(row['D'])]
        else:
            Data[int(row['A'])][0] += int(row['B'])
            Data[int(row['A'])][1] += int(row['C'])
            Data[int(row['A'])][2] += int(row['D'])
    df2 = pd.read_excel('temp2.xlsx', sheet_name='Bayes')
    df2 = pd.DataFrame(df2, columns=['A', 'B', 'C', 'D'])
    df2 = df2.reset_index()  # make sure indexes pair with number of rows
    for index, row in df2.iterrows():
        if(int(row['A']) not in Data):
            Data[int(row['A'])] = [int(row['B']), int(row['C']), int(row['D'])]
        else:
            Data[int(row['A'])][0] += int(row['B'])
            Data[int(row['A'])][1] += int(row['C'])
            Data[int(row['A'])][2] += int(row['D'])
    workbook = xlsxwriter.Workbook('temp.xlsx')
    worksheet = workbook.add_worksheet('Bayes')
    worksheet.write(0,0,"A")
    worksheet.write(0,1,"B")
    worksheet.write(0,2,"C")
    worksheet.write(0,3,"D")
    row = 1
    for x in Data:
        worksheet.write(row,0,x)
        worksheet.write(row,1,Data[x][0])
        worksheet.write(row,2,Data[x][1])
        worksheet.write(row,3,Data[x][2])
        row += 1
    workbook.close()

merge()
# def test():
#     number_of_turn = 100000000000
#     for i in range(number_of_turn):
#         workbook = xlsxwriter.Workbook('temp.xlsx')
#         worksheet = workbook.add_worksheet('Bayes')
#         df = pd.read_excel('temp.xlsx', sheet_name='Bayes')
#         df = pd.DataFrame(df, columns=['A', 'B', 'C', 'D'])
#         Data = {}
#         df = df.reset_index()  # make sure indexes pair with number of rows
#         for index, row in df.iterrows():
#             if(int(row['A']) not in Data):
#               Data[int(row['A'])] = [int(row['B']), int(row['C']), int(row['D'])]
#             else:
#               Data[int(row['A'])][0] += int(row['B'])
#               Data[int(row['A'])][1] += int(row['C'])
#               Data[int(row['A'])][2] += int(row['D'])
        
#         worksheet.write(0, 0, "A")
#         worksheet.write(0, 1, "B")
#         worksheet.write(0, 2, "C")
#         worksheet.write(0, 3, "D")
#         row = 1
#         for x in Data:
#             worksheet.write(row, 0, x)
#             worksheet.write(row, 1, Data[x][0]+1)
#             worksheet.write(row, 2, Data[x][1]+1)
#             worksheet.write(row, 3, Data[x][2]+1)
#             row += 1
#         workbook.close()
# test()