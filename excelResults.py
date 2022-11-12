import pandas as pd
import time
timestr = time.strftime("%Y%m%d-%H%M%S")
df_windows = pd.read_csv('testswindows.csv')
df_linux = pd.read_csv('testslinux.csv')
df_mac = pd.read_csv('testsmac.csv')
with pd.ExcelWriter("Test_Results_"+timestr+".xlsx") as writer:
    df_windows.to_excel(writer, sheet_name="Windows")
    df_linux.to_excel(writer, sheet_name="Linux")
    df_mac.to_excel(writer, sheet_name="Mac")

