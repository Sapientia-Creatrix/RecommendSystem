import subprocess

# 測試TestLearningCourseRecommender.py
try:
    file_path = 'LearningCourseRecommender.py'
    user_id = '1'
    recommend_way = 'recommend'
    result = subprocess.run(['python', file_path, user_id, recommend_way], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    print(output)

    user_id = '1'
    recommend_way = 'popularity'
    result = subprocess.run(['python', file_path, user_id, recommend_way], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    print(output)
except Exception as e:
    print(e)

# 測試TestLearningCourseRecommender_collaborative.py
try:
    file_path = 'LearningCourseRecommender_collaborative.py'
    user_id = '1'
    result = subprocess.run(['python', file_path, user_id], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    print(output)
except Exception as e:
    print(e)

# 測試TestLearningCourseRecommender_advance.py
try:
    file_path = 'LearningCourseRecommender_advance.py'
    user_id = '1'
    result = subprocess.run(['python', file_path, user_id], stdout=subprocess.PIPE, text=True)
    output = result.stdout
    print(output)
except Exception as e:
    print(e)