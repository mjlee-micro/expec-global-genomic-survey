import pandas as pd
from scipy.stats import pearsonr

# === 读取数据 ===
mantel_df = pd.read_csv(r"mantel_result_by_Otype.csv")
meta_df = pd.read_csv(r"Supplementary Table 1_with_sharing_prop.csv")

mantel_df.columns = mantel_df.columns.str.strip()
meta_df.columns = meta_df.columns.str.strip()

sharing_df = meta_df.groupby("O_type", as_index=False).agg({
    "sharing_prop": "mean"
})

merged_df = pd.merge(mantel_df, sharing_df, on="O_type", how="inner")

df_clean = merged_df[["sharing_prop", "Mantel_r"]].dropna()

r, p_value = pearsonr(df_clean["sharing_prop"], df_clean["Mantel_r"])
r_squared = r ** 2

print(f"✅ Pearson R² = {r_squared:.3f}, p = {p_value:.2e}")
