# 本程式會從 user table 中的 skill 欄位取得使用者的技能，利用自然語言處理更新 user table 中的 skillPrefer 欄位，進而影響到推薦結果
# (未完成)

# 本程式需傳入三個參數
# user id: 用於識別唯一使用者
# recommendWay: 用於決定要使用哪一種推薦方法，可以為 "recommend"
# sortWay: 用於決定要使用哪一種排序方法決定結果的順序，可以為 "rating"

import json
import sys
import mysql.connector
import os
from dotenv import load_dotenv
import vertexai
from vertexai.preview.language_models import TextGenerationModel

def predict_large_language_model(
    model_name: str,
    temperature: float,
    max_output_tokens: int,
    top_p: float,
    top_k: int,
    content: str,
    tuned_model_name: str = "",
    ) :
    
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
      model = model.get_tuned_model(tuned_model_name)
    response = model.predict(
        content,
        temperature=temperature,
        max_output_tokens=max_output_tokens,
        top_k=top_k,
        top_p=top_p,)
    return response.text

skillType = '''
Business
Computer Science
Data Science
nan
Health
Physical Science and Engineering
Social Sciences
Software Development
Arts and Humanities
Data Analysis
Machine Learning
Information Technology
Leadership and Management
Business Essentials
Business Strategy
Education
Music and Art
Personal Development
Finance
Marketing
Language Learning
Public Health
Mobile and Web Development
Mechanical Engineering
Electrical Engineering
Learning English
Governance and Society
Basic Science
Cloud Computing
Entrepreneurship
History
Design and Product
Environmental Science and Sustainability
Computer Security and Networks
Patient Care
Algorithms
Math and Logic
Security
Philosophy
Physics and Astronomy
Health Informatics
Probability and Statistics
Law
Psychology
Data Management
Healthcare Management
Research
Economics
Chemistry
Other Languages
Support and Operations
Research Methods
Networking
Animal Health
Nutrition
'''

# 輸入參數不足，直接結束程式
if len(sys.argv) < 3:
    print("argument less than 3")
    sys.exit(1)

load_dotenv()
vertexai.init(project="tsmccareerhack2024-bsid-grp2")

userID=sys.argv[1]
recommendWay=sys.argv[2]
sortWay=sys.argv[3]

# 建立與資料庫的連接
connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    user=os.getenv("USER"),
    password=os.getenv("PASSWORD"),
    database=os.getenv("DATABASE"),
    port=os.getenv("PORT")
)


cursor = connection.cursor()
if(recommendWay=="recommend"):
    # 設定 prompt
    prompt = '''
    input: this is a user's self introduction, containing his/her skills and interests description
    "{userSkill}"

    for the EVERY skillType as described below, give me the score scale from 0 to 1, which mean the Correlation between user's self introduction and the skillType, and sorted by the score in descending order
    skillType:
    {skillType}

    Note: YOU NEED TO GIVEN THE SCORE FOR EVERY SKILLTYPE, EVEN IF THE SCORE IS 0

    response format example:
    Business: 0.98
    Computer Science: 0.95
    ... and so on

    '''

    content = prompt.format(userSkill="my dream is to be a teacher", skillType=skillType)

    response_text = predict_large_language_model(
        "text-bison@001", 
        temperature=0.2, 
        max_output_tokens=1024, 
        top_p=0.8, 
        top_k=1, 
        content=content
        )

    print(response_text)


    # query = "SELECT * FROM Course ORDER BY rate DESC LIMIT 10"
    # cursor.execute(query)
    # results = cursor.fetchall()

    # courses_list = []
    # for row in results:
    #     course_dict = {
    #         "id": row[0],  # 使用適當的鍵名稱
    #         "rate": row[5]  # 使用適當的鍵名稱
    #     }
    #     courses_list.append(course_dict)
    
    # json_result = json.dumps(courses_list)
    # print(json_result)



cursor.close()
connection.close()