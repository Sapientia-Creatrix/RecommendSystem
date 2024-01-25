# 定義數列
original_sequence = [1, 2, 5, 4, 5]

# 計算分布
result_sequence = [1 / (2**(n)) for n in range(1, len(original_sequence) + 1)]

# 輸出結果
print("原始數列:", original_sequence)
print("分布結果:", result_sequence)
