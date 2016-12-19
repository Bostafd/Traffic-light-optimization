import random
import numpy as np
from numpy.random import choice
import os
import xml.etree.ElementTree as ET

path = ''
#path = 'sumo-0.27.1\\tools\\2_INT\\2_INT\\'


#########################
# function that writes the new trafic light durations in the network file
#########################
def writeTimes(new_time):
    tree = ET.parse(path + 'twoIntersections.net.xml')
    root = tree.getroot()
    j = 0
    for tlLogic in root.findall('tlLogic'):
        for phase in tlLogic.findall('phase'):
            phase.set('duration', str(new_time[j]))
            j += 1
        
    tree.write(path + "twoIntersections.net.xml")
    pass


#########################
# function that computes important criterias for evaluation
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
    #rather use size-1 in one of the terms 
    crossed = np.zeros((2,len(chr1)))
    crossed[0,0:size] = chr1[0:size]
    crossed[1,0:size] = chr2[0:size]
    crossed[0,size:] = chr2[size:]
    crossed[1,size:] = chr1[size:]    
    return crossed

######################
# initialisation of a random population
######################
#Trafic light parameters
lightsNb = 16
max_time = 60
min_time = 5

populationSize = 4
population = np.random.random((populationSize,lightsNb))
population = min_time + (max_time - min_time) * population
#we transform the trafic lights into integers
for i in range(populationSize):
    for j in range(lightsNb):
        population[i,j]=int(population[i,j])
        
mutationProba = 1/float(lightsNb)


# reiterate until the population's evaluation is to far from the fitness fonction -QUESTION-
# until we have a fitness function, will use a for loop with a fixed number of iterations -QUESTION-
#why xrange ?
for x in xrange(1,3):       
#####################N
# evaluation of the scores produced by each member of the population
######################
#first we create an array that will contain the scores
    marks = np.zeros((populationSize))
        
    if x==1: #first iteration 
        for i in range(populationSize):
            writeTimes(population[i,:])
            os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg')
            marks[i] = getOutputs()
    else:
        #not needed ?
        marks[0:populationSize/2] = nextMarks
        for i in range(populationSize/2,populationSize):
            writeTimes(population[i,:])
            os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg')
            marks[i] = getOutputs()

    # we modify the scores to get higher values for low durations
    initialMarks = marks
    #marks = np.sum(marks) - marks
    #we increase probability of selection for the people who have the best scores
    #marks[np.argmax(marks)] += 300
    #marks = np.exp(marks-np.amin(marks))
    ######################
    # Selection
    ######################
    #randomly choose N/2 people from the population, Note that higher scores have more chances of being selected
    selected = np.zeros((populationSize,lightsNb))
    index = range(populationSize)
    nextMarks = np.zeros((populationSize/2))
    #Note that nextmarks only contains N/2 people of the population 
    for i in range(populationSize/2):
        choix = choice(index, p= marks[index[:]]/np.sum(marks[index[:]]))
        selected[i,:] = population[choix,:]
        nextMarks[i] = initialMarks[choix]
        index.remove(choix)
    #print selected
    #print nextMarks
    ######################
    # Crossing and Mutation, Note we only cross and mutate the ones that we selected, so the ones that we deemed were the best
    ######################
    #why not a fixed crossing probability 
    crossingProba = 0.3
    crossed = np.zeros((2,lightsNb))
    for i in range(0, populationSize/2, 2):
        if(i+1<populationSize/2): 
            #we cross pairs of the recently selected people to get mixed children
            crossed = crossing(selected[i,:],selected[i+1,:], int(lightsNb*crossingProba))
            #why not 
            """
            #we then generate random mutations for these crossed children
            for k in range(2):
                for j in range(lightsNb):
                if random.random() < mutationProba:
                    mutation = random.random()
                    mutation = min_time + (max_time - min_time) * mutation
                    crossed[k,j] = mutation
                    #we put them in the remaining selected children
                    selected[i+populationSize/2+k,:] = crossed[k,:]
            """
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
        else: #when the last element is alone and no couple can be done we just mutate it to generate a child
            selected[i+populationSize/2,:] = selected[i,:]
            # Mutation on child 1
            for j in range(lightsNb):
                if random.random() < mutationProba:
                    mutation = random.random()
                    mutation = min_time + (max_time - min_time) * mutation
                    selected[i+populationSize/2,j] = mutation

    # reinitiate population for next process
    #forgot pop=selected ?
    population = selected
#    print initialMarks

#print population    

    #marks = np.zeros((populationSize))
    #marks[0:populationSize/2] = nextMarks
    """    for i in range(populationSize/2,populationSize):
        writeTimes(population[i,:])
        os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg')
        marks[i] = getOutputs()
    """
    print initialMarks
    print marks