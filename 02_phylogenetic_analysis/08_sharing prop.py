import pandas as pd
import numpy as np
from itertools import combinations

# 1. 读取你的元数据（Excel 格式）
#    确保这张表里至少有列：sample, serotype, continent, st
meta = pd.read_excel(r"D:\研究生\1.大肠埃希菌\论文\附表1.xlsx", dtype=str)

# 检查必需的列是否存在
for col in ("sample", "serotype", "continent", "st"):
    if col not in meta.columns:
        raise ValueError(f"元数据中缺少必需列: '{col}'")

# 2. 按大洲计算 “不同血清型” 间的 ST sharing_prop
def calc_sharing_prop(sub: pd.DataFrame) -> float:
    total = shared = 0
    for i, j in combinations(sub.index, 2):
        # 只统计不同血清型的样本对
        if sub.at[i, "serotype"] != sub.at[j, "serotype"]:
            total += 1
            # 如果两株属于同一个 ST，则计为“shared”
            if sub.at[i, "st"] == sub.at[j, "st"]:
                shared += 1
    return shared / total if total > 0 else np.nan

res = (
    meta
    .groupby("continent")
    .apply(calc_sharing_prop)
    .reset_index(name="sharing_prop")
)

# 3. 合并结果并导出
out = meta.merge(res, on="continent", how="left")
out.to_csv(r"D:\研究生\1.大肠埃希菌\论文\附表1_with_sharing_prop.csv", index=False)

print("Done! 结果保存在 '附表1_with_sharing_prop.csv'。")
