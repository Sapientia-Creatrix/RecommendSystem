# 這隻程式的目的是讓 express 後端呼叫，並回傳推薦的課程資訊
# 本程式需傳入兩個參數
# user id: 用於識別唯一使用者
# recommendWay: 用於決定要使用哪一種推薦方法，可以為 "recommend"

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
recommendWay=sys.argv[2]

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
if(recommendWay=="recommend"):
    query = f"SELECT skillPrefer FROM user WHERE id = {userID}" # 取得該使用者的 skillPrefer
    cursor.execute(query)

    result = cursor.fetchone()

    if result: # 如果找到該使用者的資料
        skillPrefer_str = result[0] # 取得 skillPrefer 的 JSON 字串
        skillPrefer = json.loads(skillPrefer_str) # 將 JSON 字串轉換為 Python 字典
        for i in range(0, RECOMMEND_COURSE_NUM): # 依照 skillPrefer 的權重隨機選擇 skillType
            chosen_skill = random.choices(list(skillPrefer.keys()), weights=list(skillPrefer.values()))[0]
            skill_counter[chosen_skill] += 1
    else:
        print("找不到該使用者的資料")

# ------------------- 計算出 skill_counter END-------------------


# ------------------- 根據 skill_counter 決定 final_result -------------------
final_result=[] # 用於存放最後的結果
chooseCourseId = {} # 用於確保不會重複推薦同一個課程 (因為資料庫中有些課程有重複)
for skill, count in skill_counter.items(): # 依照 skill_counter 去資料庫中找課程
    query = f"SELECT * FROM Course WHERE skills like '%{skill}%' ORDER BY popularity DESC" # 根據 popularity 排序
    cursor.execute(query)
    results = cursor.fetchall()

    counter=0
    for result in results:
        if(result[1] in chooseCourseId):
            continue
        final_result.append(result)
        chooseCourseId[result[1]] = 1

        counter+=1
        if(counter==count):
            break
    
# 根據 result[8] 排序 final_result
final_result.sort(key=lambda x: x[8], reverse=True)
# for result in final_result:
#     print(result[0], result[1], result[5])

# ------------------- 根據 skill_counter 決定 final_result END-------------------

# 將 final_result 轉成 JSON 格式
        
final_result_json = []
for row in final_result:
    course_dict = {
        "id": row[0],
        "name": row[1],
        "name": row[2],
        "url": row[3],
        "difficulty": row[4],
        "rate": row[5],
        # "description": row[6],
        "skills": row[7],
        "deleted": row[8]
    }
    final_result_json.append(course_dict)

json_result = json.dumps(final_result_json)
print(json_result)


cursor.close()
connection.close()