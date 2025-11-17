import pandas as pd
import numpy as np
from skbio import TreeNode

tree_path = "phylotree.treefile"
meta_path = "Supplementary Table 1_with_sharing_prop.csv"
output_path = "gen_dist.csv"

tree = TreeNode.read(tree_path)
dm = tree.cophenet(use_length=True)
df = dm.to_data_frame()

meta = pd.read_csv(meta_path, dtype=str)
meta["GCA"] = meta["GCA"].str.replace(" ", "_")
full_ids = sorted(meta["GCA"].unique())  

full_df = pd.DataFrame(np.nan, index=full_ids, columns=full_ids)

intersect_ids = df.index.intersection(full_df.index)
full_df.loc[intersect_ids, intersect_ids] = df.loc[intersect_ids, intersect_ids]

for i in full_df.index:
    for j in full_df.columns:
        if pd.isna(full_df.loc[i, j]) and not pd.isna(full_df.loc[j, i]):
            full_df.loc[i, j] = full_df.loc[j, i]
        elif not pd.isna(full_df.loc[i, j]) and pd.isna(full_df.loc[j, i]):
            full_df.loc[j, i] = full_df.loc[i, j]

full_df.to_csv(output_path, float_format="%.5f")
print(f"done：{output_path}")
