VCF_DIR=files/vcf/files_to_read
SCRIPT_PATH=genomicVariations_vcf.py
OUTPUTS_DIR=outputs_cmds

for chr in $(seq 1 22) X
do
    nohup python3 $SCRIPT_PATH $VCF_DIR/*_chr${chr}.vcf.gz &>> $OUTPUTS_DIR/$chr &
done