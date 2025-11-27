# Genomic and Geographic Analysis Scripts

This repository contains several Python scripts that help perform genomic and geographic analyses on Extraintestinal pathogenic Escherichia coli (ExPEC). These scripts support tasks like pangenome analysis, calculating geographic distances, Mantel tests, and more.

## Prerequisites

Before running the scripts, make sure that you have the following Python environment and libraries installed:

### Python Version

* Python 3.8 or higher.

### Required Libraries

You will need several Python libraries to run the scripts. The necessary libraries are:

1. **pandas**: Data manipulation and analysis.
2. **numpy**: Numerical computations.
3. **matplotlib**: Plotting and visualization.
4. **seaborn**: Statistical data visualization.
5. **scipy**: Statistical computations (for Mantel tests).
6. **skbio**: Bioinformatics tools, including distance matrices and phylogenetic tree analysis.

You can install the required libraries via `pip`:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-bio
```

Alternatively, if you're using **conda**, you can create a new environment and install the dependencies using:

```bash
conda create -n ecoli_analysis python=3.9
conda activate ecoli_analysis
conda install pandas numpy matplotlib seaborn scipy scikit-bio
```

Additionally, for phylogenetic analysis, you will need **IQ-TREE**. Install it with:

```bash
conda install -c bioconda iqtree -y
```

## Scripts Overview

### 1. **`01_ppanggolin_cluster.py`**

This script uses the **PPAngolin** tool for pangenome analysis. It annotates and clusters genomic data into a pangenome. You need to install the **PPAngolin** tool using `conda`.

**Commands**:

```bash
conda install -c bioconda ppanggolin
ppanggolin annotate --gff gff_list.txt --fasta fasta_list.txt --cpu 16 --output annotate_results
ppanggolin cluster --pangenome annotate_results/pangenome.h5 --cpu 16 --output phylo_out
```

### 2. **`02_IQ-tree.py`**

This script uses **IQ-TREE** to perform phylogenetic tree construction on the aligned genomic sequences. It applies model selection and bootstrapping to refine the phylogenetic tree.

**Commands**:

```bash
conda install -c bioconda iqtree -y
iqtree2 -s phylo_out/core_genome_alignment.fasta -m MFP -B 1000 --alrt 1000 -T AUTO --prefix refined_tree
```

**Key Output**:

* `refined_tree.treefile`: The refined phylogenetic tree based on the core genome alignment.

### 3. **`03_geodist.py`**

This script calculates the geographic distances between continents using predefined centroid coordinates for each continent. It produces a matrix of pairwise geographic distances.

**Key Output**:

* `geo_dist.csv`: A CSV file containing the geographic distances between samples.

### 4. **`04_Mantel_r.py`**

This script performs a Mantel test to correlate genomic distances with geographic distances using Pearson's correlation coefficient. It uses distance matrices from `gen_dist.csv` and `geo_dist.csv`.

**Key Output**:

* The script prints the **Pearson R²** and **p-value** for the Mantel test.

### 5. **`05_gen_dist.py`**

This script calculates genomic distances between ExPEC strains using phylogenetic data. It merges the results with metadata for downstream analysis.

**Key Output**:

* `gen_dist.csv`: A CSV file containing the genomic distances between samples.

### 6. **`06_ρ_value_of_Mantel_test.py`**

This script calculates the Mantel test’s **Pearson R²** and **p-values** between genomic and geographic distances, as prepared in previous steps.

### 7. **`07_genomic_and_geographic_distances.py`**

This script generates the genomic and geographic distance matrices. It combines these matrices for further analysis, ensuring all samples with complete data are considered.

### 8. **`08_sharing_prop.py`**

This script calculates the **strain sharing proportion (sharing_prop)** between different serotypes in each continent, based on the sequence types (STs). It outputs the proportion of shared strains.

**Key Output**:

* `Supplementary Table 1_with_sharing_prop.csv`: This file contains metadata, including the calculated sharing proportions for each continent.

### 9. **Visualization**

In the final step, some scripts generate scatter plots of **geographic effect vs. strain sharing proportion** (e.g., `geography_vs_sharing_labeled_safe.png`) for visualization.

---

## How to Use the Scripts

### Step 1: Prepare Your Data

* You will need the metadata file (`Supplementary Table 1.xlsx`) containing information such as **sample**, **serotype**, **continent**, and **sequence type (st)**.
* You must also have **phylogenetic tree data** (e.g., `phylotree.treefile`) for genomic distance calculations.
* Create a list of **GCA numbers** for downloading genome data if necessary.

### Step 2: Run Each Script

* Make sure to execute the scripts in sequence. Each script builds on the results of the previous one.
* For example:

  1. Run **`08_sharing_prop.py`** to calculate strain sharing proportions.
  2. Run **`03_geodist.py`** and **`05_gen_dist.py`** to compute geographic and genomic distances.
  3. Then, use **`04_Mantel_r.py`** and **`06_ρ_value_of_Mantel_test.py`** to perform statistical analyses.
  4. Visualize the results using **`07_genomic_and_geographic_distances.py`**.
  5. Perform phylogenetic analysis using **`02_IQ-tree.py`** to generate a refined phylogenetic tree.

### Step 3: Analyze the Results

* The results are saved as CSV files (`geo_dist.csv`, `gen_dist.csv`, `mantel_result_by_Otype.csv`), which can be further analyzed or visualized.
* Scatter plots and Mantel test results provide insights into the relationship between genomic and geographic distances.

## Output Files

* `geo_dist.csv`: Geographic distance matrix.
* `gen_dist.csv`: Genomic distance matrix.
* `mantel_result_by_Otype.csv`: Mantel test results for each serotype (O-type).
* `Supplementary Table 1_with_sharing_prop.csv`: Metadata with calculated strain sharing proportions for each continent.
* `refined_tree.treefile`: Refined phylogenetic tree generated using **IQ-TREE**.
