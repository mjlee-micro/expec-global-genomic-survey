import requests
import os
import time

gca_file_path = r"C:\Users\Desktop\GCA number list.txt"
with open(gca_file_path, 'r') as gca_file:
    gca_numbers = [line.strip() for line in gca_file if line.strip()]

output_directory = r"your address"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

def download_genome(gca_number):
    try:
        # Using NCBI Datasets API
        base_url = f"https://api.ncbi.nlm.nih.gov/datasets/v2alpha/genome/accession/{gca_number}/download"
        params = {"include_annotation_type": "GENOME_FASTA"}
        
        print(f"Downloading {gca_number}...")
        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            output_path = os.path.join(output_directory, f"{gca_number}.zip")
            with open(output_path, "wb") as f:
                f.write(response.content)
            print(f"Successfully downloaded {gca_number}")
            return True
        else:
            print(f"Failed to download {gca_number}: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error downloading {gca_number}: {e}")
        return False

# Download each genome
for gca_number in gca_numbers:
    download_genome(gca_number)
    time.sleep(1)  # Be nice to NCBI servers