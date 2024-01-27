# 本程式的目的是更新使用者的 skillprefer
# 傳入參數:
# userID: 要更新的使用者 id
# updateType: 要更新的類型，有 "buyCourse"、"clickCourse"
# courseID: 觸發更新的課程 id

from collections import Counter
import math
import sys
import mysql.connector
import os
import json
from dotenv import load_dotenv

# 輸入參數不足，直接結束程式
if len(sys.argv) < 4:
    print("argument less than 3")
    sys.exit(1)

load_dotenv()
userID=sys.argv[1]
updateType=sys.argv[2]
courseID=sys.argv[3]

# 建立與資料庫的連接
connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    port=os.getenv("PORT")
)

# 取得 user 的 SkillPrefer
cursor = connection.cursor()
query = f"SELECT skillPrefer FROM user WHERE id = {userID}" # 取得該使用者的 skillPrefer
cursor.execute(query)
userSkillPreferStr = cursor.fetchone()

# 取得 course 的 skillsType
query = f"SELECT skills FROM course WHERE id = {courseID}" # 取得該課程的 skills
cursor.execute(query)
courseSkillsStr = cursor.fetchone()

sepSkills = []
if courseSkillsStr[0] != None:
    sepSkills = courseSkillsStr[0].split("@")

print("sepSkills: \n", sepSkills)
if updateType == "buyCourse":
    userSkillPrefer = json.loads(userSkillPreferStr[0])
    print(userSkillPrefer)
    for skill in sepSkills:
        if userSkillPrefer.get(skill) == None:
            continue

        userSkillPrefer[skill] += math.sqrt(math.pow(2, -(userSkillPrefer[skill] - 0.5)) - 1) ** 3

    # normalize
    sum=0
    for skill in userSkillPrefer:
        sum += userSkillPrefer[skill]
    for skill in userSkillPrefer:
        userSkillPrefer[skill] /= sum

    # 將 userSkillPrefer 轉換為 JSON 字串
    userSkillPreferStr = json.dumps(userSkillPrefer)
    query = f"UPDATE user SET skillPrefer = '{userSkillPreferStr}' WHERE id = {userID}"
    cursor.execute(query)
    connection.commit()
elif updateType == "clickCourse":
    userSkillPrefer = json.loads(userSkillPreferStr[0])
    print(userSkillPrefer)
    for skill in sepSkills:
        if userSkillPrefer.get(skill) == None:
            continue

        userSkillPrefer[skill] += math.sqrt(math.pow(2, -(userSkillPrefer[skill] - 0.5)) - 1) ** 5

    # normalize
    sum=0
    for skill in userSkillPrefer:
        sum += userSkillPrefer[skill]
    for skill in userSkillPrefer:
        userSkillPrefer[skill] /= sum

    # 將 userSkillPrefer 轉換為 JSON 字串
    userSkillPreferStr = json.dumps(userSkillPrefer)
    query = f"UPDATE user SET skillPrefer = '{userSkillPreferStr}' WHERE id = {userID}"
    cursor.execute(query)
    connection.commit()

    print(userSkillPrefer)



cursor.close()
connection.close()