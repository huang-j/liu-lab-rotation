#!/bin/bash

# Parses through 10x bam file, finds barcode headers and writes them to a sam file.

usage() {
    echo "Usage: $0 [-b <string>] [-o <string>]"
    echo "		-b bam file"
    echo "		-o output directory"
    exit 1;
}
while getopts ":b:o:" x; do
    case "${x}" in
        b)
            b=${OPTARG}
            ;;
        o)
            o=${OPTARG}
            ;;
    esac
done
if [ -z "${b}" ]; then
    usage
fi
if [ -z "${o}" ]; then
    usage
fi

echo "making header sam file"
samtools view -H $b > ${b%.bam}_header.sam

## awk '{if(/^@/) {print $0} else {if($17 ~ /XI/) split($17,barcodes,":"); else if($16 ~ /XI/) split($16,barcodes,":"); if(barcodes[3] >=2) print }}
# samtools view $b | awk -v dir="$o" '{ if($17 ~ /CB/) split($17,barcode,":"); else if($19 ~ /CB/) split($19, barcodes,":"); if(barcodes[3] != "") print dir  }'

echo "writing to bam files"
samtools view $b | awk -v dir="$o" '{ if($17 ~ /CB/) split($17,barcode,":"); else if($19 ~ /CB/) split($19, barcodes,":"); if(barcodes[3] != "") print >> dir"/"barcodes[3]".sam"; else print >> dir"/test_leftovers.sam"  }'

# echo "submitting reheader jobs"
# find $o -type f | grep 'sam$' > files.list
# for f in  $(find $o -type f | grep 'sam$'); do
# 	echo $f
# 	python ~/liu-lab-rotation/scripts/attachHeaderSort.py -I $f -O $o --header ${b%.bam}_header.sam
# done
