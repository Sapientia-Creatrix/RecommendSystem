# 這隻程式的目的是讓 express 後端呼叫，並回傳推薦的課程資訊
# 本程式需傳入兩個參數
# user id: 用於識別唯一使用者
# recommendWay: 用於決定要使用哪一種推薦方法，可以為 "recommend", "popularity" 其中之一

from collections import Counter
import json
import random
import sys
import mysql.connector
import os
from dotenv import load_dotenv


RECOMMEND_COURSE_NUM = 50 # 每次回傳的推薦課程數量

# 輸入參數不足，直接結束程式
if len(sys.argv) < 2:
    print("argument less than 2")
    sys.exit(1)


load_dotenv()
userID=sys.argv[1]

# 建立與資料庫的連接
connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    port=os.getenv("PORT")
)

# ------------------- 計算出 skill_counter -------------------
cursor = connection.cursor()
skill_counter = Counter() # 為 hashTable 結構，用於計算要推薦的 skillType 的種類及數量
query = f"SELECT id, skillPrefer FROM user WHERE id = {userID}" # 取得該使用者的 skillPrefer
cursor.execute(query)

user = cursor.fetchone()

if user: # 如果找到該使用者的資料
    skillPrefer_str = user[1] # 取得 skillPrefer 的 JSON 字串
    skillPrefer = json.loads(skillPrefer_str) # 將 JSON 字串轉換為 Python 字典

# else:
    # print("找不到該使用者的資料")

query = f"SELECT id, skillPrefer FROM user"
cursor.execute(query)
users = cursor.fetchall()


similarity_users = []
similarity_limit = 0.3

# 取得最相似的user
for user2 in users:
    skillPrefer2 = json.loads(user2[1])
    len1 = 0
    len2 = 0
    dot_value = 0
    for skill in skillPrefer:
        dot_value += (user[skill] * user2[skill])
        len1 += (user[skill]**2)
        len2 += (user[skill]**2)
    len1 = len1 **0.5
    len2 = len2 **0.5
    cos_value = dot_value / (len1 * len2)
    id1 = json.loads(user[0])
    id2 = json.loads(user2[0])
    if id1 == id2:
        continue
    if similarity_limit < cos_value:
        similarity_users.append(id)
    
# get recommend history

course_set = set()
for similarity_user in similarity_users:
    query = f"select recommendHistory from user where id = {similarity_user}"
    cursor.execute(query)
    result = cursor.fetchone()
    histories = json.loads(result)


    for course in histories:
        course_dict = {
            "id": course["course_id"]
        }
        course_set.add(course_dict)
        

print(result)




cursor.close()
connection.close()