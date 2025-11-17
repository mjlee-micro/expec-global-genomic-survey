conda create -n ppanggolin python=3.9
conda activate ppanggolin

conda install -c bioconda ppanggolin

ppanggolin annotate \
  --gff gff_list.txt \
  --fasta fasta_list.txt \
  --cpu 16 \
  --output annotate_results

ppanggolin cluster \
  --pangenome annotate_results/pangenome.h5 \
  --cpu 16 \
  --output phylo_out