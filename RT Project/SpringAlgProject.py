#!/usr/bin/env python

"""
SpringAlgProject.py by Ryan Becker and Ginnie White

Based on schedulability.py - suite of schedulability tests by Tanya Amert

NOTE: To run this, you must have taskset.py in the same folder!
"""

from taskset import TaskSetJsonKeys, Task

import matplotlib.pyplot as plt
import random

def getUniformValue(a, b):
    """
    Returns a value uniformly selected from the range [a,b].
    """
    return random.uniform(a,b)

# Per-task density functions
densityFunc = lambda : getUniformValue(0.1, 0.5)
#Function included in case we want to explore different ways of generating numbers
densityFunc2 = lambda: random.randint(0.1, 0.5)

# deadlines are in milliseconds
deadlineFunc = lambda : getUniformValue(1, 10)
#Function included in case we want to explore different ways of generating numbers
densityFunc2 = lambda: random.randint(1,10)

## TODO: update to reflect density, potentially ditch the periodFunc
def generateRandomTaskSet(targetDensity, densityFunc, deadlineFunc):
    """
    Generates a random task set with total density targetDensity.

    Just returns the task set as a list of Task objects, rather than
    the proper TaskSet type.
    """
    densitySum = 0

    # Generate tasks until the utilization target is met
    taskSet = []
    i = 0
    while densitySum < targetDensity:
        taskId = i+1
        # Choose the utilization for the task based on the utilization function
        task_density = densityFunc()
        # If the task's utilization would push it over the target, instead choose
        # its utilization to be the remaining utilization to reach the target sum.
        if task_density+ densitySum > targetDensity:
            task_density = targetDensity - densitySum
        densitySum += task_density
        # Choose task parameters:
        # * offset
        offset = random.randint(0, 10)
        # * period
        relativeDeadline = deadlineFunc()
        # * WCET <-- change this to be task density * min(di, ti)
        wcet = task_density * relativeDeadline

        period = 0
        i += 1

        # Build the dictionary for the task parameters
        taskDict = {}
        taskDict[TaskSetJsonKeys.KEY_TASK_ID] = taskId
        taskDict[TaskSetJsonKeys.KEY_TASK_PERIOD] = period
        taskDict[TaskSetJsonKeys.KEY_TASK_WCET] = wcet
        taskDict[TaskSetJsonKeys.KEY_TASK_DEADLINE] = relativeDeadline
        taskDict[TaskSetJsonKeys.KEY_TASK_OFFSET] = offset

        task = Task(taskDict)
        taskSet.append(task)

    return taskSet

'''
Compute the schedule that the heuristic would use on the task set, then sees if
that schedule is actually feasible. Return True if it is, False otherwise.
score_calculator changes based on the heuristic used to order tasks the way we
want. Computed dynamically, so the computer only makes choices about task sets
after they have been releeased
'''
def testFunc(taskSet, score_calculator):
    #actually come up with the order
    time = 0
    tree= []

    topJob = 0
    topJobScore = 10000
    #if we have not gone through all the tasks, keep going
    while (len(tree) != 0 or len(taskSet) != 0):
        jobsToRemove = []
        nextList = []
        for task in taskSet:
            #get all jobs that released at or before time
            if task.offset <= time:
                tree.append(task)
                jobsToRemove.append(task)
        #remove all the released jobs from the taskSet
        for task in taskSet:
            if task not in jobsToRemove:
                nextList.append(task)
        taskSet = nextList

        if (len(tree) !=0):
            topJob = tree[0]
            topJobScore = score_calculator(topJob)
            #pick job via Heuristic
            for task in tree:
                if score_calculator(task) < topJobScore:
                    topJob = task
                    topJobScore = score_calculator(task)

            time += topJob.wcet
            if (topJob.offset + topJob.relativeDeadline < time):
                return False
            tree.remove(topJob)

        #If nothing released at the time, then increment time by one and keep going
        else:
            time += 1
    #if we made it through all the jobs, the schedule is feasible
    return True

#These calculate the score each heuristic
#Heuristic 1: Order by the shortest relative deadline
def h1Score(task):
    return task.relativeDeadline
#Heuristic 2: Di + W*Ci. Paper was unclear about what weight to use so we chose 3
def h2Score(task):
    return (task.relativeDeadline + (3 * task.wcet))
#Heuristic #: Di - (Ri + Ci), laxity
def h3Score(task):
    return ((task.relativeDeadline - (task.offset + task.wcet)))
#Heuristic 4: Order by lowest task density
def h4Score(task):
    return (task.wcet/ task.relativeDeadline)
#Heuristic 5: Order by lowest task density (with denominator squared)
def h5Score(task):
    return (task.wcet/ (task.relativeDeadline**2))


def checkSchedulability(numTaskSets, targetUtilization, densityFunc, deadlineFunc, scoreFunc):
    """
    Generates numTaskSets task sets using a given density-generation function
    and a given deadline-generation function, such that the task sets have a given
    target system density.  Uses the given schedulability test along with a function
    that makes choices based on a heuristic to determine what fraction of the
    task sets are schedulable.

    Returns: the fraction of task sets that pass the schedulability test.
    """
    count = 0
    for i in range(numTaskSets):
        taskSet = generateRandomTaskSet(targetUtilization, densityFunc, deadlineFunc)

        if testFunc(taskSet, scoreFunc):
            count += 1

    return count / numTaskSets

def performTests(numTests):
    densityVals = []
    for i in range(10):
        val = 0.1 + i * 0.1
        densityVals.append(val)


    results = {}
    results["Di"] = []
    results["Di + W*Ci"] = []
    results["Laxity"] = []
    results["Density"] = []
    results["Modified Density"] = []

    for density in densityVals:
        h1Result = checkSchedulability(numTests, density, densityFunc, deadlineFunc, h1Score)
        h2Result = checkSchedulability(numTests, density, densityFunc, deadlineFunc, h2Score)
        h3Result = checkSchedulability(numTests, density, densityFunc, deadlineFunc, h3Score)
        h4Result = checkSchedulability(numTests, density, densityFunc, deadlineFunc, h4Score)
        h5Result = checkSchedulability(numTests, density, densityFunc, deadlineFunc, h5Score)

        results["Di"].append(h1Result)
        results["Di + W*Ci"].append(h2Result)
        results["Laxity"].append(h3Result)
        results["Density"].append(h4Result)
        results["Modified Density"].append(h5Result)

    return densityVals, results

def plotResults(densityVals, results):
    plt.figure()

    LINE_STYLE = ['b:+', 'g-^', 'r-s', 'b', 'g']


    for (styleId, label) in enumerate(results):
        yvals = results[label]

        plt.plot(densityVals, yvals, LINE_STYLE[styleId], label=label)

    plt.legend(loc="best")

    plt.xlabel("System Density")
    plt.ylabel("Schedulability")
    plt.title("Schedulability for Different Heuristics")

    plt.show()

def testSchedulability():
    random.seed(None) # seed the random library

    # Perform the schedulability tests
    densityVals, results = performTests(1000)

    # Plot the results
    plotResults(densityVals, results)

if __name__ == "__main__":
    testSchedulability()
