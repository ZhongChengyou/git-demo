import numpy as np
import pymysql
import pandas as pd
from pandas.core.frame import DataFrame
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
# 查看获取到的数据信息:
# print(df_result.info())
# print(df_result.shape)
# Display the data
# print(df_result.head(10))
#显示数值型数据的描述统计
# print(df_result.describe())
# 查看列标题
# print(df_result.columns)
# 查看前4行数据
# print(df_result.head(4))

# 检查重复值duplicated()
# print(df_result.duplicated())
df_result['latitude'] = df_result['latitude'].astype('float64')
df_result['longitude'] = df_result['longitude'].astype('float64')




print(df_result.head(10))
print('*'*100)
# 1.Delete the units without “time” data:
df_time = df_result.dropna(subset=['time'])

# 2.Sort GPS data units according to “time”(根据时间排序):
df_sorted = df_time.sort_values(by="time", axis = 0, ascending=True, inplace=False, na_position="last")

# 3.Linear interpolation of missing numerical data(缺失位置插值):
df_sorted["latitude"].interpolate(method='linear', axis=0, limit=None, inplace=True)
df_sorted["longitude"].interpolate(method='linear', axis=0, limit=None, inplace=True)
# check whether there is "null" value data:
# print(df_sorted[df_result.isnull().T.any()])
print(df_sorted.head(50))
print('*'*100)

# print(df_result.sort_values(by="time", axis = 0, ascending=True, inplace=False, na_position="last"))
# find the rows having "null" values:
# print(df_result[df_result.isnull().T.any()])
# Delete data units with duplicate “longitude”/”latitude”/”time”:


# print(df_sorted)
print('*'*100)
# Check the duplicate values(检查是否存在重复值):
print(df_sorted[df_sorted.duplicated(subset=['time'])])
print(df_sorted[df_sorted.duplicated(subset=['latitude', 'longitude'])])

# Delete data units with duplicate ”time”:
df_duplicated = df_sorted[df_sorted.duplicated(subset=['time']) == False]
# Delete data units with duplicate “longitude”/”latitude”:
df_duplicated = df_duplicated[df_duplicated.duplicated(subset=['longitude','latitude']) == False]
# print(df_duplicated)
print('*'*100)

# Check whether there is duplicate values:
# print(df_duplicated['latitude'].value_counts())
# print(df_duplicated['longitude'].value_counts())
# print(df_duplicated['time'].value_counts())

# Review whether duplicate data is deleted cleanly:
# print(df_duplicated[df_duplicated.duplicated(subset=['time'])])
# print('*'*100)
# print(df_duplicated[df_duplicated.duplicated(subset=['latitude', 'longitude'])])


# 绘制latitude/longitude的数据图像
# plt.plot(df_duplicated["latitude"])
# plt.show()
# plt.plot(df_duplicated["longitude"])
# plt.show()

# 把DataFrame中的longitude/latitude数据转换成list数据
df_lon = df_duplicated["longitude"].tolist()
df_lat = df_duplicated["latitude"].tolist()
df_time = df_duplicated["time"].tolist()

# 把timedelta数据转换为seconds来计数:
df_time_second = []
for i in df_time:
    df_time_second.append(i.total_seconds())




# # 处理longitude数据:
# i = 0
# while i < (len(df_lon)-1):
#     # 计算i+1与i之间的速度:
#     distance = df_lon[i + 1] - df_lon[i]
#     time = (df_time[i+1]-df_time[i]).total_seconds()
#     speed = (distance/time)
#     # find the exception value:
#     if(speed > 0.00005705 or speed < -0.00005705):
#         # implement linear interpolation of this missing data
#         time_2 = (df_time[i + 2] - df_time[i+1]).total_seconds()
#         df_lon[i+1] = df_lon[i] + ((time)/(time+time_2)) * (df_lon[i+2]-df_lon[i])
#     i += 1
# # 绘制longitude的数据图像
# plt.plot_date(df_time_second, df_lon)
# plt.tight_layout
# plt.show()
#
#
#
# # 处理latitude数据:
# i = 0
# while i < (len(df_lat)-1):
#     # 计算i+1与i之间的速度:
#     distance = df_lat[i + 1] - df_lat[i]
#     time = (df_time[i+1]-df_time[i]).total_seconds()
#     speed = (distance/time)
#     # find the exception value:
#     if(speed > 0.00004495 or speed < -0.00004495):
#         # implement linear interpolation of this missing data
#         time_2 = (df_time[i + 2] - df_time[i+1]).total_seconds()
#         df_lat[i+1] = df_lat[i] + ((time)/(time+time_2)) * (df_lat[i+2]-df_lat[i])
#     i += 1
# # 绘制latitude的数据图像
# plt.plot_date(df_time_second, df_lat)
# plt.tight_layout
# plt.show()

# 处理latitude数据:

# # 处理latitude数据:
# i = 0
# j = 0
# while i < (len(df_lat)-1):
#     # calculate the speed between i+1 and i:
#     distance = df_lat[i + 1] - df_lat[i]
#     time = (df_time[i+1]-df_time[i]).total_seconds()
#     speed = (distance/time)
#     # find the exception value:
#     if(speed > 0.00004495 or speed < -0.00004495):
#         df_lat[i + 1] = 0
#         flag = True
#         j = i
#         while (flag):
#             distance = df_lat[j + 2] - df_lat[i]
#             time = (df_time[j + 2] - df_time[i]).total_seconds()
#             speed = (distance / time)
#             if(speed <= 0.00004495 and speed >= -0.00004495):
#                 i = j + 1
#                 flag = False
#                 continue
#             df_lat[j + 2] = 0
#             j += 1
#     i += 1

# 将list df_lat转换成dataframe格式:
# data_lat = DataFrame(df_lat)
# data_lat = data_lat.replace(0, np.NaN)
#
# df_duplicated["latitude"] = data_lat
# df_duplicated["latitude"].interpolate(method='linear', axis=0, limit=None, inplace=True)
# df_lat_new = df_duplicated["latitude"].tolist()
# # 绘制latitude的数据图像
# plt.plot_date(df_time_second, df_lat_new)
# plt.tight_layout
# plt.show()



# # process longitude data:
# i = 0
# j = 0
# while i < (len(df_lon)-1):
#     # calculate the speed between i+1 and i:
#     distance = df_lon[i + 1] - df_lon[i]
#     time = (df_time[i+1]-df_time[i]).total_seconds()
#     speed = (distance/time)
#     # find the exception value:
#     if(speed > 0.00005705 or speed < -0.00005705):
#         df_lon[i + 1] = 0
#         flag = True
#         j = i
#         while (flag):
#             distance = df_lon[j + 2] - df_lon[i]
#             time = (df_time[j + 2] - df_time[i]).total_seconds()
#             speed = (distance / time)
#             if(speed <= 0.00005705 and speed >= -0.00005705):
#                 i = j + 1
#                 flag = False
#                 continue
#             df_lon[j + 2] = 0
#             j += 1
#     i += 1

# # 将list df_lon转换成dataframe格式:
# data_lon = DataFrame(df_lon)
# data_lon = data_lon.replace(0, np.NaN)
#
# df_duplicated["longitude"] = data_lon
# df_duplicated["longitude"].interpolate(method='linear', axis=0, limit=None, inplace=True)
# df_lon_new = df_duplicated["longitude"].tolist()
# # # 绘制longitude的数据图像
# plt.plot_date(df_time_second, df_lon_new)
# plt.tight_layout
# plt.show()

# 绘制longitude的数据图像
plt.plot_date(df_time_second, df_lon)
plt.tight_layout
plt.show()



# Process longitude data:
i0 = 0
t = 1
while i0 <= (len(df_lon)-1):
    # calculate the speed between i+1 and i:
    distance = df_lon[i0 + 1] - df_lon[i0]
    time = (df_time[i0+1]-df_time[i0]).total_seconds()
    speed = (distance/time)
    print(speed)
    # identify the normal/exception value:
    if(speed <= 0.00005705 and speed >= -0.00005705):
        t += 1
        i0 += 1
        # Starting from [i0-t+1], there are 4 consecutive normal values,
        # jump out of the loop
        if(t >= 4):
            break
    else:
        t = 1
        i0 += 1

# Delete data before index [i0-t+1]([0]~[i0-t]):
i = 0
while i <= (i0 - t):
    del df_lon[0]
    del df_time[0]
    i += 1

# Convert timedelta data into seconds to count:
df_time_second = []
for i in df_time:
    df_time_second.append(i.total_seconds())

# Draw data image of longitude
plt.plot_date(df_time_second, df_lon)
plt.tight_layout
plt.show()