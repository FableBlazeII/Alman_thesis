#!/usr/bin/env python

import sys, time, os, array, Pyro4, cPickle
sys.path.append(os.path.abspath('./Baaslahendus/'))
import MotSum_worker
from bitarray import bitarray



class Manager(object):
	maxActiveWorks=1 #Max number of works that can be active
	
	
	activeWorks=0 #Counter of how many works are currently active (goes up and down as works start and finish)
	worksList={} #Dictionary of all the works corrently tracked by the manager (cotains work parameters)
	workQueue=[] #List of work id's waiting to be started
	nextWorkID=0 #ID that is given to next submitted work (goes up every time work is submitted, resets to 0 if 1000 reached)

	def __init__(self):
		PepCount=10000
		SUMMARY='./Testandmed/inputSummary.txt'
		emptyVec=bitarray(PepCount)
		emptyVec.setall(False)
		aminoPosMap={'A':0,'C':1,'D':2,'E':3,'F':4,'G':5,'H':6,'I':7,'K':8,'L':9,'M':10,'N':11,'P':12,'Q':13,'R':14,'S':15,'T':16,'V':17,'W':18,'Y':19}

		vecList=[]
		BScounts=[]
		BSlocations=[]
		
		try:
			with open(SUMMARY+'.pkl', 'rb') as pkl_file:
				vecList=cPickle.load(pkl_file)
				print "Loaded vecList from pickle:"
				print SUMMARY+'.pkl'
				sys.stdout.flush()
			with open(SUMMARY) as BS:
				lines = BS.readlines(131072)
				while lines:
					for line in lines:
						counts=line.rstrip('\n').split('\t')[1:]
						#Fill BScounts and BSlocations
						nonZeroCounts=array.array('i')
						nonZeroLocations=array.array('H')
						for i in range(len(counts)):
							if counts[i]!='0':
								nonZeroCounts.append(int(counts[i]))
								nonZeroLocations.append(i)
						BScounts.append(nonZeroCounts)
						BSlocations.append(nonZeroLocations)

					lines=BS.readlines(131072)
			self.vecList=tuple( vecList )
			self.BScounts=tuple( BScounts )
			self.BSlocations=tuple( BSlocations )
			
		except IOError, UnpicklingError:
			print "Can't load vecList from pickle. Building from summary."
			sys.stdout.flush()
			
			#Generate initial vecList
			for i in range(20):
				vecList.append([])
				for j in range(12):
					vecList[i].append(emptyVec.copy())

			with open(SUMMARY) as BS:
				lineNumber=0
				lines = BS.readlines(131072)
				while lines:
					for line in lines:
						line=line.rstrip('\n').split('\t')
						peptide, counts=line[0], line[1:]
						#Fill vecList
						vecList[aminoPosMap[peptide[0]]][0][lineNumber]=True
						vecList[aminoPosMap[peptide[1]]][1][lineNumber]=True
						vecList[aminoPosMap[peptide[2]]][2][lineNumber]=True
						vecList[aminoPosMap[peptide[3]]][3][lineNumber]=True
						vecList[aminoPosMap[peptide[4]]][4][lineNumber]=True
						vecList[aminoPosMap[peptide[5]]][5][lineNumber]=True
						vecList[aminoPosMap[peptide[6]]][6][lineNumber]=True
						vecList[aminoPosMap[peptide[7]]][7][lineNumber]=True
						vecList[aminoPosMap[peptide[8]]][8][lineNumber]=True
						vecList[aminoPosMap[peptide[9]]][9][lineNumber]=True
						vecList[aminoPosMap[peptide[10]]][10][lineNumber]=True
						vecList[aminoPosMap[peptide[11]]][11][lineNumber]=True

						#Fill BScounts and BSlocations
						nonZeroCounts=array.array('i')
						nonZeroLocations=array.array('H')
						for i in range(len(counts)):
							if counts[i]!='0':
								nonZeroCounts.append(int(counts[i]))
								nonZeroLocations.append(i)
						BScounts.append(nonZeroCounts)
						BSlocations.append(nonZeroLocations)

						lineNumber=lineNumber+1
					lines=BS.readlines(131072)
			vecList=tuple(tuple(x) for x in vecList)
			#try:
			#	with open(SUMMARY+'.pkl', 'wb') as pkl_file:
			#		cPickle.dump(vecList, pkl_file, 2)
			#		print "Created vecList pickle:"
			#		print SUMMARY+'.pkl'
			#		sys.stdout.flush()
			#except:
			#	print "Can not create vecList pickle. Continuing..."
			self.vecList=vecList
			self.BScounts=tuple( BScounts )
			self.BSlocations=tuple( BSlocations )

	def submitWork(self, motifList, outdir, noWaitFlag):
		if self.nextWorkID==1000:
			self.nextWorkID=0
		if self.activeWorks < self.maxActiveWorks:
			self.worksList[self.nextWorkID]=['Starting', motifList, outdir, noWaitFlag]
			self.activeWorks=self.activeWorks+1
			forkPid=os.fork()
			if forkPid==0:
				workStartTime=time.time()
				print "started", os.getpid( )
				sys.stdout.flush()
				MotSum_worker.runWork(self.nextWorkID, self.worksList[self.nextWorkID][1], self.worksList[self.nextWorkID][2], self.vecList, self.BScounts, self.BSlocations)
				if noWaitFlag!='False':
					del self.worksList[self.nextWorkID]
				print "finished", os.getpid( ), time.time()-workStartTime
				sys.stdout.flush()
				sys.exit(0)
		else:
			self.worksList[self.nextWorkID]=['Waiting', motifList, outdir, noWaitFlag]
			self.workQueue.append(self.nextWorkID)
		self.nextWorkID = self.nextWorkID + 1
		sys.stdout.flush()
		return self.nextWorkID - 1

	def checkAllWorks(self):
		sys.stdout.flush()
		return self.worksList
	
	def checkWork(self, id):
		sys.stdout.flush()
		return self.worksList[id][0]
	
	def setWorkStarted(self, id):
		self.worksList[id][0]='Started'
		sys.stdout.flush()
	
	def setWorkFinished(self, id):
		self.worksList[id][0]='Finished'
		self.activeWorks=self.activeWorks-1
		if (self.activeWorks < self.maxActiveWorks) and (len(self.workQueue)!=0):
			self.activeWorks=self.activeWorks+1
			id=self.workQueue.pop(0)
			forkPid=os.fork()
			if forkPid==0:
				workStartTime=time.time()
				print "started", os.getpid( )
				MotSum_worker.runWork(id, self.worksList[id][1], self.worksList[id][2], self.vecList, self.BScounts, self.BSlocations)
				if self.worksList[id][3]!='False':
					del self.worksList[self.nextWorkID]
				print "finished", os.getpid( ), time.time()-workStartTime
				sys.stdout.flush()
				sys.exit(0)
		sys.stdout.flush()
	
	def removeFinishedWork(self, id):
		if self.worksList[id][0]=='Finished':
			del self.worksList[id]
		else:
			print "Work is not finished, can not remove"
		sys.stdout.flush()
	
	def removeWork(self, id):
		del self.worksList[id]
		print "Work %s removed" %str(id)
		sys.stdout.flush()
	
	def setMaxActiveWorks(self, maxActiveWorks):
		self.maxActiveWorks=maxActiveWorks
		sys.stdout.flush()

	def getManagerPID(self):
		return os.getpid( )
	
	def shutdownManager(self):
		daemon.shutdown()

	def checkWorkQueue(self):
		return self.workQueue

	def checkActiveWorksNumber(self):
		return self.activeWorks

print "START"
print "PID:", os.getpid( )
startTime=time.time()
print "Init Start"
sys.stdout.flush()
manager=Manager()
print "Init Done. Time taken:"
print time.time()-startTime

daemon=Pyro4.Daemon(port=50555)
uri=daemon.register(manager, "motifCountManager")

print "Ready. Object uri =", uri
sys.stdout.flush()
daemon.requestLoop()
