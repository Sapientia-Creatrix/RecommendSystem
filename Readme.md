# LearningCourseRecommender 使用範例
這隻程式的目的是讓 express 後端呼叫，並回傳推薦的課程 id 與評分
本程式需傳入兩個參數
user id: 用於識別唯一使用者
recommendType: 用於決定要使用哪一種推薦方法，可以為 "highestRating"

## 執行
```
python -u "e:\progremmingFile\Github\Sapientia-Creatrix\RecommendSystem\LearningCourseRecommender.py" 0 highestRating
```
## 回傳結果 (於終端機中顯示)
```
[{"id": 2560, "rate": 5.0}, {"id": 2565, "rate": 5.0}, {"id": 1033, "rate": 5.0}, {"id": 2574, "rate": 5.0}, {"id": 28, "rate": 5.0}, {"id": 1054, "rate": 5.0}, {"id": 800, "rate": 5.0}, {"id": 1312, "rate": 5.0}, {"id": 34, "rate": 5.0}, {"id": 550, "rate": 5.0}]
```