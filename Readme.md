# LearningCourseRecommender 使用範例
這隻程式的目的是讓 express 後端呼叫，並回傳推薦的課程 id
本程式需傳入兩個參數
user id: 用於識別唯一使用者
recommend: 用於判斷推薦課程的方式，可以為 recommend 或 popularity

## 執行
```
python -u "e:\progremmingFile\Github\Sapientia-Creatrix\RecommendSystem\LearningCourseRecommender.py"1 recommend
```
## 回傳結果 (於終端機中顯示)
```
[{"id": 561}, {"id": 2841}, {"id": 377}, {"id": 3162}, {"id": 2808}, {"id": 2066}, {"id": 3485}, {"id": 1548}, {"id": 
2645}, {"id": 568}, {"id": 467}, {"id": 871}, {"id": 1866}, {"id": 3427}, {"id": 616}, {"id": 2663}, {"id": 2695}, {"id": 1127}, {"id": 1024}, {"id": 935}, {"id": 2810}, {"id": 2882}, {"id": 1509}, {"id": 7}, {"id": 518}, {"id": 1205}, 
{"id": 2215}, {"id": 1033}, {"id": 1768}, {"id": 1937}, {"id": 3270}, {"id": 791}, {"id": 1045}, {"id": 1974}, {"id": 
350}, {"id": 485}, {"id": 373}, {"id": 2047}, {"id": 2395}, {"id": 3520}, {"id": 1698}, {"id": 2370}, {"id": 2753}, {"id": 2554}, {"id": 1153}, {"id": 1223}, {"id": 1892}, {"id": 261}, {"id": 2139}, {"id": 1066}]
```

# LearningCourseRecommender_advance 使用範例
跟上面的程式類似，但原理是基於內容過濾的特徵向量演算法

## 執行
```
 python -u "e:\progremmingFile\Github\Sapientia-Creatrix\RecommendSystem\LearningCourseRecommender_advance.py" 1
```

## 回傳結果 (於終端機中顯示)
```
[{"id": 147}, {"id": 153}, {"id": 171}, {"id": 174}, {"id": 242}, {"id": 245}, {"id": 253}, {"id": 261}, {"id": 297}, 
{"id": 327}, {"id": 344}, {"id": 348}, {"id": 365}, {"id": 373}, {"id": 390}, {"id": 437}, {"id": 566}, {"id": 631}, {"id": 633}, {"id": 649}, {"id": 832}, {"id": 843}, {"id": 875}, {"id": 876}, {"id": 877}, {"id": 951}, {"id": 953}, {"id": 987}, {"id": 1010}, {"id": 1066}, {"id": 1120}, {"id": 1153}, {"id": 1185}, {"id": 1206}, {"id": 1221}, {"id": 1223}, {"id": 1252}, {"id": 1259}, {"id": 1323}, {"id": 1361}, {"id": 1470}, {"id": 1503}, {"id": 1524}, {"id": 1534}, {"id": 1556}, {"id": 1596}, {"id": 1619}, {"id": 1627}, {"id": 1649}, {"id": 1683}]
```
