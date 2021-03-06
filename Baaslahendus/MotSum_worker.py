#!/usr/bin/env python

import sys, operator, array, multiprocessing, traceback, Pyro4

MAX_PROCESSES=10
sampleCount=100

##Salvestab iga motiivi stringina listi
def genMotifsList(motifFile):
	motifList=[]
	with open(motifFile) as motifFile:
		for line in motifFile:
			line=line.rstrip('\n')
			if line:
				motifList.append(line)
	return tuple( motifList )

def calcCounts(motifsList, vecList, aminoPosMap, BScounts, BSlocations, result_queue=None):
	allMotifCounts=[]
	for motif in motifsList:
		#Performs bitvector calculations
		matchingLinesList=[]
		motifCounts=[0]*sampleCount
		motifRange=range(12-len(motif)+1)
		calcList=[[] for x in motifRange]
		i=0
		for char in motif:
			if char=='.':
				i=i+1
				continue
			for j in motifRange:
				calcList[j].append(vecList[aminoPosMap[char]][i+j])
			i=i+1
		motifResultVec=reduce(operator.or_, [reduce(operator.and_, x) for x in calcList])
		#Finds locations of 1 in motifResultVec
		count=motifResultVec.count()
		if count==0:
			allMotifCounts.append(array.array('i', motifCounts))
			continue
		else:
			matchingLinesList.append(motifResultVec.index(True))
			for i in xrange(count-1):
				matchingLinesList.append(motifResultVec.index(True, matchingLinesList[-1]+1))
		for lineNr in matchingLinesList:
			for i in range(len(BSlocations[lineNr])):
				motifCounts[BSlocations[lineNr][i]]=motifCounts[BSlocations[lineNr][i]]+BScounts[lineNr][i]
		allMotifCounts.append(array.array('i', motifCounts))
	if result_queue==None:
		return allMotifCounts
	else:
		result_queue.send(allMotifCounts)

def writeOutput(motifsList, allMotifCounts, OUT_FILE):
	with open(OUT_FILE, 'w') as outFile:
		outFile.write(motifsList[0]+'\t'+'\t'.join(str(x) for x in allMotifCounts[0]))
		i=1
		for motif in motifsList[1:]:
			outFile.write('\n'+motif+'\t'+'\t'.join(str(x) for x in allMotifCounts[i]))
			i=i+1

def runWork(id, motifList, output, vecList, BScounts, BSlocations):
	motifCountManager=Pyro4.Proxy('PYRO:motifCountManager@localhost:50555')
	motifCountManager.setWorkStarted(id)
	try:
		aminoPosMap={'A':0,'C':1,'D':2,'E':3,'F':4,'G':5,'H':6,'I':7,'K':8,'L':9,'M':10,'N':11,'P':12,'Q':13,'R':14,'S':15,'T':16,'V':17,'W':18,'Y':19}
		motifsList=genMotifsList(motifList)
		if len(motifsList)<MAX_PROCESSES:
			allMotifCounts=calcCounts(motifsList, vecList, aminoPosMap, BScounts, BSlocations)
		else:
			allMotifCounts=[]
			jobs = []
			result_queues=[multiprocessing.Pipe(False) for i in range(MAX_PROCESSES)]
			motifs_per_process=len(motifsList)/MAX_PROCESSES
			for i in range(MAX_PROCESSES-1):
				p = multiprocessing.Process(target=calcCounts, args=(motifsList[motifs_per_process*i:motifs_per_process*i+motifs_per_process], vecList, aminoPosMap, BScounts, BSlocations, result_queues[i][1]))
				jobs.append(p)
				p.start()
			p = multiprocessing.Process(target=calcCounts, args=(motifsList[motifs_per_process*(MAX_PROCESSES-1):], vecList, aminoPosMap, BScounts, BSlocations, result_queues[MAX_PROCESSES-1][1]))
			jobs.append(p)
			p.start()
			sys.stdout.flush()
			
			for results in result_queues:
				allMotifCounts=allMotifCounts+results[0].recv()

			for job in jobs:
				job.join()
			
		writeOutput(motifsList, allMotifCounts, output)
	except:
		print "Unexpected error:"
		print "Type:", sys.exc_info()[0]
		print "Value:", sys.exc_info()[1]
		print "Exception:"
		print traceback.format_tb(sys.exc_info()[2])
		sys.exit(1)
	finally:
		motifCountManager.setWorkFinished(id)
