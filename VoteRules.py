from numpy import random
import numpy as np
import math
from vote import Vote
from election import Election
import os
""" import matplotlib.pyplot as plt """
import time


class SVoter:
    def __init__(self, x, num):
        self.x = x
        self.id = num
        self.scores = {}

    def setScores(self,scoreDict):
        self.scores = scoreDict

    def __str__(self):
        return "Voter "+str(self.id)

class SCandidate:
    def __init__(self, x, num):
        self.x = x
        self.id = num

    def __str__(self):
        return "Candidate "+str(self.id)
    
class VoteResult:
    def __init__(self, n, m, distribution="normal"):
        self.voters = []
        self.candidates = []
        self.distribution = distribution

        #generate random coordinates of voters and candidates for different distributions
        if self.distribution == "normal":
            voters = random.normal(50, 18,n)
            candidates = random.normal(50, 18, m)
        elif self.distribution == "poisson":
            voters = random.poisson(30, n)
            candidates = random.poisson(30, m)
        elif self.distribution == "uniform":
            voters = random.uniform(0, 100, n)
            candidates = random.uniform(0, 100, m)
        elif self.distribution == "bimodal":
            voters1 = random.normal(30, 10, n//2)
            voters2 = random.normal(70, 10, n-n//2)
            voters = np.concatenate((voters1, voters2), axis=None)
            candidates1 = random.normal(30, 10, m//2)
            candidates2 = random.normal(70, 10, m-m//2)
            candidates = np.concatenate((candidates1, candidates2), axis = None)
        #generate voters and candidates based on the coordinates
        for i in range(len(voters)):
            voter = SVoter(voters[i], i)
            self.voters.append(voter)

        for i in range(len(candidates)):
        
            candidate = SCandidate(candidates[i], i)
            self.candidates.append(candidate)

        self.minDistance = float('inf')
        self.OPTcandidate = self.candidates[0]
        for candidate in self.candidates:
            sumDistance = 0
            for voter in self.voters:
                distance = abs(voter.x - candidate.x)
                sumDistance += distance
            if sumDistance < self.minDistance:
                self.minDistance = sumDistance
                self.OPTcandidate = candidate

        #get preference profile of each voter
        self.ballots = []
        for voter in self.voters:
            distances = {}
            for candidate in self.candidates:
                distance = abs(voter.x - candidate.x)
                distances[candidate] = distance         
            sorted_dict = sorted(distances, key = distances.get)
            self.ballots.append(sorted_dict)
        


    def plurality(self):
        votes = {}
        for ballot in self.ballots:
            if ballot[0] in votes:
                votes[ballot[0]] += 1
            else:
                votes[ballot[0]] = 1
        sorted_dict = sorted(votes.items(), key = lambda kv: kv[1], reverse = True)      
        return sorted_dict[0][0]

    def borda(self):
        points = {}
        for ballot in self.ballots:
            n = len(ballot)
            i = 1
            for candidate in ballot:
                if candidate in points:
                    points[candidate] += (n - i)
                else:
                    points[candidate] = (n - i)
                i += 1
        sorted_dict = sorted(points.items(), key = lambda kv: kv[1], reverse = True)     
        return sorted_dict[0][0]

    def STV(self):
        votes = []
        for ballot in self.ballots:
            vote = Vote(ballot)
            votes.append(vote)
        election = Election(votes)
        election.run_election()
        winner = election.winner
        
        return winner

    def copeland(self):
        points = {}
        score1 = 0
        score2 = 0
        for i in range(len(self.candidates)):
            for j in range(i + 1, len(self.candidates)):
                for ballot in self.ballots:
                    found = False
                    k = 0
                    while not found:
                        if ballot[k] == self.candidates[i]:
                            score1 += 1
                            found = True
                        elif ballot[k] == self.candidates[j]:
                            score2 += 1
                            found = True
                        k += 1             
                if score1 >= score2:
                    if self.candidates[i] in points:
                        points[self.candidates[i]] += 1
                    else:
                        points[self.candidates[i]] = 1
                else:
                    if self.candidates[j] in points:
                        points[self.candidates[j]] += 1
                    else:
                        points[self.candidates[j]] = 1
                score1 = 0
                score2 = 0
        sorted_dict = sorted(points.items(), key = lambda kv: kv[1], reverse = True)
        return sorted_dict[0][0]



    def pluralityVeto(self):
        points = {}
        for ballot in self.ballots:
            if ballot[0] in points:
                points[ballot[0]] += 1
            else:
                points[ballot[0]] = 1
        k = -1
        numToRemove = len(points) - 1
        while numToRemove>0:
            for ballot in self.ballots:
                if ballot[k] in points:
                    if points[ballot[k]] == 1:
                        del points[ballot[k]]
                        numToRemove -= 1
                        if numToRemove == 0:
                            break
                    else:
                        points[ballot[k]] -= 1
                else:
                    j = k
                    while not ballot[j] in points:
                        j -= 1
                    if points[ballot[j]] == 1:
                        del points[ballot[j]]
                        numToRemove -= 1
                        if numToRemove == 0:
                            break
                    else:
                        points[ballot[j]] -= 1
            k -= 1
        winner = list(points)
        return winner[0]   

    def getScores(self):
        totalScores = {}
        for voter in self.voters:
            distances = {}
            minDis = float('inf')
            maxDis = 0
            for candidate in self.candidates:
                distance = abs(voter.x - candidate.x)
                distances[candidate] = int(distance)
                if distance >= maxDis:
                    maxDis = int(distance)
                if distance <= minDis:
                    minDis = int(distance)
            disRange = maxDis - minDis
            scale = round(disRange/6)
            scoringMatrix = []
            zero = list(range(maxDis-scale,maxDis+1))
            one = list(range(maxDis-(scale*2),maxDis-scale))
            two = list(range(maxDis-(scale*3),maxDis-(scale*2)))
            three = list(range(maxDis-(scale*4),maxDis-(scale*3)))
            four = list(range(maxDis-(scale*5),maxDis-(scale*4)))
            five = list(range(minDis,maxDis-(scale*5)))
            scoringMatrix.append(zero)
            scoringMatrix.append(one)
            scoringMatrix.append(two)
            scoringMatrix.append(three)
            scoringMatrix.append(four)
            scoringMatrix.append(five)
            for candidate in self.candidates:
                dis = distances[candidate]
                i = 0
                for score in scoringMatrix:
                    if dis in score:
                        distances[candidate] = i
                        if candidate not in totalScores:
                            totalScores[candidate] = i
                        else:
                            totalScores[candidate] += i
                    i += 1
            voter.setScores(distances)
        return totalScores

    def runoff(self, can1,can2):
        can1tot = 0
        can2tot = 0
        for voter in self.voters:
            voterBallot = voter.scores
            score1 = voterBallot[can1]
            score2 = voterBallot[can2]
            if score1 > score2:
                can1tot += 1
            elif score2 > score1:
                can2tot += 1
        if can1tot == can2tot:
            return False
        elif can1tot > can2tot:
            return can1
        else:
            return can2

    def STAR(self):
        finalScores = self.getScores()
        sorted_dict = sorted(finalScores, key = finalScores.get, reverse=True)
        firstCandidate = sorted_dict[0]
        secondCandidate = sorted_dict[1]
        winner = self.runoff(firstCandidate, secondCandidate)
        return winner
    
    def distortion(self,candidate):
        if not candidate:
            return False
        
        sumDistance = 0 
        for voter in self.voters:
            distance = abs(voter.x - candidate.x)
            sumDistance += distance

    
        distortion = sumDistance / self.minDistance
        return distortion
        


def main():

    test = VoteResult(3, 10, "uniform")
    print(test.STV())
    print(test.distortion(test.STV()))
if __name__ == "__main__":  
    main()
    