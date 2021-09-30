#! /bin/python2.7.9

import sys
import csv
import argparse

parser=argparse.ArgumentParser(description='Compare starting sample list with global summary table output to ensure number of samples and sample names match.')

parser.add_argument('-s','--start', type=argparse.FileType('r'), required=True, metavar='', help='path to starting .lst file')
parser.add_argument('-e','--end', type=argparse.FileType('r'), required=True, metavar='', help='path to global_summary.tsv file')

args=parser.parse_args()

#open files
starlst=args.start
gsummfil=args.end

#read as tab delim
starl=csv.reader(starlst, delimiter='\t')
gsumm=csv.reader(gsummfil, delimiter='\t')

#make list of sample names from each file
slist=[i[0] for i in starl]
glist=[i[0] for i in gsumm]

#remove 'Sample' header from global summary table
glist.remove('Sample')

#store length of sample list
slistlen=len(slist)
glistlen=len(glist)

#compare list lengths and missing values
if slistlen != glistlen:
	print "FAIL\nLength of starting sample list and samples in global summary table does not match."
	print "Length of starting sample list: ", slistlen,"\n","Length of sample list in global summary table: ", glistlen
	sset=set(slist)
	gset=set(glist)
	missing=list(sorted(sset-gset))
	added=list(sorted(gset-sset))
	if len(missing) > 0:
		print "Samples missing from global summary table: ", missing
	if len(added) > 0:
		print "Samples missing from starting sample list: ", added
elif slistlen == glistlen:
	sset=set(slist)
	gset=set(glist)
	missing=list(sorted(sset-gset))
	added=list(sorted(gset-sset))
	if len(missing) > 0 or len(added) > 0:
		print "FAIL\nLength of starting sample list and samples in global summary table match, but some sample names do not match."
		print "Length of starting sample list: ", slistlen,"\n","Length of sample list in global summary table: ", glistlen
	if len(missing) > 0:
		print "Samples missing from global summary table: ", missing
	if len(added) > 0:
		print "Samples missing from starting sample list: ", added
	else:
		print "PASS\nSample names and length of starting sample list and samples in global summary table match."
		print "Length of starting sample list: ", slistlen,"\n","Length of sample list in global summary table: ", glistlen

