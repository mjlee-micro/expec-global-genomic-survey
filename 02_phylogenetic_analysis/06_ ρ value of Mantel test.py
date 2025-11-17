import pandas as pd
import numpy as np
from skbio.stats.distance import DistanceMatrix, mantel

gen_dist_path = "gen_dist.csv"
geo_dist_path = "geo_dist.csv"
meta_path     = "Supplementary Table 1 with_sharing_prop.csv"
output_path   = "mantel_result_by_Otype.csv"

gen_df = pd.read_csv(gen_dist_path, index_col=0)
geo_df = pd.read_csv(geo_dist_path, index_col=0)
meta   = pd.read_csv(meta_path, dtype=str)

gen_df.index = gen_df.index.str.replace(" ", "_")
gen_df.columns = gen_df.columns.str.replace(" ", "_")
geo_df.index = geo_df.index.str.replace(" ", "_")
geo_df.columns = geo_df.columns.str.replace(" ", "_")
meta["GCA"] = meta["GCA"].str.replace(" ", "_")

common_ids = gen_df.index.intersection(geo_df.index).intersection(meta["GCA"])
gen_df = gen_df.loc[common_ids, common_ids]
geo_df = geo_df.loc[common_ids, common_ids]
meta = meta[meta["GCA"].isin(common_ids)]

gen_df = gen_df.sort_index().sort_index(axis=1)
geo_df = geo_df.loc[gen_df.index, gen_df.columns]

results = []

for otype in meta["O_type"].unique():
    sub_meta = meta[meta["O_type"] == otype]
    ids = sub_meta["GCA"].tolist()

    if len(ids) < 3:
        continue

    try:
        gen_sub = gen_df.loc[ids, ids].copy()
        geo_sub = geo_df.loc[ids, ids].copy()

        
        gen_sub = gen_sub.fillna(gen_sub.mean().mean())
        geo_sub = geo_sub.fillna(geo_sub.mean().mean())

        
        np.fill_diagonal(gen_sub.values, 0)
        np.fill_diagonal(geo_sub.values, 0)

        
        dist1 = DistanceMatrix(gen_sub.values, ids)
        dist2 = DistanceMatrix(geo_sub.values, ids)
        r, p_value, _ = mantel(dist1, dist2, method='pearson', permutations=999)

        results.append({
            "O_type": otype,
            "n_samples": len(ids),
            "Mantel_r": round(r, 4),
            "p_value": p_value
        })

    except Exception as e:
        print(f"⚠️skip O_type: {otype}，error：{str(e)}")
        continue

result_df = pd.DataFrame(results)
result_df.to_csv(output_path, index=False)
print(f"\n✅ Mantel test results：{output_path}")
