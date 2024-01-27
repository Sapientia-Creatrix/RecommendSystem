import pandas as pd
import shutil

df = pd.read_csv("./Coursera_NewSkill_v2.csv")

# 定义条件
condition_course_name_university = df['Course Name'].str.match(r'^[a-zA-Z0-9\s]+$')
condition_difficulty_level = df['Difficulty Level'].isin(['Conversant', 'Advanced', 'Beginner', 'Intermediate', 'Not Calibrated'])
# condition_course_rating = df['Course Rating'].apply(lambda x: isinstance(x, (int, float)))
condition_course_description = df['Course Description'].str.match(r'^[a-zA-Z0-9\s\.,\'";:!&\(\)\-\?]+$')
condition_sepskills = df['sepSkills'].str.startswith('@')

# 应用条件进行过滤
df = df[condition_course_name_university & condition_difficulty_level  &
        condition_course_description & condition_sepskills]

# # 定义条件
# valid_difficulty_levels = ('Conversant', 'Advanced', 'Beginner', 'Intermediate', 'Not Calibrated')

# # 删除不符合条件的行
# df = df[df['Difficulty Level'].isin(valid_difficulty_levels)]
# df = df[pd.to_numeric(df['Course Rating'], errors='coerce').notna()]  # 确保Course Rating是数字
# df = df[df['sepSkills'].str.startswith('@')]

# # 刪除rating不等於數字 或 sepSkills不是@開頭
# df = df[df['Difficulty Level'].str.isalpha() & 
#         pd.to_numeric(df['Course Rating'], errors='coerce').notna() & 
#         df['sepSkills'].astype(str).str.startswith('@') ]

# 刪除欄位數量不等於8的
df = df[df.apply(lambda x: x.count() == 8, axis=1)]

# 将过滤后的DataFrame写回CSV文件
df.to_csv("./Coursera_NewSkill.csv", index=False)

# 把./Coursera_NewSkill.csv 複製到 C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Coursera_NewSkill.csv
shutil.copy("./Coursera_NewSkill.csv", "C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Coursera_NewSkill.csv")