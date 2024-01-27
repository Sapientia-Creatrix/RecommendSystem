# 這隻程式的目的是讓 express 後端呼叫，並回傳推薦的課程資訊
# 本程式需傳入兩個參數
# user id: 用於識別唯一使用者

from collections import Counter
import json
import random
import sys
import mysql.connector
import os
from dotenv import load_dotenv


RECOMMEND_COURSE_NUM = 50 # 每次回傳的推薦課程數量
SIMILARITY_LIMIT = 0.3 # 相似度門檻值，大於此值的使用者才會被視為同背景的使用者

# 輸入參數不足，直接結束程式
if len(sys.argv) < 2:
    print("argument less than 1")
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


similarity_users = [] # 用於存放相似度大於 SIMILARITY_LIMIT 的使用者 id
for user2 in users: # 對於每一個使用者
    skillPrefer2 = json.loads(user2[1]) # 取得其 skillPrefer 的 JSON 字串
    len1 = 0
    len2 = 0
    dot_value = 0
    for skill in skillPrefer: # 計算跟當前使用者相似度的 cosine similarity
        dot_value += (skillPrefer[skill] * skillPrefer2[skill])
        len1 += (skillPrefer[skill]**2)
        len2 += (skillPrefer[skill]**2)
    len1 = len1 **0.5
    len2 = len2 **0.5
    cos_value = dot_value / (len1 * len2)
    id1 = user[0]
    id2 = user2[0]
    if id1 == id2:
        continue
    if SIMILARITY_LIMIT < cos_value: # 如果相似度大於 SIMILARITY_LIMIT
        similarity_users.append(id2) # 將該使用者加入 similarity_users

# 取得 similarity_users 的 recommendHistory
recommendCourseSet = [] # 用於存放所有推薦課程的 id (基於相似使用者的歷史紀錄)
for similarity_user in similarity_users:
    query = f"select recommendHistory from user where id = {similarity_user}"
    cursor.execute(query)
    result = cursor.fetchone()
    histories = json.loads(result[0]) # 取得該使用者的 recommendHistory (JSON 字串) 

    for course in histories:
        recommendCourseSet.append(course["course_id"])
        

# 取得 user 的 recommendHistory
query = f"SELECT recommendHistory FROM user WHERE id = {userID}"
cursor.execute(query)
result = cursor.fetchone()
recommendHistory = json.loads(result[0])

final_result=[] # 用於存放最後的結果
chooseCourseId = {} # 用於確保不會重複推薦同一個課程 (因為資料庫中有些課程有重複)
for courseID in recommendCourseSet: # 遍歷recommendCourseSet
    if(courseID in chooseCourseId): # 如果出現重複的課程，則跳過
        continue

    skipThisCourse = False # 用於確認是否要跳過這個課程
    for history in recommendHistory:
        if(history["course_id"]==courseID): # 如果這個課程已經被推薦過了，則有概率跳過
            prob = 1 / (2**(history["RecommendFrequency"]))
            if(random.random() > prob):
                skipThisCourse = True
                break

    if(skipThisCourse):
        continue

    final_result.append(courseID)
    chooseCourseId[courseID] = 1

    if(len(final_result)==RECOMMEND_COURSE_NUM):
        break

# 將 final_result 轉成 JSON 格式
        
final_result_json = []
for row in final_result:
    course_dict = {
        "id": row,
        #"name": row[1],
        #"university": row[2],
        #"url": row[3],
        #"difficulty": row[4],
        #"rate": row[5],
        # "description": row[6],
        #"skills": row[7],
        #"popularity": row[8],
        #"deleted": row[9]
    }
    final_result_json.append(course_dict)

json_result = json.dumps(final_result_json)
print(json_result)


cursor.close()
connection.close()