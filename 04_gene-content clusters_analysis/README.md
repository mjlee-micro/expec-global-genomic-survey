Here’s a `README` file for the **04_gene-content_clusters_analysis** folder that explains the purpose and usage of the provided **gene-content cluster analysis** script.

---

# 04 Gene-Content Clusters Analysis

This folder contains a Python script used for analyzing gene-content clusters in microbial genomes, specifically focusing on virulence and resistance factors. The script performs clustering on gene data and generates various outputs to facilitate the analysis of gene patterns across different serotypes. It uses **K-Means clustering** to group genes into functional modules, then explores their distribution across different O-serotypes.

## Prerequisites

Before running the script, ensure that you have the following software and libraries installed:

### Python Version

* Python 3.8 or higher.

### Required Libraries

You will need the following Python libraries:

* **pandas**: For handling tabular data.
* **sklearn**: For clustering and machine learning functionalities.

Install these libraries via `pip`:

```bash
pip install pandas scikit-learn
```

Alternatively, you can use **conda** to set up the environment and install the required packages:

```bash
conda create -n gene_cluster_analysis python=3.9
conda activate gene_cluster_analysis
conda install pandas scikit-learn
```

## Script Overview

### **`gene-content_cluster_analysis.py`**

This script performs the following tasks:

1. **Data Preprocessing**:

   * Reads virulence, resistance, and serotype data from input files.
   * Preprocesses the data (converts to numeric, fills missing values with zero).

2. **K-Means Clustering**:

   * Clusters the virulence and resistance genes into 5 modules using **K-Means**.
   * Assigns labels to each sample based on the clustering result.

3. **Pivot Table Creation**:

   * Creates pivot tables to show the distribution of virulence and resistance modules across different O-serotypes.

4. **Top Genes Extraction**:

   * For each cluster, identifies the top 5 representative genes based on frequency within the cluster.

5. **Output Generation**:

   * Saves the results to several CSV files, including:

     * **Cluster Labels**: Gene content clustering results.
     * **Serotype vs. Virulence**: Shows virulence module distribution by O-serotype.
     * **Serotype vs. Resistance**: Shows resistance module distribution by O-serotype.
     * **Top Virulence Genes**: Lists top 5 representative virulence genes for each module.
     * **Top Resistance Genes**: Lists top 5 representative resistance genes for each module.

### Input Files

The script expects three input files:

* **Virulence Data** (`VFDB_annoted.txt`): Contains gene presence/absence or frequency data for virulence factors.
* **Resistance Data** (`CARD_annoted.txt`): Contains gene presence/absence or frequency data for resistance factors.
* **Serotype Data** (`serotype_annoted.txt`): Contains serotype information for each sample.

### Output Files

The script generates the following output files:

1. **`cluaster_label.csv`**: Cluster labels for each sample (virulence and resistance).
2. **`serotype_vs_virulence.csv`**: Pivot table showing the distribution of virulence modules by O-serotype.
3. **`serotype_vs_resistance.csv`**: Pivot table showing the distribution of resistance modules by O-serotype.
4. **`virulence_represent_genes.csv`**: Top 5 representative virulence genes for each cluster.
5. **`resistance_represent_genes.csv`**: Top 5 representative resistance genes for each cluster.

### How to Use the Script

1. **Prepare Input Files**:

   * Ensure you have the required input files (`VFDB_annoted.txt`, `CARD_annoted.txt`, and `serotype_annoted.txt`) containing gene data and serotype information.
   * The files should have the sample IDs as the index and the gene names or presence/absence as the values.

2. **Run the Script**:

   * Place the input files in the directory where the script is located, or modify the file paths in the script accordingly.
   * Run the script using Python:

     ```bash
     python gene-content_cluster_analysis.py
     ```

3. **Analyze the Results**:

   * After running the script, check the output CSV files in the specified output directory (`output_dir`).
   * The pivot tables and gene lists can be used for further analysis or visualization of the distribution of gene modules across different O-serotypes.
