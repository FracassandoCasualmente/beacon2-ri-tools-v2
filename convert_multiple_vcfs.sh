VCF_DIR=files/vcf/files_to_read
SCRIPT_PATH=genomicVariations_vcf.py
OUTPUTS_DIR=outputs_cmds

# Run it with `nohup bash convert_multiple_vcfs.sh &`

function main_func {
	pids=""

	# launch processes
	for chr in $(seq 1 22) X
	do
		nohup python3 $SCRIPT_PATH $VCF_DIR/*_chr${chr}.vcf.gz &>> $OUTPUTS_DIR/$chr &
		pids="$pids $!"
	done

	# wait for processes to finish
	c=0
	for p in $pids
	do
		c=$(expr $c + 1)
		echo "waiting $c process, with PID $p"
		wait $p
	done
}

# run it
main_func
