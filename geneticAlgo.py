import random
import numpy as np
from numpy.random import choice
import os
import xml.etree.ElementTree as ET

path = 'sumo-0.27.1\\tools\\2_INT\\2_INT\\'

#########################
# function to right new light cycle in xml file
#########################
def writeTimes(new_time):
	tree = ET.parse(path + 'twoIntersections.net.xml')
	root = tree.getroot()
	i = 0
	j = 0

	for tlLogic in root.findall('tlLogic'):
		for phase in tlLogic.findall('phase'):
			phase.set('duration', str(new_time[j]))
			j += 1
		
	tree.write(path + "twoIntersections.net.xml")
	pass

#########################
# function to calculate the marks (avg times and others...)
#########################
def getOutputs():
	tree = ET.parse(path + 'output-tripinfos.xml')
	root = tree.getroot()
	avgTime = 0
	i = 0
	for tripinfo in root.findall('tripinfo'):
		avgTime += float(tripinfo.get('duration'))
		i += 1
	return avgTime/i	

#########################
# function to cross the cycles
#########################
def crossing(chr1, chr2, size):
	crossed = np.zeros((2,len(chr1)))
	crossed[0,0:size] = chr1[0:size]
	crossed[1,0:size] = chr2[0:size]
	crossed[0,size:] = chr2[size:]
	crossed[1,size:] = chr1[size:]	
	return crossed

######################
# initialisition of a random population
######################
#number of duration parameters
lightsNb = 16
max_time = 60
min_time = 5

populationSize = 40
population = np.random.random((populationSize,lightsNb))
population = min_time + (max_time - min_time) * population
mutationProba = 1/float(lightsNb)


# reiterate untill the population's evaluation is to far from the fitness fonction
# untill we have a fitness funcition, will use a for loop with a fixed number of itterations
for x in xrange(1,50):
		
	######################
	# evaluation
	######################
	marks = np.zeros((populationSize))
		
	if x==1: #first iteration 
		for i in range(populationSize):
			writeTimes(population[i,:])
			os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg')
			marks[i] = getOutputs()
	else:
		marks[0:populationSize/2] = nextMarks
		for i in range(populationSize/2,populationSize):
			writeTimes(population[i,:])
			os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg')
			marks[i] = getOutputs()

	# revearse marks
	initialMarks = marks
	marks = np.sum(marks) - marks
	#increase proba of best mark
	marks[np.argmax(marks)] += 300
	marks = np.exp(marks-np.amin(marks))
	######################
	# Selection
	######################
	#random choose of N/2 candidates 
	selected = np.zeros((populationSize,lightsNb))
	index = range(populationSize)
	nextMarks = np.zeros((populationSize/2))

	for i in range(populationSize/2):
		choix = choice(index, p= marks[index[:]]/np.sum(marks[index[:]]))
		selected[i,:] = population[choix,:]
		nextMarks[i] = initialMarks[choix]
		index.remove(choix)
	#print selected
	#print nextMarks
	######################
	# Crossing and Mutation
	######################
	crossingProba = 0.3
	crossed = np.zeros((2,lightsNb))
	for i in range(0, populationSize/2, 2):
		if(i+1<populationSize/2): 
			crossed = crossing(selected[i,:],selected[i+1,:], int(lightsNb*crossingProba))
			for j in range(lightsNb):
				# Mutation on child 1
				if random.random() < mutationProba:
					mutation = random.random()
					mutation = min_time + (max_time - min_time) * mutation
					crossed[0,j] = mutation
				# Mutation on child 2
				if random.random() < mutationProba:
					mutation = random.random()
					mutation = min_time + (max_time - min_time) * mutation
					crossed[1,j] = mutation
			selected[i+populationSize/2,:] = crossed[0,:]
			selected[i+populationSize/2+1,:] = crossed[1,:]
		else: #when the last element is alone and no couple can be done
			selected[i+populationSize/2,:] = selected[i,:]
			# Mutation on child 1
			for j in range(lightsNb):
				if random.random() < mutationProba:
					mutation = random.random()
					mutation = min_time + (max_time - min_time) * mutation
					selected[i+populationSize/2,j] = mutation

	# reinitialize population for next process
#	population = selected
#	print initialMarks

#print population	

marks = np.zeros((populationSize))

marks[0:populationSize/2] = nextMarks
for i in range(populationSize/2,populationSize):
	writeTimes(population[i,:])
	os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg')
	marks[i] = getOutputs()

print marks