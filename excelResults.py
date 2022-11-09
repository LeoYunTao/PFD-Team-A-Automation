import pandas as pd
df_new = pd.read_csv('tests.csv')
df_new.to_excel("Test Results.xlsx")
# # saving xlsx file
# GFG = pd.ExcelWriter('Test Results.xlsx', engine="openpyxl",mode='a')
# df_new.to_excel(GFG, index=False)
