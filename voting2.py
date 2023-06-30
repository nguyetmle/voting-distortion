from numpy import random
from election import Election
from vote import Vote
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

class Voter:
    def __init__(self, x, y, num):
        self.id = num
        self.x = x
        self.y = y

class Candidate:
    def __init__(self, x, y, num):
        self.id = num
        self.x = x
        self.y = y

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

def simulate(n, m, mechanism):
    voters = []
    candidates = []

    for i in range(n):
        # x = round(random.uniform(0, 100), 2)
        # y = round(random.uniform(0, 100), 2)
        # x = np.random.poisson(30)
        # y = np.random.poisson(30)
        x = round(random.normal(50, 15), 2)
        y = round(random.normal(50, 15), 2)
        voter = Voter(x, y, i)
        voters.append(voter)

    for i in range(m):
        # x = round(random.uniform(0, 100), 2)
        # y = round(random.uniform(0, 100), 2)
        # x = np.random.poisson(30)
        # y = np.random.poisson(30)
        x = round(random.normal(50, 15), 2)
        y = round(random.normal(50, 15), 2)
        candidate = Candidate(x, y, i)
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

    #print("opt:", OPTcandidate.id, "x:", OPTcandidate.x, "y:", OPTcandidate.y, "sum dist:", minDistance, "\n")

    ballots = getBallots(voters, candidates)

    if mechanism == "Borda":
        winner = borda(ballots)
    elif mechanism == "Copeland":
        winner = copeland(ballots, candidates)
    elif mechanism == "Plurality":
        winner = plurality(ballots)
    elif mechanism == "STV":
        winner = STV(ballots)

    sumDistance = 0
    for voter in voters:
        distance = math.sqrt((voter.x - winner.x) ** 2 + (voter.y - winner.y) ** 2)
        sumDistance += distance

    #print("winner:", winner.id, "x:", winner.x, "y:", winner.y, "sum dist:", sumDistance, "\n")

    distortion = sumDistance / minDistance

    #print("distortion:", distortion)

    correct = int(OPTcandidate == winner)
    # print(correct)
    return distortion, correct, voters, candidates, OPTcandidate, winner

def plot(voters, candidates, OPT, winner, mechanism):
    voterX = []
    voterY = []

    candidateX = []
    candidateY = []

    for voter in voters:
        voterX.append(voter.x)
        voterY.append(voter.y)
    for candidate in candidates:
        candidateX.append(candidate.x)
        candidateY.append(candidate.y)
    
    plt.figure()
    plt.scatter(voterX, voterY, c = "darkorange", s = 24, label = "Voters")
    plt.scatter(candidateX, candidateY, c = "blue", s = 24, label = "Candidates")
    plt.scatter([OPT.x], [OPT.y], c = "green", s = 56, label = "OPT")
    plt.scatter([winner.x], [winner.y], c = "purple", s = 24, label = "Winner")
    plt.xlim(0, 100)
    plt.ylim(0, 100)

    plt.title(mechanism+" Voter and Candidate Metric Space")
    
    plt.legend()
    plt.show()

def plotDistortion(nArray, nDistortions):
    
    nAvgDistortionPlurality = nDistortions[0]
    nWorstDistortionPlurality = nDistortions[1]
    
    nAvgDistortionBorda = nDistortions[2]
    nWorstDistortionBorda = nDistortions[3]
    
    nAvgDistortionCopeland = nDistortions[4]
    nWorstDistortionCopeland = nDistortions[5]

    nAvgDistortionSTV = nDistortions[6]
    nWorstDistortionSTV = nDistortions[7]

    plt.figure()
    plt.plot(nArray, nAvgDistortionPlurality, c = "red", linestyle = "dotted", label = "Plurality Average Distortion")
    plt.plot(nArray, nWorstDistortionPlurality, c = "red", label = "Plurality Worst Case Distortion")

    plt.plot(nArray, nAvgDistortionBorda, c = "blue", linestyle = "dotted", label = "Borda Average Distortion")
    plt.plot(nArray, nWorstDistortionBorda, c = "blue", label = "Borda Worst Case Distortion")

    plt.plot(nArray, nAvgDistortionCopeland, c = "green", linestyle = "dotted", label = "Copeland Average Distortion")
    plt.plot(nArray, nWorstDistortionCopeland, c = "green", label = "Copeland Worst Case Distortion")

    plt.plot(nArray, nAvgDistortionSTV, c = "orange", linestyle = "dotted", label = "STV Average Distortion")
    plt.plot(nArray, nWorstDistortionSTV, c = "orange", label = "STV Worst Case Distortion")

    # new_list = range(math.floor(min(nArray)), math.ceil(max(nArray))+1)
    # plt.xticks(new_list)
    plt.xlabel("Number of Voters (n)")
    plt.ylabel("Distortion")
    plt.title("Distortion vs. n (m = 10)")
    plt.legend()
    plt.show()

def plotCorrect(nArray, nCorrects):

    nCorrectP = nCorrects[0]
    nCorrectB = nCorrects[1]
    nCorrectC = nCorrects[2]
    nCorrectS = nCorrects[3]
    plt.figure()
    plt.plot(nArray, nCorrectP, c = "red", label = "Plurality")

    plt.plot(nArray, nCorrectB, c = "blue", label = "Borda")

    plt.plot(nArray, nCorrectC, c = "green", label = "Copeland")

    plt.plot(nArray, nCorrectS, c = "orange", label = "STV")

    new_list = range(math.floor(min(nArray)), math.ceil(max(nArray))+1)
    plt.xticks(new_list)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    plt.xlabel("Number of Voters (n)")
    plt.ylabel("% of Time OPT Chosen by Voting Mechanism")
    plt.title("Correct % vs. m (n = " + str(max(nArray)) + ")")
    plt.legend()
    plt.show()

def simulateRounds(rounds, n, m, mechanism):
    sumD = 0
    correctCount = 0
    maxD = 0
    
    for i in range(rounds):
        distortion, correct, voters, candidates, OPT, winner = simulate(n, m, mechanism)
        if distortion > maxD:
            maxD = distortion
        sumD += distortion
        correctCount += correct
    avgD = sumD / rounds
    correctPercent =  correctCount / rounds
    #print("Correct:",correctCount)
    #print("Rounds",rounds)
    return maxD, avgD, correctPercent, voters, candidates, OPT, winner
                   
def main():
    # n = 20
    # m = 10
    # rounds = 10
    mechanisms = ["Plurality", "Borda", "Copeland", "STV"]

    nArray = [10,50,100,200,500,1000]
    nAvgDistortionPlurality = []
    nWorstDistortionPlurality = []
    nCorrectPlurality = []

    nAvgDistortionBorda = []
    nWorstDistortionBorda = []
    nCorrectBorda = []

    nAvgDistortionCopeland = []
    nWorstDistortionCopeland = []
    nCorrectCopeland = []

    nAvgDistortionSTV = []
    nWorstDistortionSTV = []
    nCorrectSTV = []
    
    for n in nArray:
        #print("m =", m)
        for mechanism in mechanisms:
            maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(1000, n, 10, mechanism)

            if mechanism == "Plurality":
                nWorstDistortionPlurality.append(maxD)
                nAvgDistortionPlurality.append(avgD)
                nCorrectPlurality.append(correctPercent)
                #plot(voters, candidates, OPT, winner, mechanism)
                
            elif mechanism == "Borda":
                nWorstDistortionBorda.append(maxD)
                nAvgDistortionBorda.append(avgD)
                nCorrectBorda.append(correctPercent)
                #plot(voters, candidates, OPT, winner, mechanism)

            elif mechanism == "STV":
                nWorstDistortionSTV.append(maxD)
                nAvgDistortionSTV.append(avgD)
                nCorrectSTV.append(correctPercent)
                #plot(voters, candidates, OPT, winner, mechanism)
                
            else:
                nWorstDistortionCopeland.append(maxD)
                nAvgDistortionCopeland.append(avgD)
                nCorrectCopeland.append(correctPercent)
                #plot(voters, candidates, OPT, winner, mechanism)
    
    # mDistortions = [mAvgDistortionPlurality, mWorstDistortionPlurality, mAvgDistortionBorda,
    #                 mWorstDistortionBorda, mAvgDistortionCopeland, mWorstDistortionCopeland,
    #                 mAvgDistortionSTV, mWorstDistortionSTV]


    nDistortions = [nAvgDistortionPlurality, nWorstDistortionPlurality, nAvgDistortionBorda,
                    nWorstDistortionBorda, nAvgDistortionCopeland, nWorstDistortionCopeland,
                    nAvgDistortionSTV, nWorstDistortionSTV]
    # # mCorrects = [mCorrectPlurality, mCorrectBorda, mCorrectCopeland, mCorrectSTV]
    
    #plot(voters, candidates, OPT, winner)
    
    # plotDistortion(nArray, nDistortions, mArray, mDistortions)
    plotDistortion(nArray, nDistortions)

    # plotCorrect(mArray, mCorrects)

def main2():

    print("Plurality")
    maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(5000, 100, 20, "Plurality")
    print("Percent Correct: ", correctPercent)
    print("Winner: ",winner)
    print("Average Distortion: ", avgD)
    
    print("")
    print("STV")
    maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(5000, 100, 20, "STV")
    print("Percent Correct: ", correctPercent)
    print("Winner: ",winner)
    print("Average Distortion: ", avgD)

    print("")
    print("Borda Count")
    maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(5000, 100, 20, "Borda")
    print("Percent Correct: ", correctPercent)
    print("Winner: ",winner)
    print("Average Distortion: ", avgD)

    print("")
    print("Copeland")
    maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(5000, 100, 20, "Copeland")
    print("Percent Correct: ", correctPercent)
    print("Winner: ",winner)
    print("Average Distortion: ", avgD)



main()
#main2()



