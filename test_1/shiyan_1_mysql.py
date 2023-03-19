import re

import pandas as pd
# import mysql.connector
import pymysql
import os

# 读取Excel文件
excel_file = "students_scores.xlsx"
df = pd.read_excel(excel_file, sheet_name='Sheet2')
# df_5cols = df.iloc[:, :5]
# print(df_5cols)
# 输出所有内容
print(df)


def table_exists(con, table_name):        # 这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        return 1        # 存在返回1
    else:
        return 0        # 不存在返回0


conn = pymysql.connect(
    host='localhost',  # MySQL服务器地址
    port=3306,  # MySQL服务器端口号
    user='root',  # 用户名
    password='111111',  # 密码
    database='pythonprogramming',  # 数据库名称
    charset='utf8mb4'  # 字符集
)
cursor = conn.cursor()

if table_exists(cursor, 'students') != 1:
    # 创建表
    create_table_query = """
    CREATE TABLE students(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        age INT,
        gender VARCHAR(10)
        # TODO: 添加更多字段
    )ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """
    cursor.execute(create_table_query)

# 将数据插入表中
for sheet_name in df.keys():
    sheet = df[sheet_name]
#   for row in sheet.iterrows():
    for row in df.iterrows():
        insert_query = """
        INSERT ignore INTO students(name, age, gender) VALUES (%s, %s, %s) 
        """

        values = tuple(row[1])  # 注意：这里需要转换为元组
        cursor.execute(insert_query, values)
    conn.commit()

# 保存为二进制格式文件
binary_file = "students_scores.pkl"
df.to_pickle(binary_file)

# 保存为JSON文本格式文件
json_file = "students_scores.json"
df.to_json(json_file)

# 比较文件大小
print("Excel文件大小：", os.path.getsize(excel_file))
print("二进制文件大小：", os.path.getsize(binary_file))
print("JSON文件大小：", os.path.getsize(json_file))

# 关闭连接
cursor.close()
conn.close()
