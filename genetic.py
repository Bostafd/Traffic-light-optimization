from __future__ import division
import random
import numpy as np
from numpy.random import choice
import os
import xml.etree.ElementTree as ET

path = ''
#path = 'sumo-0.27.1\\tools\\2_INT\\2_INT\\'

#########################
# Here we chose our optimization scheme
#########################
priviledge=5
var=0
print ("which optimization scheme would you like to use :"+ "\n")
print ("1. Mixed optimization - for multiple criterias")
print ("2. Unique optimization - for one criteria"+ "\n")
while True:
    var = raw_input("Please chose between 1 and 2: "+ "\n")
    if var=="1":
        print ("you chose a unique parameter"+ "\n")
        criteria="unique"
        print ("which criteria would you like to use :"+ "\n")
        print ("1. Duration - Time spent by vehicles on the simulation")
        print ("2. Route Length - Route length traveled by vehicles on the simulation")
        print ("3. Wait Step - Number of steps in which the cehicle speed was below 0.1m/s")
        print ("4. Time Loss - Time Lost by vehicles"+ "\n")
        while True:
            var = raw_input("Please chose between 1, 2, 3 and 4 : "+ "\n")
            if var=="1":
                print("you chose to optimize a unique parameter : Duration"+ "\n")
                optimization="duration"
                break
            if var=="2":
                print("you chose to optimize a unique parameter : Route Length"+ "\n")
                optimization="routeLength"
                break
            if var=="3":
                print("you chose to optimize a unique parameter : Wait Step"+ "\n")
                optimization="waitSteps"
                break
            if var=="4":
                print("you chose to optimize a unique parameter : Time Loss"+ "\n")
                optimization="timeLoss"
                break
            else:
                pass
        break
    if var=="2":
        print("you chose multiple parameters")
        criteria="multiple"
        print ("which criteria would you like to priveledge the most among these parameters:"+ "\n")
        print ("0. None - Uniform Optimization")
        print ("1. Duration - Time spent by vehicles on the simulation")
        print ("2. Route Length - Route length traveled by vehicles on the simulation")
        print ("3. Wait Step - Number of steps in which the cehicle speed was below 0.1m/s")
        print ("4. Time Loss - Time Lost by vehicles"+ "\n")
        while True:
            var = raw_input("Please chose between 0,1, 2, 3 and 4 : "+ "\n")
            if var=="0":
                print("you chose to optimize all parameters with no priviledge "+ "\n")
                optimization="uniform"
                break
            if var=="1":
                print("you chose multiple parameters and emphasized on parameter : Duration"+ "\n")
                optimization="duration"
                break
            if var=="2":
                print("you chose multiple parameters and emphasized on parameter : Route Length"+ "\n")
                optimization="routeLength"
                break
            if var=="3":
                print("you chose multiple parameters and emphasized on parameter : Wait Step"+ "\n")
                optimization="waitSteps"
                break
            if var=="4":
                print("you chose multiple parameters and emphasize parameter : Time Loss"+ "\n")
                optimization="timeLoss"
                break
            else:
                pass
        break
        break
    else:
        pass

#########################
# function that writes the new trafic light durations in the network file
#########################
def writeTimes(new_time):
    #access xml file
    tree = ET.parse(path + 'twoIntersections.net.xml')
    root = tree.getroot()
    j = 0
    for tlLogic in root.findall('tlLogic'):
        for phase in tlLogic.findall('phase'):
            phase.set('duration', str(new_time[j]))
            j += 1
    #writing input in xml file 
    tree.write(path + "twoIntersections.net.xml")
    pass


#########################
# function that computes important criterias for evaluation
# by default we will be using uniform optimization
#########################
def getOutputs(criteria="unique",optimization="duration"):
    tree = ET.parse(path + 'output-tripinfos.xml')
    root = tree.getroot()
    #the parameters that we chose to use for our optimization
    avgDuration = 0
    avgRouteLength = 0
    avgWaitSteps = 0
    avgTimeLoss = 0
    #This list will contain the averages of our parameters
    L=[]
    #iteration counter for averaging
    i = 0
    
    if criteria is "multiple":
        if optimization is "uniform":
            for tripinfo in root.findall('tripinfo'):
                avgDuration += float(tripinfo.get('duration'))
                avgRouteLength += float(tripinfo.get('routeLength'))
                avgWaitSteps += float(tripinfo.get('waitSteps'))
                avgTimeLoss += float(tripinfo.get('timeLoss'))
                i += 1
            L.append(avgDuration/i)
            L.append(avgRouteLength/i)
            L.append(avgWaitSteps/i)
            L.append(avgTimeLoss/i)
            return (L[0]+L[1]+L[2]+L[3])/4
        if optimization is "duration":
            for tripinfo in root.findall('tripinfo'):
                avgDuration += float(tripinfo.get('duration'))
                avgRouteLength += float(tripinfo.get('routeLength'))
                avgWaitSteps += float(tripinfo.get('waitSteps'))
                avgTimeLoss += float(tripinfo.get('timeLoss'))
                i += 1
            L.append(avgDuration/i)
            L.append(avgRouteLength/i)
            L.append(avgWaitSteps/i)
            L.append(avgTimeLoss/i)
            return (priviledge*L[0]+L[1]+L[2]+L[3])/(priviledge+3)
        if optimization is "routeLenght":
            for tripinfo in root.findall('tripinfo'):
                avgDuration += float(tripinfo.get('duration'))
                avgRouteLength += float(tripinfo.get('routeLength'))
                avgWaitSteps += float(tripinfo.get('waitSteps'))
                avgTimeLoss += float(tripinfo.get('timeLoss'))
                i += 1
            L.append(avgDuration/i)
            L.append(avgRouteLength/i)
            L.append(avgWaitSteps/i)
            L.append(avgTimeLoss/i)
            return (L[0]+priviledge*L[1]+L[2]+L[3])/(priviledge+3)
        if optimization is "waitSteps":
            for tripinfo in root.findall('tripinfo'):
                avgDuration += float(tripinfo.get('duration'))
                avgRouteLength += float(tripinfo.get('routeLength'))
                avgWaitSteps += float(tripinfo.get('waitSteps'))
                avgTimeLoss += float(tripinfo.get('timeLoss'))
                i += 1
            L.append(avgDuration/i)
            L.append(avgRouteLength/i)
            L.append(avgWaitSteps/i)
            L.append(avgTimeLoss/i)
            return (L[0]+L[1]+priviledge*L[2]+L[3])/(priviledge+3)
        if optimization is "timeLoss":
            for tripinfo in root.findall('tripinfo'):
                avgDuration += float(tripinfo.get('duration'))
                avgRouteLength += float(tripinfo.get('routeLength'))
                avgWaitSteps += float(tripinfo.get('waitSteps'))
                avgTimeLoss += float(tripinfo.get('timeLoss'))
                i += 1
            L.append(avgDuration/i)
            L.append(avgRouteLength/i)
            L.append(avgWaitSteps/i)
            L.append(avgTimeLoss/i)
            return (L[0]+L[1]+L[2]+priviledge*L[3])/(priviledge+3)
    else :
        if optimization is "duration":
            for tripinfo in root.findall('tripinfo'):
                avgDuration += float(tripinfo.get('duration'))
                i += 1
            return avgDuration/i
        if optimization is "routeLength":
            for tripinfo in root.findall('tripinfo'):
                avgRouteLength += float(tripinfo.get('routeLength'))
                i += 1
            return avgRouteLength/i
        if optimization is "waitSteps":
            for tripinfo in root.findall('tripinfo'):
                avgWaitSteps += float(tripinfo.get('waitSteps'))
                i += 1
            return avgWaitSteps/i
        if optimization is "timeLoss":
            for tripinfo in root.findall('tripinfo'):
                avgTimeLoss += float(tripinfo.get('timeLoss'))
                i += 1
            return avgTimeLoss/i
        
            

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

populationSize = 8
population = np.random.random((populationSize,lightsNb))
population = min_time + (max_time - min_time) * population
#we transform the trafic lights into integers
for i in range(populationSize):
    for j in range(lightsNb):
        population[i,j]=int(population[i,j])
        
mutationProba = 1/float(lightsNb)

#########################
# function to mutate a gene
#########################
def mutate():
    mutation = random.random()
    mutation = min_time + (max_time - min_time) * mutation
    return int(mutation)


# reiterate until the population's evaluation is to far from the fitness fonction -QUESTION-
# until we have a fitness function, will use a for loop with a fixed number of iterations -QUESTION-
for x in range(1,20):       
#####################N
# evaluation of the scores produced by each member of the population
######################
#first we create an array that will contain the scores
    print"processing iteration : " + str(x) +"......"
    marks = np.zeros((populationSize))
        
    if x==1: #first iteration 
        for i in range(populationSize):
            writeTimes(population[i,:])
            os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg'+' >nul 2>&1')
            marks[i] = getOutputs(criteria,optimization)
    else:
        marks[0:int(populationSize/2)] = nextMarks
        for i in range(int(populationSize/2),populationSize):
            writeTimes(population[i,:])
            os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg'+' >nul 2>&1')
            marks[i] = getOutputs(criteria,optimization)

    # we modify the scores to get higher values for low durations
    #print("for iteration " , x ," we have scores of ", np.sort(marks))
    print"the mean value of the scores in the population is : " , np.mean(marks)
    initialMarks = marks
    marks = np.sum(marks) - marks
    #we increase probability of selection for the people who have the best scores
    marks[np.argmax(marks)] += 300
    marks = np.exp(marks-np.amin(marks))
    ######################
    # Selection
    ######################
    #randomly choose N/2 people from the population, Note that higher scores have more chances of being selected
    selected = np.zeros((populationSize,lightsNb))
    index = range(populationSize)
    nextMarks = np.zeros(int(populationSize/2))
    #Note that nextmarks only contains N/2 people of the population 
    for i in range(int(populationSize/2)):
        choix = choice(index, p= marks[index[:]]/np.sum(marks[index[:]]))
        selected[i,:] = population[choix,:]
        nextMarks[i] = initialMarks[choix]
        #python2
        index.remove(choix)
        #python3
        #index.pop([choix])
    #print selected
    #print ("this is next marks ",nextMarks)
    ######################
    # Crossing and Mutation, Note we only cross and mutate the ones that we selected, so the ones that we deemed were the best
    ######################
    #why not a fixed crossing probability 
    crossingProba = 0.3
    crossed = np.zeros((2,lightsNb))
    for i in range(0, int(populationSize/2), 2):
        if(i+1<populationSize/2): 
            #we cross pairs of the recently selected people to get mixed children
            crossed = crossing(selected[i,:],selected[i+1,:], int(lightsNb*crossingProba))
            
            #we then generate random mutations for these crossed children
            for k in range(2):
                for j in range(lightsNb):
                    if random.random() < mutationProba:
                        crossed[k,j] = mutate()
                #we put them in the remaining selected children
                selected[i+int(populationSize/2)+k,:] = crossed[k,:]
        else: #when the last element is alone and no couple can be done we just mutate it to generate a child
            selected[i+int(populationSize/2),:] = selected[i,:]
            # Mutation on remaining parent that will be a mutated childs
            for j in range(lightsNb):
                if random.random() < mutationProba:
                    selected[i+int(populationSize/2),j]=mutate()

    # reinitiate population for next process
    population = selected

marks = np.zeros((populationSize))
marks[0:int(populationSize/2)] = nextMarks
for i in range(int(populationSize/2),populationSize):
    writeTimes(population[i,:])
    os.system('sumo ' + path + 'twoIntersections.500.sumo.cfg'+' >nul 2>&1')
    marks[i] = getOutputs(criteria,optimization)

print (np.sort(initialMarks))
#print marks
