#! /bin/python3.9.5

import sys
import numpy as np

####----Compatibility----####
#compatible with RSeQC v4.0.0
#must include 7 input files in correct order
#sample input: python summarygen.py {SAMPLENAME}.Aligned.sortedByCoord.out.summary.txt {SAMPLENAME}_junction_annotation_summary_more.txt rseqc_bam_stat_report.txt {SAMPLENAME}.STAR.Log.final.out {SAMPLENAME}_infer_experiment.txt {SAMPLENAME}_inner_distance.txt {SAMPLENAME}_read_distribution.txt
#tin.py                 -- {SAMPLENAME}.Aligned.sortedByCoord.out.summary.txt
#junction_annotation.py -- {SAMPLENAME}_junction_annotation_summary_more.txt
#bam_stat.py            -- rseqc_bam_stat_report.txt (sample specific)
#STAR_log_final         -- {SAMPLENAME}.STAR.Log.final.out (from STAR mapping)
#infer_experiment.py    -- {SAMPLENAME}_infer_experiment.txt
#inner_distance.py      -- {SAMPLENAME}_inner_distance.txt
#read_distribution.py   -- {SAMPLENAME}_read_distribution.txt


####----Input----####
tin=open(sys.argv[1], 'r')
juncanno=open(sys.argv[2], 'r')
bamstat=open(sys.argv[3], 'r')
logfin=open(sys.argv[4], 'r')
inferexp=open(sys.argv[5], 'r')
innerdist=open(sys.argv[6], 'r')
readdist=open(sys.argv[7], 'r')
outfile=open("summary_row_out.tsv", 'w')
outfile2=open("summary_col_out.tsv", 'w')


####----TIN file----####
tinheader=tin.read().splitlines()[0] #extract header
tinheader=tinheader.split('\t') #split by tab delim
TINmean=tinheader[1]
TINmed=tinheader[2]
TINsd=tinheader[3]
mainheader=np.array(['Sample',TINmean,TINmed,TINsd])

tin.seek(0)
tinstat=tin.read().splitlines()[1]
tinstat2=tinstat.split('\t')
sampname=tinstat2[0].split('.')[0]
TINmeannum=tinstat2[1]
TINmednum=tinstat2[2]
TINsdnum=tinstat2[3]
mainstats=np.array([sampname,TINmeannum,TINmednum,TINsdnum])



####----junction annotation----####
for line in juncanno.read().splitlines()[5:]:
	if ':' in line:
		head=line.replace(' ','_').split('\t')[0].split(':')[0]
		val=line.split('\t')[-1]
		mainheader=np.append(mainheader,[head])
		mainstats=np.append(mainstats,[val])


####----BAM stat report----####
for line in bamstat.read().splitlines()[5:]:
	if ':' in line:
		head=line.replace(' ','_').split(':')[0]
		if '<' in head:
			head='mapq_non_unique_reads'
		if '>=' in head:
			head='mapq_unique_reads'
		val=line.replace(' ','').split(':')[-1]
		mainheader=np.append(mainheader,[head])
		mainstats=np.append(mainstats,[val])
	elif 'Non primary hits' in line:
		head='_'.join(line.split(' ')[0:3])
		val=line.split(' ')[-1]
		mainheader=np.append(mainheader,[head])
		mainstats=np.append(mainstats,[val])

# adjust for special characters
mainheader=[s.replace("'+'","pos") for s in mainheader] #positive
mainheader=[s.replace("'-'","neg") for s in mainheader] #negative



####----STAR log final out report----####
for line in logfin.read().splitlines()[5:] :
	if '|' in line:
		head=line.lstrip().replace(' ','_').split('|')[0]
		if '%' in head:
			head=head.replace('%','_fraction_')
		val=line.replace('\t','').split('|')[-1]
		mainheader=np.append(mainheader,[head])
		mainstats=np.append(mainstats,[val])


####----infer experiment----####
failed=inferexp.read().splitlines()[3]
failh=failed.replace(' ','_').split(':')[0]
failv=failed.replace(' ','').split(':')[-1]
inferexp.seek(0)
forw=inferexp.read().splitlines()[4]
frowh='_'.join(forw.split(' ')[0:4])+'_stranded_forward'
frowv=forw.replace(' ','').split(':')[-1]
inferexp.seek(0)
rev=inferexp.read().splitlines()[5]
revh='_'.join(rev.split(' ')[0:4])+'_stranded_reverse'
revv=rev.replace(' ','').split(':')[-1]
mainheader=np.append(mainheader,[failh,frowh,revh])
mainstats=np.append(mainstats,[failv,frowv,revv])


####----inner distance----####
indis=innerdist.read().splitlines()[1]
indis=indis.split('\t')
indismean=indis[1]
indismed=indis[2]
indissd=indis[3]
mainheader=np.append(mainheader,["inner_distance_mean","inner_distance_median","inner_distance_sd"])
mainstats=np.append(mainstats,[indismean,indismed,indissd])


####----read distribution----####
for line in readdist.read().splitlines()[5:14]:
	headtot=line.split()[0]+'_total_bases'
	valtot=line.split()[1]
	headtag=line.split()[0]+'_tags/Kb'
	valtag=line.split()[3]
	mainheader=np.append(mainheader,[headtot,headtag])
	mainstats=np.append(mainstats,[valtot,valtag])


####----remove/replace certain special characters----####
mainheader=[s.replace("'","_") for s in mainheader] #safe
mainheader=[s.replace("(","_") for s in mainheader] #safe
mainheader=[s.replace(")","") for s in mainheader]  #safe
mainheader=[s.replace("/","_") for s in mainheader] #safe
mainheader=[s.replace(":","_") for s in mainheader] #safe
mainheader=[s.replace("\"","_") for s in mainheader] #safe
mainheader=[s.replace("-","_") for s in mainheader] #safe
mainheader=[s.replace(",","_") for s in mainheader] #safe

## checks for no values and zeros and percentages turned to fractions
for i,j in enumerate(mainstats):
	if len(j) == 0:
		mainstats[i]='NA'
	if j == '0':
		mainstats[i]='NA'
	if '%' in j:
		x=float(mainstats[i].replace('%',''))
		mainstats[i]=x/100

## checks for missing items and zeros, removes leading and trailing '_' and capitalize first letter
for i,j in enumerate(mainheader):
	if '_' in j:
		mainheader[i]=mainheader[i].strip('_')
	mainheader[i]=mainheader[i].capitalize()
	if len(j) == 0:
		mainheader[i]='NA'
	if j == '0':
		mainheader[i]='NA'


####----Output----####
## Write numpy array to tab delimited file
#as rows
summarray=np.vstack((mainheader,mainstats))
np.savetxt(outfile, summarray, fmt='%s', delimiter='\t')
#as columns
summarray2=np.column_stack((mainheader,mainstats))
np.savetxt(outfile2, summarray2, fmt='%s', delimiter='\t')
	
tin.close()
juncanno.close()
bamstat.close()
logfin.close()
inferexp.close()
innerdist.close()
readdist.close()

