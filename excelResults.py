import pandas as pd
import time
import glob
import os

timestr = time.strftime("%Y%m%d-%H%M%S")

df_test_results = []

# find all the csv files in the directory
for file in glob.glob('csv-reports/*.csv'):
    df_test_results.append(pd.read_csv(file))

if not os.path.exists('excel-report'):
   os.makedirs('excel-report')

# convert it into excel file
with pd.ExcelWriter("excel-report/Test_Results_" + timestr + ".xlsx") as writer:
    for df_test_result in df_test_results:
        df_test_result.to_excel(writer, sheet_name=df_test_result['os_system'])
