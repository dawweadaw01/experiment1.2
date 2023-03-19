import pandas as pd
import sqlite3

# 连接数据库
conn = sqlite3.connect('test.db')

# 创建表格
c = conn.cursor()
c.execute('''CREATE TABLE scores
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT,
             subject TEXT,
             score INTEGER);''')

# 读取Excel文件内容
df = pd.read_excel('scores.xlsx')

# 将数据写入数据库
df.to_sql('scores', conn, if_exists='append', index=False)

# 查询某个学生某门课成绩
query = "SELECT * FROM scores WHERE name='张三' AND subject='语文'"
result = pd.read_sql_query(query, conn)

# 解析结果集并比较
expected_result = pd.DataFrame({'name': ['张三'], 'subject': ['语文'], 'score': [90]})
assert result.equals(expected_result)

# 导出数据库中数据到Excel文件
result.to_excel('result.xlsx', index=False)

# 关闭连接
conn.close()
