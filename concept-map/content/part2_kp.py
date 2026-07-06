# -*- coding: utf-8 -*-
"""Part 2 模擬實戰各題 → 對應考點（供錯題導回考點複習）。
每個 slug 一串 kp（依 Part 2 題目出現順序，含單選／多選／選填各組）；長度＝該單元 Part 2 題數。
依各題「解題核心」對應。若 Part 2 增刪題，這裡的清單要同步（位置對應）。
考點若在 content/<slug>.py 的 Part2 題目內嵌 "kp"，以內嵌者為優先。
"""

PART2_KP = {
    # 數與式 kp1實數 kp2絕對值 kp3數線根號 kp4乘法算幾 kp5比例加權 kp6高斯
    "numexpr": ["kp2", "kp3", "kp2", "kp4", "kp3", "kp2", "kp2", "kp4", "kp3", "kp2", "kp4", "kp5"],
    # 多項式 kp1除法餘式 kp2二次判別配方 kp3方程不等式 kp4高次有理根勘根 kp5三次對稱
    "poly": ["kp1", "kp1", "kp2", "kp2", "kp5", "kp2", "kp4", "kp1", "kp3", "kp5"],
    # 指對 kp1指數律 kp2對數運算 kp3常用對數位數 kp4指對圖形 kp5應用數列
    "explog": ["kp1", "kp2", "kp2", "kp3", "kp1", "kp3", "kp4", "kp1", "kp2", "kp5"],
    # 數列 kp1等差 kp2等比 kp3遞迴 kp4級數週期
    "seq": ["kp1", "kp1", "kp2", "kp2", "kp1", "kp1", "kp2", "kp1", "kp2", "kp4"],
    # 機率 kp1計數排列 kp2組合分組 kp3古典機率 kp4條件貝氏 kp5獨立餘事件 kp6期望值
    "prob": ["kp1", "kp2", "kp3", "kp4", "kp6", "kp5", "kp2", "kp1", "kp4", "kp3", "kp6"],
    # 數據 kp1一維標準差 kp2相關係數 kp3迴歸 kp4加權判讀
    "data": ["kp1", "kp1", "kp1", "kp2", "kp3", "kp1", "kp2", "kp4", "kp4", "kp1"],
    # 三角 kp1三角比弧度 kp2正餘弦定理 kp3三角測量 kp4三角函數圖形 kp5和差倍角 kp6角平分面積比 kp7圓周角二面角
    "trig": ["kp1", "kp1", "kp2", "kp2", "kp4", "kp4", "kp5", "kp6", "kp7", "kp3"],
    # 直線與圓 kp1直線斜率 kp2兩點距離三角形 kp3圓方程 kp4直線與圓位置 kp5平面區域線性規劃
    "linecir": ["kp1", "kp1", "kp2", "kp3", "kp4", "kp1", "kp4", "kp4", "kp5", "kp4"],
    # 平面向量 kp1表示運算 kp2線性組合分點面積比 kp3內積 kp4行列式面積 kp5旋轉坐標應用
    "pvec": ["kp1", "kp1", "kp3", "kp3", "kp4", "kp3", "kp2", "kp2", "kp5", "kp4"],
    # 空間 kp1坐標距離 kp2內積垂直 kp3外積體積 kp4平面方程距離 kp5空間直線歪斜 kp6二面角立體
    "space": ["kp1", "kp2", "kp3", "kp4", "kp3", "kp2", "kp4", "kp3", "kp5", "kp2"],
    # 矩陣 kp1意義相等乘法 kp2高次方 kp3反方陣解方程 kp4一次聯立高斯 kp5平面線性變換
    "matrix": ["kp2", "kp2", "kp3", "kp5", "kp4", "kp1", "kp5", "kp4", "kp1", "kp2", "kp5", "kp4", "kp5"],
}
