conda install -c bioconda iqtree -y

iqtree2 -s phylo_out/core_genome_alignment.fasta -m MFP -B 1000 --alrt 1000 -T AUTO --prefix refined_tree