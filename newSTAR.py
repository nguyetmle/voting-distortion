import numpy
from numpy import random
import math
from vote import Vote
from election import Election

class SVoter:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.id = num
        self.scores = {}

    def setScores(self,scoreDict):
        self.scores = scoreDict

    def __str__(self):
        return "Voter "+str(self.id)

class SCandidate:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.id = num

    def __str__(self):
        return "Candidate "+str(self.id)

def plurality(ballots):
    votes = {}
    for ballot in ballots:
        if ballot[0] in votes:
            votes[ballot[0]] += 1
        else:
            votes[ballot[0]] = 1
    sorted_dict = sorted(votes.items(), key = lambda kv: kv[1], reverse = True)      
    return sorted_dict[0][0]

def borda(ballots):
    points = {}
    for ballot in ballots:
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

def copeland(ballots, candidates):
    points = {}
    score1 = 0
    score2 = 0
    for i in range(len(candidates)):
        for j in range(i + 1, len(candidates)):
            for ballot in ballots:
                found = False
                k = 0
                while not found:
                    if ballot[k] == candidates[i]:
                        score1 += 1
                        found = True
                    elif ballot[k] == candidates[j]:
                        score2 += 1
                        found = True
                    k += 1             
            if score1 >= score2:
                if candidates[i] in points:
                    points[candidates[i]] += 1
                else:
                    points[candidates[i]] = 1
            else:
                if candidates[j] in points:
                    points[candidates[j]] += 1
                else:
                    points[candidates[j]] = 1
            score1 = 0
            score2 = 0
    sorted_dict = sorted(points.items(), key = lambda kv: kv[1], reverse = True)
    return sorted_dict[0][0]

def STV(ballots):
    votes = []
    for ballot in ballots:
        vote = Vote(ballot)
        votes.append(vote)
    election = Election(votes)
    election.run_election()
    winner = election.winner
    return winner

def getBallots(voters, candidates):
    ballots = []
    for voter in voters:
        distances = {}
        for candidate in candidates:
            distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2)
            distances[candidate] = distance         
        sorted_dict = sorted(distances, key = distances.get)
        ballots.append(sorted_dict)
    return ballots

def rMajorityCheck(voters,candidates,ballots):
    canDict = {can:0 for can in candidates}
    for ballot in ballots:
        winningCan = ballot[0]
        canDict[winningCan] += 1
    benchmark = len(voters)/2
    for can in candidates:
        if canDict[can] >= benchmark:
            return can
    return "There is no ranked majority winner"

def rCondorcetCheck(candidates,ballots):
    pairs = []
    for can in candidates:
        for can2 in candidates:
            if can != can2:
                pair = (can,can2)
                pairs.append(pair)
    pairDict = {pair:0 for pair in pairs}
    for ballot in ballots:
        for i in range(len(ballot)):
            j = len(ballot)-i - 1
            k = 1
            while j>0:
                pairing = (ballot[i],ballot[i+k])
                pairDict[pairing] += 1
                j -= 1
                k += 1
                
    canDict = {can: True for can in candidates}
    for can in candidates:
        for can2 in candidates:
            if can != can2:
                wins = pairDict[(can,can2)]
                losses = pairDict[(can,can2)]
                if losses >= wins:
                    canDict[can] = False
    for can in candidates:
        if canDict[can]==True:
            return can                
    return "There is no ranked condorcet winner"

def rankedWinners(voters, candidates):
    ballots = getBallots(voters, candidates)
    pWinner = plurality(ballots)
    bWinner = borda(ballots)
    cWinner = copeland(ballots,candidates)
    stvWinner = STV(ballots)
    rMajWinner = rMajorityCheck(voters,candidates,ballots)
    rConWinner = rCondorcetCheck(candidates,ballots)
    return pWinner, bWinner, cWinner, stvWinner, rMajWinner, rConWinner

def getScores(voters, candidates):
    totalScores = {}
    for voter in voters:
        distances = {}
        minDis = float('inf')
        maxDis = 0
        for candidate in candidates:
            distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2)
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
        return "It is a tie"
    elif can1tot > can2tot:
        return can1
    else:
        return can2

def STAR(voters, candidates):
    finalScores = getScores(voters, candidates)
    sorted_dict = sorted(finalScores, key = finalScores.get, reverse=True)
    firstCandidate = sorted_dict[0]
    secondCandidate = sorted_dict[1]
    winner = runoff(voters, firstCandidate, secondCandidate)
    return winner

def sMajorityCheck(voters,candidates):
    canDict = {can: 0 for can in candidates}
    for voter in voters:
        ballot = voter.scores
        for can in candidates:
            if ballot[can] == 5:
                canDict[can] += 1
    benchmark = len(voters)/2
    for can in candidates:
        if canDict[can] >= benchmark:
            return can
    return "No outright scored majority winner"

def sCondorcetCheck(voters,candidates):
##    canDict = {can: 1 for can in candidates}
##    for voter in voters:
##        score = voter.scores
##        for can in candidates:
##            for can2 in candidates:
##                if can != can2:
##                    if score[can] < score[can2]:
##                        canDict[can] = 0
##    for can in candidates:
##        if canDict[can] == 1:
##            return can
    pairs = []
    for can in candidates:
        for can2 in candidates:
            if can != can2:
                pair = (can,can2)
                pairs.append(pair)
    pairDict = {pair:0 for pair in pairs}
    for voter in voters:
        score = voter.scores
        for pair in pairs:
            if score[pair[0]] > score[pair[1]]:
                pairDict[pair] += 1
    canDict = {can: True for can in candidates}
    for can in candidates:
        for can2 in candidates:
            if can != can2:
                wins = pairDict[(can,can2)]
                losses = pairDict[(can,can2)]
                if losses >= wins:
                    canDict[can] = False
    for can in candidates:
        if canDict[can]==True:
            return can                
    return "There is no STAR condorcet winner"
                        
def main():
    n = 1000
    m = 5
    voters = []
    candidates = []
    for i in range(n):
        x = round(random.normal(50, 20), 1)
        y = round(random.normal(50, 20), 1)
        voter = SVoter(x, y, i)
        voters.append(voter)

    for i in range(m):
        x = round(random.normal(50, 20), 1)
        y = round(random.normal(50, 20), 1)
        candidate = SCandidate(x, y, i)
        candidates.append(candidate)

    minDistance = float('inf')
    OPTcanidate = candidates[0]
    for candidate in candidates:
        sumDistance = 0
        for voter in voters:
            distance = math.sqrt((voter.x - candidate.x) ** 2 + (voter.y - candidate.y) ** 2)
            sumDistance += distance
        if sumDistance < minDistance:
            minDistance = sumDistance
            OPTcandidate = candidate

    pWinner,bWinner,cWinner,stvWinner,rMaj,rCon = rankedWinners(voters, candidates)
    starWinner = STAR(voters,candidates)
    print("**** The optimal candidate was: ****")
    print(OPTcandidate)
    print("The election winners by mechanism are:")
    print("Plurality: ",end="")
    print(pWinner)
    print("Borda: ",end="")
    print(bWinner)
    print("Copeland: ",end="")
    print(cWinner)
    print("STV: ",end="")
    print(stvWinner)
    print("STAR: ",end="")
    print(starWinner)
    
    sMajWinner = sMajorityCheck(voters,candidates)
    print("**** The candidate who had the outright scoring majority is: ****")
    print(sMajWinner)
    sConWinner = sCondorcetCheck(voters,candidates)
    print("**** The candidate who beat every other candidate in a scored head to head is: ****")
    print(sConWinner)
    print("**** The candidate who had the outright ranked majority is: ****")
    print(rMaj)
    print("**** The candidate who beat every other candidate in a ranked head to head is: ****")
    print(rCon)    

    
    
if __name__ == "__main__":
    for i in range(30):
        print("Test #"+str(i+1))
        main()
        print()
        print("===============================")
