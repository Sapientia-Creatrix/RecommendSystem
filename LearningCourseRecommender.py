# 這隻程式的目的是讓 express 後端呼叫，並回傳推薦的課程 id 與評分
# 本程式需傳入兩個參數
# user id: 用於識別唯一使用者
# recommendType: 用於決定要使用哪一種推薦方法，可以為 "highestRating"

import json
import sys
import mysql.connector
import os
from dotenv import load_dotenv

# 輸入參數不足，直接結束程式
if len(sys.argv) < 2:
    print("argument less than 2")
    sys.exit(1)

load_dotenv()
userID=sys.argv[1]
recommendType=sys.argv[2]

# 建立與資料庫的連接
connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    port=os.getenv("PORT")
)


cursor = connection.cursor()
if(recommendType=="highestRating"):
    query = "SELECT * FROM Course ORDER BY rate DESC LIMIT 10"
    cursor.execute(query)
    results = cursor.fetchall()

    courses_list = []
    for row in results:
        course_dict = {
            "id": row[0],  # 使用適當的鍵名稱
            "rate": row[5]  # 使用適當的鍵名稱
        }
        courses_list.append(course_dict)
    
    json_result = json.dumps(courses_list)
    print(json_result)



cursor.close()
connection.close()