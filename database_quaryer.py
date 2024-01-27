import mysql.connector
import os
from dotenv import load_dotenv
import sys
import json

# 輸入參數不足，直接結束程式
if len(sys.argv) < 2:
    print("argument less than 1")
    sys.exit(1)


load_dotenv()
quaryStr=sys.argv[1]

# 建立與資料庫的連接
connection = mysql.connector.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_DBNAME"),
    port=os.getenv("DATABASE_PORT")
)

cursor = connection.cursor()
cursor.execute(quaryStr)

result = cursor.fetchall()

# 將結果打包成 json 字串
result_json = json.dumps(result, ensure_ascii=False)
for i in result_json:
    print(i, end='')