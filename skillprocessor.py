# 這支程式的功能是讀取 Coursera_NewSkill.csv 檔案，並將所有的技能列出來，並計算每個技能出現的次數

from collections import Counter
import pandas as pd
import re

# 讀取 CSV 檔案
df = pd.read_csv('Coursera_NewSkill.csv', delimiter=',')  # 假設使用 tab 作為分隔符號

# 取得 Skills 欄位的值
skills_column = df['sepSkills']

# 將每一列的 skills 字串拆分成單一的技能，以兩個空格為分隔符號
all_skills = []
for skills in skills_column:
    skills=str(skills)
    result_list = skills.split("@")
    all_skills.extend(result_list)

# # 列出不重複的技能
# unique_skills = set(all_skills)

# # 排序
# unique_skills = sorted(unique_skills)

# # 印出結果
# print("不重複的技能:")
# for skill in unique_skills:
#     print(skill)

# # 計算出技能數量
# print("總共有 %d 種技能" % len(unique_skills))
    
skill_counts = Counter(all_skills)

sorted_skill_counts = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)

# 印出不同技能及其次數 (已排序)
for skill, count in sorted_skill_counts:
    # print(f"{skill}: {count} times")
    print(skill)
