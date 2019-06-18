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
	parser.add_argument('--header', help="Header to attach", nargs=1, required=True, type=str)
	args = parser.parse_args()

	if args.Output[0] == "NA":
		args.Output = os.path.dirname(args.Input[0])

	samplename = os.path.basename(args.Input[0]).split(".")[0]

	with open("~/liu-lab-rotation/jobs/" + sampname + "_split.script", 'w+') as script:
		script.write("#!/bin/bash")
		script.write("#PBS -k o")
		script.write("#PBS -l nodes=1:ppn=1,mem=1024mb,walltime=1:00:00")
		script.write("#PBS -M jonhuang@iu.ed")
		script.write("#PBS -m ab")
		script.write("#PBS -N " + sampname + "_headandsort")
		script.write("#PBS -j o")
		script.write("echo -e \"" + args.header[0] + "\n$(cat " + args.Input[0] +")\" > " + args.Input[0])
		script.write("samtools sort -o " + args.Output[0] + "/" + samplename + ".bam " + args.Input[0])
		script.write("samtools index " + args.Output[0] + "/" + samplename + ".bam")
	call("qsub ~/liu-lab-rotation/jobs/" + sampename + "_split.script", shell=True)
