# python file to run each separate bam file through it's own job for sorting and what not
import sys
import os
from subprocess import call
import re
import argparse

if __name__ == "__main__":
	## set up argparser
	parser = argparse.ArgumentParser(description='writes job files for each bam and runs them')
	parser.add_argument('-I', '--Input', help="Inputs. Depending on which step is selected can have different one.", nargs=1, required=False, type=str)
	parser.add_argument('-O', '--Output', help="Output file", nargs=1, required=True, type=str, default="NA")
	parser.add_argument('--header', help="Header file", nargs=1, required=True, type=str)
	args = parser.parse_args()

	if args.Output[0] == "NA":
		args.Output = os.path.dirname(args.Input[0])

	samplename = os.path.basename(args.Input[0]).split(".")[0]

	with open("~/liu-lab-rotation/jobs/" + samplename + "_split.script", 'w+') as script:
		script.write("#!/bin/bash\n")
		script.write("#PBS -k o\n")
		script.write("#PBS -l nodes=1:ppn=1,mem=1024mb,walltime=1:00:00\n")
		script.write("#PBS -M jonhuang@iu.edu\n")
		script.write("#PBS -m ab\n")
		script.write("#PBS -N " + samplename + "_headandsort\n")
		script.write("#PBS -j o\n")
		## script.write("echo -e \"" + args.header[0] + "\n$(cat " + args.Input[0] +")\" > " + args.Input[0])
		script.write("module load samtools\n")
		script.write("samtools reheader " + args.header[0] + " " + args.Input[0] + " | samtools sort -o " + args.Output[0] + "/" + samplename + " | samtools index \n")
		## script.write("samtools index " + args.Output[0] + "/" + samplename + ".bam")
	call("qsub ~/liu-lab-rotation/jobs/" + samplename + "_split.script", shell=True)
	call("rm ~/liu-lab-rotation/jobs/" + samplename + "_split.script", shell=True)
