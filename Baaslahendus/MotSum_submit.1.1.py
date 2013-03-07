#!/usr/bin/env python

import sys, os, optparse, time, Pyro4

usage = "usage: %prog [options]"
version = "%prog 1.1"
description = "Submits the motif counting job and then waits for this job to be finished."


#Handle the commands line options
parser = optparse.OptionParser(usage=usage, version=version, description=description)
parser.add_option("-o", "--output", dest="output",
             help="Output table path and name (file will be overwriten)")
parser.add_option("-m", "--motifList", dest="motifList",
             help="File containing new-line separated motifs to search for")
parser.add_option("--addHeader", dest="addHeader", action="store_true",
             help="Use this flag to add a headerline to output", default="False")
parser.add_option("--noWait", dest="noWait", action="store_true",
             help="Use this flag to exit after job is submitted", default="False")

(options, args) = parser.parse_args()

def submitWork(motifList, output, noWaitFlag, addHeaderFlag):
	return motifCountManager.submitWork(motifList, output, noWaitFlag, addHeaderFlag)

def waitUntillFinished(id):
	while True:
		time.sleep(60)
		if motifCountManager.checkWork(id)=='Finished':
			break
	motifCountManager.removeFinishedWork(id)


if options.output and options.motifList:
	output=os.path.abspath(options.output)
	motifList=os.path.abspath(options.motifList)
	motifCountManager=Pyro4.Proxy('PYRO:motifCountManager@localhost:50555')
	print "Works in list:",
	print len(motifCountManager.checkAllWorks())
	sys.stdout.flush()
	id=submitWork(motifList, output, options.noWait, options.addHeader)
	print "Work submitted."
	sys.stdout.flush()
	sTime=time.time()
	if options.noWait=='False':
		waitUntillFinished(id)
		print "Done! Time taken:", time.time()-sTime
else:
	print "Output and motifList required"