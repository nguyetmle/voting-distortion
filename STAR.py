from numpy import random
import numpy as np
import math
from vote import Vote

class STARvoter:
    def __init__(self, canidateList, num):
        self.id = num
        self.canDict = {}
        for i in canidateList:
            self.canDict[i] = random.randint(0,5)
        self.canScores = sorted(self.canDict.items(), key=lambda kv:kv[1], reverse=True)
        self.orderedCans = []
        for i in self.canScores:
            self.orderedCans.append(i[0])

    def getScores(self, runCanScores):
        canidates = runCanScores.keys()
        for canidate in canidates:
            voterScore = self.canDict[canidate]
            runCanScores[canidate] += voterScore
        return runCanScores

    def voterWinner(self, can1, can2):
        score1 = self.canDict[can1]
        score2 = self.canDict[can2]
        if score1 == score2:
            return "None"
        elif score1 > score2:
            return can1
        else:
            return can2


##Set up election class that runs election phase one (score) and two (IRV)
class Election:
    def __init__(self, canList, numVoters):
        self.numVoters = numVoters
        self.voterList = []
        self.canList = canList
        for i in range(self.numVoters):
            votr = STARvoter(self.canList, i)
            self.voterList.append(votr)
        self.allScores = {}
        for can in self.canList:
            self.allScores[can] = 0
        self.canidateScoreLst = []
        self.top2 = []
        self.top2Scores = {}

    def displayScores(self):
        for i in self.canidateScoreLst:
            print(i+": "+str(self.allScores[i]))

    def scoreVoting(self):
        for voter in self.voterList:
            self.allScores = voter.getScores(self.allScores)
        finalScores = sorted(self.allScores.items(), key=lambda kv:kv[1], reverse=True)
        self.canidateScoreLst = []
        for i in finalScores:
            self.canidateScoreLst.append(i[0])
        self.top2 = self.canidateScoreLst[:2]

    def IRV(self):
        canidate1 = self.top2[0]
        canidate2 = self.top2[1]
        self.top2Scores = dict.fromkeys(self.top2, 0)
        for voter in self.voterList:
            voterChoice = voter.voterWinner(canidate1, canidate2)
            if voterChoice == canidate1:
                self.top2Scores[canidate1] += 1
            elif voterChoice == canidate2:
                self.top2Scores[canidate2] += 1

    def runElection(self):
        self.scoreVoting()
        print("====================================")
        print("After the scores were counted the canidate scores were as follows:")
        self.displayScores()
        print("Which means that "+self.top2[0]+" and "+self.top2[1]+" advance to the instant runoff")
        print("====================================")
        print("These are the results of the instant runoff")
        self.IRV()
        results = sorted(self.top2Scores.items(), key=lambda kv:kv[1], reverse=True)
        cans = []
        numBallots = []
        for i in results:
            cans.append(i[0])
            numBallots.append(i[1])
            print(i[0]+": "+str(i[1]))
        if numBallots[0] == numBallots[1]:
            print("The two canidates tied!!")
            print("This election could not be settled with STAR voting from "+str(self.numVoters)+" voters.")
        else:
            voteDiff = numBallots[0] - numBallots[1]
            if voteDiff == 1:
                print(cans[0]+" won by "+str(voteDiff)+" ballot!!")
            else:
                print(cans[0]+" won by "+str(voteDiff)+" ballots!!")
        print("**Note: Even though there were "+str(self.numVoters)+" voters in the election,",end=' ')
        print("the vote results from the runoff may not add up to "+str(self.numVoters)+" .",end=' ')
        print("This is because if a voter gave the two final canidates the same score on their",end=' ')
        print("ballot, they effectively prefer either canidate equally, and their ballot is not",end=' ')
        print("tallied in the final count.**")
        notCounted = self.numVoters - (numBallots[0] + numBallots[1])
        notCountedPct = (notCounted/self.numVoters)*100
        print()
        print("To further emphasize this point, of the "+str(self.numVoters)+" who participated in",end=' ')
        print("the election, "+str(notCounted)+" of them (or "+str(notCountedPct)+"%) were ambivalent",end=' ')
        print("between the final two canidates and did not have their ballot contribute to the final tally.")

def main():
    listOfCanidates = ["Adam", "Becky", "Charlie", "Donna","Evan","Farah","George","Haliey"]
    print("Welcome to a STAR voting simulator!")
    print("Your list of canidates are as follows:")
    for i in listOfCanidates:
        print(i)
    numberOfVoters = eval(input("How many voters would you like to simulate?: "))
    starElection = Election(listOfCanidates, numberOfVoters)
    starElection.runElection()
if __name__ == "__main__":
    main()
