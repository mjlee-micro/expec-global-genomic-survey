import pandas as pd
import os

vfdb_map = pd.read_csv("vfdb_annotations.tsv", 
                      sep="\t", 
                      header=None, 
                      names=["vfdb_id", "gene_name"])

input_dir = "separated_results"
for sample_dir in os.listdir(input_dir):
    tsv_path = os.path.join(input_dir, sample_dir, f"{sample_dir}.results.tsv")
    annotated_path = os.path.join(input_dir, sample_dir, f"{sample_dir}.annotated.tsv")
    
    if os.path.exists(tsv_path):
        df = pd.read_csv(tsv_path, sep="\t", header=None)
        
        df[1] = df[1].str.replace(r"\(.*", "", regex=True)
        

        df_annotated = df.merge(vfdb_map, 
                              left_on=1, 
                              right_on="vfdb_id", 
                              how="left")
        
    
        df_annotated.to_csv(annotated_path, 
                          sep="\t", 
                          index=False, 
                          header=False)
        
        print(f"done: {annotated_path}")