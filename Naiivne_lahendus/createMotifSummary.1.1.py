#!/usr/bin/env python

import optparse, os, multiprocessing, time, re

usage = "usage: %prog [options]"
version = "%prog 1.1"
description = "Finds the frequency of all given motifs in the input table. Can spawn multiple processes."


#Handle the commands line options
parser = optparse.OptionParser(usage=usage, version=version, description=description)
parser.add_option("-i", "--input", dest="input",
             help="Input table path and name (expects big summary format)")
parser.add_option("-o", "--output", dest="output",
             help="Output table path and name (file will be overwriten)")
parser.add_option("-m", "--motifList", dest="motifList",
             help="File containing new-line separated motifs to search for")
parser.add_option("--processes", dest="processes", default="10",
             help="Number of sub-processes to use (default 10)")

(options, args) = parser.parse_args()

# Splits the file into regions for sub-processes. Makes sure that region doesnt start in the middle of line
def findRegions():
	regions=[]
	regionSize=os.path.getsize(options.input)/int(options.processes)
	with open(options.input) as input:
		# First region
		input.seek(regionSize)
		input.readline()
		regions.append((0,input.tell()))

		if int(options.processes) > 1:
			for i in range(2,int(options.processes)):
				# Remaining regions (except last)
				start=input.tell()
				input.seek(regionSize*i)
				input.readline()
				regions.append((start,input.tell()))
			# Last region (filesize used as region end to ensure that all lines are processed)
			regions.append((input.tell(), os.path.getsize(options.input)))
			
	return regions

# Read and compile motifs in motifsFile
def compileMotifs():
	compiledMotifs=[]
	with open(options.motifList) as motifFile:
		for line in motifFile:
			compiledMotifs.append(re.compile(line.rstrip()))
	return compiledMotifs
	
def getIndexCount():
	indexCount=0
	with open(options.input) as input:
		indexCount = len(input.readline().split())-1
	return indexCount
	
def processRegion(result_queue, region, motifs, indexCount):
	subTotals = []
	indexRange=range(indexCount)
	for i in range(len(motifs)):
		subTotals.append([])
		for j in indexRange:
			subTotals[i].append(0)
	
	
	with open(options.input) as input:
		input.seek(region[0])
		prev_tell=input.tell()
		while True:
			lines=input.readlines(131072)
			if input.tell()>=region[1]:
				input.seek(prev_tell)
				while input.tell() != region[1]:
					line=input.readline()
					peptide=line[:line.find('\t')]
					motifNum = 0
					split=False
					for motif in motifs:
						if motif.search(peptide):
							if not split:
								line=map(int, line.rstrip().split('\t')[1:])
								split=True
							for i in indexRange:
								subTotals[motifNum][i] = subTotals[motifNum][i]+ int(line[i])
						motifNum = motifNum+1
				break
			else:
				prev_tell=input.tell()
				for line in lines:
					peptide=line[:line.find('\t')]
					motifNum = 0
					split=False
					for motif in motifs:
						if motif.search(peptide):
							if not split:
								line=map(int, line.rstrip().split('\t')[1:])
								split=True
							for i in indexRange:
								subTotals[motifNum][i] = subTotals[motifNum][i]+ int(line[i])
						motifNum = motifNum+1
	result_queue.put(subTotals)
	print "Region %s to %s done" %(region[0],region[1])
	return

startTime=time.time()

# Queue to store results from all sub-processes
result_queue = multiprocessing.Queue()


if __name__ == '__main__':
	regions = findRegions()
	motifs = compileMotifs()
	indexCount = getIndexCount()
	jobs = []
	
	outCounts = []
	for i in range(len(motifs)):
		outCounts.append([motifs[i].pattern])
		for j in range(indexCount):
			outCounts[i].append(0)

	print "Regions: ",
	print regions
	for region in regions:
		p = multiprocessing.Process(target=processRegion, args=(result_queue, region, motifs, indexCount))
		jobs.append(p)
		p.start()
	
	print "Processes started"
		
	for i in range(int(options.processes)):
		procesResult=result_queue.get()
		for i in range(len(procesResult)):
			for j in range(len(procesResult[i])):
				outCounts[i][j+1]=outCounts[i][j+1]+procesResult[i][j]
	
	print "Queue read"
	
	# Join jobs (awoid zombie invasion)
	for job in jobs:
		job.join()
	
	for outCount in outCounts:
		for i in range(1,len(outCount)):
			outCount[i]=str(outCount[i])

	with open(options.output, 'w') as outTable:
		for outCount in outCounts:
			outTable.write('\t'.join(outCount)+'\n')
			

print 'Time taken: %s' % (time.time()-startTime)