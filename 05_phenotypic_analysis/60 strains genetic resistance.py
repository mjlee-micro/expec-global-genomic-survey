# -*- coding: utf-8 -*-
import pandas as pd
import os
from pathlib import Path

MATRIX_PATH = r"C:\Users\Desktop\60 strain.txt"                           # sample×resistance gene 0/1 matrix
SERO_PATH   = r"C:\Users\Desktop\serotype annotion.txt"                            
AMR_PATH    = r"C:\Users\Desktop\resistance annotion.txt"  

SAMPLE_COL_IN_MATRIX = None   
SERO_SAMPLE_COL = "Sample"    
SERO_GROUP_COL  = "serotype"  
AMR_GENE_COL    = "Sample"      
AMR_TYPE_COL    = "Resistance"  

OUT_DIR = str(Path(MATRIX_PATH).parent)
OUT_01  = os.path.join(OUT_DIR, "Serogroup_AMRtype_01_matrix.tsv")
OUT_PROP = os.path.join(OUT_DIR, "Serogroup_AMRtype_proportion.tsv")  
# ==================================

def read_any(path):
       for enc in ["utf-8", "utf-8-sig", "gbk"]:
        try:
            return pd.read_csv(path, sep=None, engine="python", encoding=enc)
        except Exception:
            continue
    raise RuntimeError(f"unable to read：{path}")

def main():
    mat = read_any(MATRIX_PATH)
    sero = read_any(SERO_PATH)
    amr = read_any(AMR_PATH)

    if SAMPLE_COL_IN_MATRIX and SAMPLE_COL_IN_MATRIX in mat.columns:
        mat = mat.set_index(SAMPLE_COL_IN_MATRIX)
    else:
        if mat.shape[1] >= 2:
            mat = mat.set_index(mat.columns[0])
        else:
            raise ValueError("unable to identity sample ID")

    mat = mat.apply(pd.to_numeric, errors="coerce").fillna(0)
    mat = (mat > 0).astype(int)

    for need_col, df, name in [
        (SERO_SAMPLE_COL, sero, "serotype annotion"),
        (SERO_GROUP_COL, sero, "serotype annotion"),
        (AMR_GENE_COL, amr, "resistance annotion"),
        (AMR_TYPE_COL, amr, "resistance annotion"),
    ]:
        if need_col not in df.columns:
            raise KeyError(f"{name} error：{need_col}")

    sero = sero[[SERO_SAMPLE_COL, SERO_GROUP_COL]].dropna()
    sero = sero[sero[SERO_SAMPLE_COL].astype(str).isin(mat.index.astype(str))].copy()

    mat.columns = mat.columns.astype(str)
    amr[AMR_GENE_COL] = amr[AMR_GENE_COL].astype(str)

    amr = amr[[AMR_GENE_COL, AMR_TYPE_COL]].dropna()
    amr = amr[amr[AMR_GENE_COL].isin(mat.columns)].copy()

    long_df = mat.reset_index().rename(columns={mat.index.name or 'index': 'sample_id'})
    long_df = long_df.melt(id_vars=['sample_id'], var_name='gene', value_name='presence')
    long_df = long_df[long_df['presence'] > 0]

    long_df = long_df.merge(sero.rename(columns={SERO_SAMPLE_COL: 'sample_id', SERO_GROUP_COL: 'serogroup'}),
                            on='sample_id', how='inner')
    long_df = long_df.merge(amr.rename(columns={AMR_GENE_COL: 'gene', AMR_TYPE_COL: 'amr_type'}),
                            on='gene', how='inner')

    if long_df.empty:
        raise ValueError("Check if the sample ID, gene name, and annotation are consistent.")

    grp_any = (long_df
               .groupby(['serogroup', 'amr_type'])['presence']
               .max()  
               .unstack(fill_value=0)
               .astype(int)
               .sort_index()
               )

    sample_type_any = (long_df
                       .groupby(['sample_id', 'serogroup', 'amr_type'])['presence']
                       .max()
                       .reset_index())

    serogroup_sizes = sample_type_any.groupby('serogroup')['sample_id'].nunique()

    prop = (sample_type_any
            .groupby(['serogroup', 'amr_type'])['presence'].mean()  
            .unstack(fill_value=0.0)
            .reindex(index=grp_any.index, columns=grp_any.columns, fill_value=0.0)
            .sort_index()
            )

    grp_any.to_csv(OUT_01, sep="\t", encoding="utf-8")
    prop.to_csv(OUT_PROP, sep="\t", encoding="utf-8")

    print(f"A 0/1 matrix has been generated.：{OUT_01}")
    print(f"A scale matrix has been generated.：{OUT_PROP}")
if __name__ == "__main__":
    main()
