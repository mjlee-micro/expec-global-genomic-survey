import os
import pandas as pd
from sklearn.cluster import KMeans

vir_path = r"C:\Users\93966\Desktop\VFDB_annoted.txt"
res_path = r"C:\Users\93966\Desktop\CARD_annoted.txt"
sero_path = r"C:\Users\93966\Desktop\serotype_annoted.txt"
output_dir = r"C:\Users\93966\Desktop\output"
os.makedirs(output_dir, exist_ok=True)

try:
    vir = pd.read_csv(vir_path, sep='\t', index_col=0, encoding='utf-8')
    res = pd.read_csv(res_path, sep='\t', index_col=0, encoding='utf-16')  
    sero = pd.read_csv(sero_path, sep='\t', index_col=0, encoding='utf-8')
except UnicodeDecodeError:
       res = pd.read_csv(res_path, sep='\t', index_col=0, encoding='latin1')  

common_samples = vir.index.intersection(res.index).intersection(sero.index)
vir = vir.loc[common_samples]
res = res.loc[common_samples]
sero = sero.loc[common_samples]

def preprocess_data(df):
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.fillna(0)
    return df

vir = preprocess_data(vir)
res = preprocess_data(res)

def cluster_and_label(matrix, n_clusters=5, prefix="Module"):
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(matrix)
    labels = [f"{prefix}_{i+1}" for i in kmeans.labels_]
    return labels, kmeans.labels_

vir_labels_str, vir_labels = cluster_and_label(vir, n_clusters=5, prefix="Vir")
res_labels_str, res_labels = cluster_and_label(res, n_clusters=5, prefix="Res")

result_df = pd.DataFrame(index=common_samples)
result_df["O_Serotype"] = sero["serotype"]
result_df["Vir_Module"] = vir_labels_str
result_df["Res_Module"] = res_labels_str

sero_vir_pivot = result_df.pivot_table(index="O_Serotype", columns="Vir_Module", aggfunc="size", fill_value=0)
sero_res_pivot = result_df.pivot_table(index="O_Serotype", columns="Res_Module", aggfunc="size", fill_value=0)

vir["Cluster"] = vir_labels
vir_module_repr = vir.groupby("Cluster").sum().T
top_vir_genes = vir_module_repr.apply(lambda x: x.sort_values(ascending=False).head(5).index.tolist(), axis=0)

res["Cluster"] = res_labels
res_module_repr = res.groupby("Cluster").sum().T
top_res_genes = res_module_repr.apply(lambda x: x.sort_values(ascending=False).head(5).index.tolist(), axis=0)

result_df.to_csv(os.path.join(output_dir, "cluaster lable.csv"), encoding="utf-8-sig")
sero_vir_pivot.to_csv(os.path.join(output_dir, "serotype_vs_virulence.csv"), encoding="utf-8-sig")
sero_res_pivot.to_csv(os.path.join(output_dir, "serotype_vs_resistance.csv"), encoding="utf-8-sig")
pd.DataFrame(top_vir_genes).to_csv(os.path.join(output_dir, "virulence represent genes.csv"), encoding="utf-8-sig")
pd.DataFrame(top_res_genes).to_csv(os.path.join(output_dir, "resistance represent genes.csv"), encoding="utf-8-sig")

print("done：", output_dir)