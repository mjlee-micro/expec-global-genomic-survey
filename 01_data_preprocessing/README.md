Here's a `README` file that explains how to use your script for downloading genome data from NCBI using the provided `GCA` numbers:

Genome Download Script

This script downloads genome data from the NCBI Genomes Database using the `GCA` accession numbers provided in a text file. The genome files will be saved as ZIP archives in the specified output directory.

Prerequisites

To run this script, ensure that you have the following:

1. Python: The script was developed and tested with Python 3.8+. It is highly recommended to use a virtual environment for managing dependencies.

2. Required Libraries:

   `requests` - to make HTTP requests to the NCBI Datasets API.
    `os` - to interact with the file system (no installation needed, part of the Python Standard Library).
   `time` - to introduce delays between requests (no installation needed, part of the Python Standard Library).

Installation

1. Install Python 3.8+: You can download the latest version of Python from [python.org](https://www.python.org/downloads/).

2.Create a Virtual Environment (optional but recommended):
   ```bash
   python -m venv genome_download_env
   source genome_download_env/bin/activate  # For macOS/Linux
   genome_download_env\Scripts\activate     # For Windows
   ```
3. Install Dependencies:
   Run the following command to install the required libraries:

   ```bash
   pip install requests
   ```

Usage

1. Prepare the Input File:

   * Create a text file (`GCA number list.txt`) containing a list of NCBI Genome Assembly Accessions (GCA numbers).
   * Each accession number should be on a new line in the file.

2. Prepare the Output Directory:

   * Specify the output directory where the downloaded ZIP files will be saved.
   * Modify the `output_directory` variable in the script to the desired directory path.

   Example:

   ```python
   output_directory = r"C:\Users\YourUsername\Downloads\GenomeData"
   ```

3. Run the Script:

   * Ensure the script is in the same folder as the `GCA number list.txt` or update the `gca_file_path` variable to the correct location of your file.

   * Run the script by executing it from your terminal or command prompt:

     ```bash
     python genome_download_script.py
     ```

     The script will read each `GCA` number from the text file, download the corresponding genome data in `.zip` format, and save it in the specified output directory.

4. Optional Parameters:

   * The script uses the NCBI Datasets API with the `GENOME_FASTA` annotation type by default. If you want to change the type of annotations, modify the `params` dictionary inside the `download_genome()` function.

   Example:

   ```python
   params = {"include_annotation_type": "GENOME_FASTA"}
   ```

   Available annotation types can be adjusted based on your needs.

## Script Workflow

* The script reads the `GCA` numbers from the `GCA number list.txt` file.
* For each `GCA` number, it sends a request to the NCBI Datasets API to download the genome data.
* The data is saved as a `.zip` file in the specified output directory.
* The script introduces a 1-second delay (`time.sleep(1)`) between requests to avoid overwhelming NCBI servers.

## Troubleshooting

* If you encounter errors while downloading, check the following:

  * Ensure that the `GCA` numbers are correct and formatted properly.
  * Verify that you have a stable internet connection.
  * Check if the NCBI Datasets API is down or experiencing issues.

* If you receive an HTTP error code, the script will output an error message indicating the issue. Refer to the [NCBI Datasets API documentation](https://www.ncbi.nlm.nih.gov/datasets/docs/) for further information.

## License

This script is provided as-is, and users are free to modify and distribute it according to their needs. Use it at your own risk.

---

Let me know if you need any further customization or clarifications!
