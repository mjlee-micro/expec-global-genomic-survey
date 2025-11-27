Here is the `README` file for the **05_phenotypic_analysis** folder, which explains the purpose and usage of the phenotypic analysis scripts.

---

# 05 Phenotypic Analysis

This folder contains Python scripts used for performing various phenotypic assays on microbial strains, including growth performance, motility assays, and resistance analysis. The scripts analyze bacterial behavior such as growth curves, swarming, swimming, and iron-limitation under different experimental conditions. Additionally, resistance profiling is conducted for assessing genetic resistance across various strains.

## Prerequisites

Before running the scripts, ensure that you have the following software and libraries installed:

### Python Version

* Python 3.8 or higher.

### Required Libraries

You will need the following Python libraries:

* **pandas**: For handling tabular data.
* **matplotlib**: For plotting and visualization.
* **seaborn**: For enhanced data visualization.
* **numpy**: For numerical computations.
* **scipy**: For statistical analysis (ANOVA tests).

Install these libraries via `pip`:

```bash
pip install pandas matplotlib seaborn numpy scipy
```

Alternatively, you can use **conda** to set up the environment and install the required packages:

```bash
conda create -n phenotypic_analysis python=3.9
conda activate phenotypic_analysis
conda install pandas matplotlib seaborn numpy scipy
```

## Script Overview

### 1. **`Growth performance curve.py`**

This script generates bacterial growth curves for different serotypes over time. The data is provided in an Excel file, and the script visualizes the growth (OD600) across different time points for each sample.

**Key Features**:

* Reads growth performance data from an Excel file.
* Plots bacterial growth curves by serotype.
* Includes error bars representing the standard deviation.

**Input**:

* Excel file (`Growth performance.xlsx`) with growth data.

**Output**:

* A plot showing bacterial growth curves by serotype.

### 2. **`Swarming motility assay.py`**

This script analyzes the swarming motility of bacterial strains over time (4 hours, 8 hours, and 24 hours) based on an assay. It performs statistical analysis (ANOVA) to assess significant differences between serotypes.

**Key Features**:

* Reads swarming assay data from an Excel file.
* Performs ANOVA to determine statistical significance.
* Visualizes the swarming diameter at different time points for each serotype.

**Input**:

* Excel file (`Swarming motility assay.xlsx`) containing swarming data.

**Output**:

* A plot showing the mean swarming diameter for each serotype.
* ANOVA test results for each time point.

### 3. **`Swimming motility or Iron-limitation assay.py`**

This script analyzes the swimming motility or iron-limitation assay results. It uses ANOVA to test for significant differences between serotypes in the swimming diameter.

**Key Features**:

* Reads swimming or iron-limitation assay data from an Excel file.
* Performs ANOVA to assess statistical significance between serotypes.
* Visualizes the motility across different serotypes.

**Input**:

* Excel file (`Swimming motility/Iron-limitation assay.xlsx`) containing assay results.

**Output**:

* ANOVA test results for the swimming or iron-limitation assay.
* A plot of swimming diameters for each serotype.

### 4. **`60 strains genetic resistance.py`**

This script processes a genetic resistance matrix and serotype data, producing 0/1 matrices to represent the presence/absence of resistance genes across different serotypes. It calculates proportions of resistance genes within each serogroup.

**Key Features**:

* Reads a resistance gene matrix, serotype annotation, and resistance annotations.
* Generates 0/1 matrices for the presence or absence of resistance genes.
* Calculates the proportion of resistance genes across different serogroups.
* Outputs two CSV files: a 0/1 matrix and a proportion matrix.

**Input**:

* Resistance matrix (`60 strain.txt`).
* Serotype annotation file (`serotype annotion.txt`).
* Resistance annotation file (`resistance annotion.txt`).

**Output**:

* 0/1 matrix of resistance genes per serogroup (`Serogroup_AMRtype_01_matrix.tsv`).
* Proportion matrix of resistance genes per serogroup (`Serogroup_AMRtype_proportion.tsv`).

## How to Use the Scripts

### Step 1: Prepare Input Files

Ensure that the input files are in the correct format:

* **Growth assay**: An Excel file with columns for sample name, serotype, and time points.
* **Motility assays**: Excel files with data on swarming or swimming motility (typically containing measurements across multiple time points for each serotype).
* **Resistance matrix**: A file representing the presence/absence (0/1) of resistance genes across strains.
* **Serotype and resistance annotation files**: Files mapping each sample to its serotype and resistance profile.

### Step 2: Run the Scripts

Run the scripts in your terminal or command prompt by using the following command:

```bash
python Growth performance curve.py
python Swarming motility assay.py
python Swimming motility or Iron-limitation assay.py
python 60 strains genetic resistance.py
```

Ensure that the input files are placed in the directory where the scripts are located or adjust the file paths within the scripts.

### Step 3: Analyze the Results

* **Growth performance**: The growth curves will be displayed as plots for each serotype.
* **Swarming and Swimming motility assays**: Results will include visualizations of the assay outcomes and ANOVA statistical tests.
* **Genetic resistance**: The script will generate matrices and CSV files representing the presence of resistance genes across serogroups and proportions of resistance in each group.
