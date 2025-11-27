import pandas as pd
import numpy as np
from scipy.stats import f_oneway

file_path = r"Swimming motility/Iron-limitation assay.xlsx"
df = pd.read_excel(file_path)

df.columns = df.columns.str.strip()

df["serotype"] = df["serotype"].astype(str).str.strip()

long_df = df.melt(
    id_vars=["sample", "serotype"],
    value_vars=["diameter1", "diameter2", "diameter3"],  
    var_name="replicate",
    value_name="diameter"
)

grouped_data = []
for serotype, group in long_df.groupby("serotype"):
    values = group["diameter"].dropna().values
    print(f"{serotype}: n={len(values)}")  
    if len(values) >= 2:
        grouped_data.append(values)

if len(grouped_data) >= 2:
    res = f_oneway(*grouped_data)
    k = len(grouped_data)             
    N = sum(len(g) for g in grouped_data)  
    df1 = k - 1
    df2 = N - k

    print("ANOVA test of Iron-limitation assay")
    print(f"F({df1},{df2}) = {res.statistic:.4f}, p = {res.pvalue:.6g}")

    if res.pvalue < 0.0001:
        p_text = "p < 0.0001"
    else:
        p_text = f"p = {res.pvalue:.4f}"
    print(f"ANOVA, F({df1},{df2}) = {res.statistic:.2f}, {p_text}")
else:
    print("unable to test")
