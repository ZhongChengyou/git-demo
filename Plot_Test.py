import pymysql
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from datetime import datetime, timedelta

# get data from MySQL:
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    db="gps_data_new")

# 把原始数据存放在df_result中:
cur = conn.cursor()
cur.execute("select * from gpgll_data")
result = cur.fetchall()
df_result = pd.DataFrame(list(result), columns = ["id", "header", "latitude","N_S",
                                                  "longitude","E_W", "time", "status",
                                                  "check_value"])


# 把dataframe中的数据转换成数列的形式:
df_lon = df_result["longitude"].tolist()
df_lat = df_result["latitude"].tolist()
df_time = df_result["time"].tolist()

# 把timedelta数据转换为seconds来计数:
df_time_second = []
for i in df_time:
    df_time_second.append(i.total_seconds())

# 绘制longitude的数据图像
plt.plot_date(df_time_second, df_lon)
plt.tight_layout
plt.show()

# 绘制latitude的数据图像
plt.plot_date(df_time_second, df_lat)
plt.tight_layout
plt.show()


