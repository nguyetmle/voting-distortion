from numpy import random
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
    def __init__(self, n, m):
        self.voters = []
        selfcandidates = []
        for i in range(n):
            x = round(random.normal(50, 20), 1)
            voter = SVoter(x, i)
            self.voters.append(voter)

        for i in range(m):
            x = round(random.normal(50, 20), 1)
            candidate = SCandidate(x, i)
            self.candidates.append(candidate)

        minDistance = float('inf')
        self.OPTcandidate = self.candidates[0]
        for candidate in self.candidates:
            sumDistance = 0
            for voter in self.voters:
                distance = abs(voter.x - candidate.x)
                sumDistance += distance
            if sumDistance < minDistance:
                minDistance = sumDistance
                self.OPTcandidate = candidate

        #get preference profile of each voter
        self.ballots = []
        for voter in voters:
            distances = {}
            for candidate in candidates:
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
        stvTie = election.isTie
        return winner, stvTie

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

    def getScores(voters, candidates):
        totalScores = {}
        for voter in voters:
            distances = {}
            minDis = float('inf')
            maxDis = 0
            for candidate in candidates:
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
            for candidate in candidates:
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

    def runoff(voters,can1,can2):
        can1tot = 0
        can2tot = 0
        for voter in voters:
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
        finalScores = self.getScores(self.voters, self.candidates)
        sorted_dict = sorted(finalScores, key = finalScores.get, reverse=True)
        firstCandidate = sorted_dict[0]
        secondCandidate = sorted_dict[1]
        winner = self.runoff(self.voters, firstCandidate, secondCandidate)
        return winner



    