# with open("weather_data.csv", mode="r") as formated_data:
#     read_line_data = formated_data.readlines()
#
# weather_data_cleaned = []
#
# for data in read_line_data:
#     weather_data_cleaned.append(data.strip())
#
# print(weather_data_cleaned)

# with open("weather_data.csv", mode="r") as data_file:
#     data = csv.reader(data_file)
#     temperatures = []
#     for temp in list(data)[1:]:
#         temperatures.append(int(temp[1]))
#     print(temperatures)

# data = pandas.read_csv("weather_data.csv")
# all_temps = data["temp"].to_list()
# avg_temp = sum(all_temps) / len(all_temps)
#
# print(data[data.temp == data["temp"].max()])
# data["temp_f"] = data["temp"] * 9/5 + 32
#
# print(data[data.day == "Monday"].temp_f)

import csv
import pandas
data = pandas.read_csv("2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20241110.csv")

all_colors = data["Primary Fur Color"].value_counts()
all_colors.to_csv("Color_Count_And_Sorted")


