# 這支程式用於使用 chatGPT 利用語意分割 SKILL 欄位

import pandas as pd
from openai import OpenAI

def ChatGPT_Get_Context(client, question):
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "help me seperate different skills with \"@\" no any space, only return result for me, do not have any other text"},
        {"role": "user", "content": question}
    ]
    )
    return completion.choices[0].message.content

client = OpenAI()

# 讀取 CSV 檔案
df = pd.read_csv('Coursera.csv', delimiter=',')  # 假設使用 tab 作為分隔符號

# 取得 Skills 欄位的值
skills_column = df['Skills']

# 將每一列的 skills 字串拆分成單一的技能，以兩個空格為分隔符號
all_skills = []

counter=0
for skills in skills_column:
    message = skills + "\n help me seperate different skills with \"@\" no any space, after that, only return result for me, do not have any other text"
    response=ChatGPT_Get_Context(client, message)
    print(response)
    if counter>1:
        break
