#! /bin/python3.9.5


import sys

filelist = open(sys.argv[1], 'r')
samplist = open(sys.argv[2], 'r')


names1=[]
names2=[]
names3=[]
for file in filelist:
	file = file.strip('\n')
	if '_1' in file:
		names1.append(file)
		names3.append(file)
	if '_2' in file:
		names2.append(file)
		names3.append(file)

names4=[]
for file in names3:
	file1 = file.split('_')
	names4.append(file1[0])
names4set = set(names4)

names5=[]
for samp in samplist:
	samp = samp.strip('\n')
	names5.append(samp)
names5set = set(names5)

n4len = len(names4set)
n5len = len(names5set)

missing = list(sorted(names5set-names4set))
added = list(sorted(names4set-names5set)) 

#print('files in fastq_1 list: '+str(len(names1)))
#print('files in fastq_2 list: '+str(len(names2)))
print('Individual sample list length: '+str(n4len))
print('Individual sample list length: '+str(n5len))
print('Missing: ', missing, str(len(missing)))
print('Added: ', added, str(len(added)))


filelist.close()
samplist.close()