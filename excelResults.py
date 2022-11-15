import pandas as pd
import time
import glob
import os

from config import csv_reports_path, excel_report_path

timestr = time.strftime("%Y%m%d-%H%M%S")

df_test_results = []

# find all the csv files in the directory
for file in glob.glob(f'{csv_reports_path}/*.csv'):
    df_test_results.append(pd.read_csv(file))

if not os.path.exists(f'{excel_report_path}'):
   os.makedirs(f'{excel_report_path}')

# dfs=[df_windows,df_mac,df_linux]
# with pd.ExcelWriter("Test_Results_"+timestr+".xlsx") as writer:
#     pd.concat(dfs).to_excel(writer,sheet_name="Test Results",index=False)

# convert it into excel file
with pd.ExcelWriter(f"{excel_report_path}/Test_Results_" + timestr + ".xlsx") as writer:
    for df_test_result in df_test_results:
        df_test_result.to_excel(writer, sheet_name=df_test_result['os_system'].iloc[0],index=False)
