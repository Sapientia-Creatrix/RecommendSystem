# 這隻程式的目的是讓 express 後端呼叫，並回傳推薦的課程資訊，使用基於內容過濾的特徵向量演算法
# 本程式需傳入一個參數
# user id: 用於識別唯一使用者

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
    print("argument less than 1")
    sys.exit(1)


load_dotenv()
userID=sys.argv[1]

# 建立與資料庫的連接
connection = mysql.connector.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_DBNAME"),
    port=os.getenv("DATABASE_PORT")
)

# ------------------- 計算出 skill_counter -------------------
cursor = connection.cursor()
skill_counter = Counter() # 為 hashTable 結構，用於計算要推薦的 skillType 的種類及數量
query = f"SELECT skillPrefer FROM user WHERE id = {userID}" # 取得該使用者的 skillPrefer
cursor.execute(query)

result = cursor.fetchone()

user_len = 0 # 該使用者的 skillPrefer 的長度


if result: # 如果找到該使用者的資料
    skillPrefer_str = result[0] # 取得 skillPrefer 的 JSON 字串
    skillPrefer = json.loads(skillPrefer_str) # 將 JSON 字串轉換為 Python 字典
    # print(skillPrefer)
    for skill in skillPrefer:
        user_len += (skillPrefer[skill])**2
    user_len = user_len ** 0.5
else:
    print("找不到該使用者的資料")

# ------------------- 計算出 skill_counter END-------------------


# ------------------- 根據 skill_counter 決定 final_result -------------------
# 取得 user 的 recommendHistory
query = f"SELECT * FROM Course"
cursor.execute(query)
results = cursor.fetchall()

allCourse = [] # 用於存放所有課程的 cos 值及對應的 id
for result in results:
    if result[7] !=None: # 如果 sepSkills 欄位不為空
        sepSkills = result[7].split("@") # 將 skills 用逗號分隔

        # 計算出user skillPrefer 向量與該課程 skillType 向量的 cos 值
        course_len = 0
        dot_value = 0 # 內積
        for skill in sepSkills:
            course_len += 1
            if(skillPrefer.get(skill) == None):
                continue
            dot_value += (skillPrefer[skill] * 1)
        course_len = course_len ** 0.5
        cos_value = dot_value / (user_len * course_len)
        allCourse.append([cos_value, result[0], result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8], result[9]])

# 依照 cos 值排序
allCourse.sort(key=lambda x: x[0], reverse=True)

# 從 allCourse 中挑出課程
# 取得 user 的 recommendHistory
query = f"SELECT recommendHistory FROM user WHERE id = {userID}"
cursor.execute(query)
result = cursor.fetchone()
recommendHistory = json.loads(result[0])

final_result=[] # 用於存放最後的結果
chooseCourseId = {} # 用於確保不會重複推薦同一個課程 (因為資料庫中有些課程有重複)
for course in allCourse:
    if(course[1] in chooseCourseId): # 如果出現重複的課程，則跳過
        continue

    skipThisCourse = False # 用於確認是否要跳過這個課程
    for history in recommendHistory:
        if(history["course_id"]==result[0]): # 如果這個課程已經被推薦過了，則有概率跳過
            prob = 1 / (2**(history["RecommendFrequency"]))
            if(random.random() > prob):
                skipThisCourse = True
                break

    if(skipThisCourse):
        continue

    final_result.append([course[1], course[2], course[3], course[4], course[5], course[6], course[7], course[8], course[9], course[10]])
    chooseCourseId[course[1]] = True
    if(len(final_result) >= RECOMMEND_COURSE_NUM): # 如果已經達到推薦數量，則跳出迴圈
        break

final_result_json = []
for row in final_result:
    course_dict = {
        "id": row[0],
        #"name": row[1],
        #"university": row[2],
        #"url": row[3],
        #"difficulty": row[4],
        #"rate": row[5],
        #"description": row[6],
        #"skills": row[7],
        #"popularity": row[8],
        #"deleted": row[9]
    }
    final_result_json.append(course_dict)
    #print(row[7])

json_result = json.dumps(final_result_json)
print(json_result)


cursor.close()
connection.close()