Here is a `README` file for the **03_gene_annotation** folder that explains the purpose and usage of the scripts and pipelines within the folder.

---

# 03 Gene Annotation Pipeline

This folder contains the pipelines and scripts used for the annotation of genomic data, focusing on the analysis of genomic sequences using tools like **Prokka**, **Abricate**, and **VFDB** (Virulence Factor Database). These tools help in annotating genes, identifying virulence factors, and performing resistance gene analyses. The scripts are designed for E. coli and ExPEC genomic studies, allowing for automated annotation and analysis of large datasets.

## Prerequisites

Before running the scripts, ensure that you have the following software and libraries installed:

### 1. **Prokka** (for Prokaryotic Genome Annotation)

Prokka is used to annotate prokaryotic genomes by identifying genes, coding sequences (CDS), rRNA, tRNA, and other genomic features.

**Installation**:

```bash
conda create -n prokka -c conda-forge -c bioconda -c defaults prokka
conda activate prokka
```

### 2. **Abricate** (for Antimicrobial Resistance and Virulence Factor Annotation)

Abricate is used for genome-wide antimicrobial resistance and virulence factor detection using various databases like **CARD**, **VFDB**, etc.

**Installation**:

```bash
conda create -n abricate_new -c conda-forge -c bioconda perl=5.26.2 abricate=1.0.1
conda activate abricate_new
```

### 3. **Diamond** (for Fast Sequence Alignment)

Diamond is used for fast sequence alignments, specifically for identifying virulence factors from VFDB.

**Installation**:

```bash
conda create -n diamond_env
conda install diamond
```

### 4. **Required Python Libraries**

You will need the following Python libraries:

* `pandas`: For handling tabular data.
* `os`: For interacting with the file system.

Install these via `pip`:

```bash
pip install pandas
```

## Pipeline Overview

This folder contains several scripts that automate different parts of the gene annotation process. Below is an overview of the files:

### 1. **`card_analysis_pipeline_and_code.txt`**

This file provides instructions for using **Abricate** with the **CARD** database to identify antimicrobial resistance genes in genomic sequences.

**Steps**:

1. Install **Abricate**.
2. Set up the CARD database.
3. Run **Abricate** on your input files:

   ```bash
   abricate --db card *.fasta > card_results.tsv
   ```

### 2. **`prokka_annotation_pipeline_and_code.txt`**

This file provides instructions for using **Prokka** to annotate prokaryotic genomes.

**Steps**:

1. Install **Prokka** and set up the database.
2. Annotate genomes:

   ```bash
   prokka --setupdb
   mkdir -p prokka_analysis/{input,output}
   cd prokka_analysis
   for file in input/*.fasta; do
       base=$(basename "$file" .fasta)
       prokka --outdir output/"$base" --prefix "$base" --cpus 8 "$file"
   done
   ```

### 3. **`vfdb_analysis_pipeline_and_code.txt`**

This file provides instructions on using **Diamond** for aligning genomic sequences to the **VFDB** (Virulence Factor Database) and generating a list of virulence factors.

**Steps**:

1. Download and unzip the VFDB database:

   ```bash
   wget http://www.mgc.ac.cn/VFs/Down/VFDB_setA_pro.fas.gz
   gunzip VFDB_setA_pro.fas.gz
   ```
2. Process the VFDB annotations:

   ```bash
   grep ">" VFDB_setA_pro.fas | perl -nle 'if (/>(VFG\d+)\(.*?\)\s+\((.*?)\)/) { print "$1\t$2" } else { print "$1\tUnknown" }' > vfdb_annotations.tsv
   ```
3. Run **vfdb_annotation.py** to annotate your results:

   ```bash
   python vfdb_annotation.py
   ```

### 4. **`vfdb_annotion.py`**

This Python script takes the output of the **VFDB** annotation (from `vfdb_annotations.tsv`) and merges it with the results from **Abricate** or other genomic annotation tools. It adds gene names to the results and outputs an annotated table for each sample.

**Steps**:

1. The script reads results from separate annotation files.
2. It merges these results with the VFDB annotations.
3. The annotated results are saved as `.annotated.tsv` files for each sample.

Run the script with:

```bash
python vfdb_annotion.py
```

### Workflow Summary

1. **Annotation**:

   * Annotate genomic sequences using **Prokka** or **Abricate** to identify genes, virulence factors, and antimicrobial resistance genes.
2. **Virulence Factor Annotation**:

   * Align sequences to the **VFDB** using **Diamond** and annotate using the `vfdb_annotion.py` script.
3. **Analysis**:

   * Combine results from different annotation tools and databases into comprehensive annotated datasets.

### Output Files

* **Prokka Output**: `prokka_analysis/output/{sample_name}/`
* **Abricate Output**: `card_results.tsv`
* **VFDB Annotation Output**: Annotated files in `separated_results/{sample_name}/{sample_name}.annotated.tsv`

## How to Use the Scripts

### Step 1: Prepare Input Files

Ensure you have FASTA files for your genomes and a working directory structure as described in the pipeline documentation (e.g., `input/` directory for genome sequences).

### Step 2: Run the Pipelines

* For **Prokka** and **Abricate** annotation, follow the instructions in `prokka_annotation_pipeline_and_code.txt` and `card_analysis_pipeline_and_code.txt`.
* For **VFDB** annotation, run `vfdb_annotion.py` to generate annotated results after aligning sequences using **Diamond**.

### Step 3: Analyze the Annotated Results

After running the pipelines, you will get annotated genomic data that can be further analyzed for virulence factors, antimicrobial resistance, and other genomic features.


This `README` should provide all the necessary instructions for using the **03_gene_annotation** pipeline, including setting up the environment, running the scripts, and understanding the outputs. Let me know if you need further adjustments!
