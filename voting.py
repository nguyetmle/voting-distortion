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
        # x = round(random.uniform(0, 100), 1)
        # y = round(random.uniform(0, 100), 1)
        # x = np.random.poisson(30)
        # y = np.random.poisson(30)
        x = round(random.normal(50, 20), 1)
        y = round(random.normal(50, 20), 1)
        voter = Voter(x, y, i)
        voters.append(voter)
    # for i in range(n//2):
    #      x = round(random.normal(20, 10), 1)
    #      y = round(random.normal(50, 20), 1)
    #      voter = Voter(x, y, i)
    #      voters.append(voter)
    # for i in range(n//2):
    #     x = round(random.normal(80, 10), 1)
    #     y = round(random.normal(50, 20), 1)
    #     voter = Voter(x, y, i)
    #     voters.append(voter)


    # for i in range(n//2):
    #     x = round(random.normal(20, 10), 1)
    #     y = round(random.normal(50, 20), 1)
    #     voter = Voter(x, y, i)
    #     voters.append(voter)

    # for i in range(n//2):
    #     x = round(random.normal(80, 10), 1)
    #     y = round(random.normal(50, 20), 1)
    #     voter = Voter(x, y, i)
    #     voters.append(voter)
        


    for i in range(m):
        # x = round(random.uniform(0, 100), 1)
        # y = round(random.uniform(0, 100), 1)
        # x = np.random.poisson(30)
        # y = np.random.poisson(30)
    # #     # x1 = np.random.normal(50,15, 2)
    # #     # x2 = np.random.normal(30, 15, 2)
    # #     # x = np.concatenate((x1, x2))
    # #     # x = np.vectorize(x3)
    # #     # y1 = np.random.normal(50,15, 2)
    # #     # y2 = np.random.normal(30, 15, 2)
    # #     # y = np.concatenate((y1, y2))
    # #     # y = np.vectorize(y3)
        x = round(random.normal(50, 20), 1)
        y = round(random.normal(50, 20), 1)
        candidate = Candidate(x, y, i)
        candidates.append(candidate)

    # for i in range(m//2):
    #     x = round(random.normal(20, 10), 1)
    #     y = round(random.normal(50, 20), 1)
    #     candidate = Candidate(x, y, i)
    #     candidates.append(candidate)

    # for i in range(m//2):
    #     x = round(random.normal(80, 10), 1)
    #     y = round(random.normal(50, 20), 1)
    #     candidate = Candidate(x, y, i)
    #     candidates.append(candidate)


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
    plt.scatter(voterX, voterY, c = "cyan", s = 24, label = "Voters")
    plt.scatter(candidateX, candidateY, c = "navy", s = 24, label = "Candidates")
    plt.scatter([OPT.x], [OPT.y], c = "green", s = 56, label = "OPT")
    plt.scatter([winner.x], [winner.y], c = "red", s = 24, label = "Winner")
    plt.xlim(0, 100)
    plt.ylim(0, 100)

    # plt.title(mechanism+" Voter and Candidate Metric Space")
    plt.title("Bimodal Distribution Voter and Candidate Metric Space")
    
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
    
    # mAvgDistortionPlurality = mDistortions[0]
    # mWorstDistortionPlurality = mDistortions[1]
    
    # mAvgDistortionBorda = mDistortions[2]
    # mWorstDistortionBorda = mDistortions[3]
    
    # mAvgDistortionCopeland = mDistortions[4]
    # mWorstDistortionCopeland = mDistortions[5]

    # mAvgDistortionSTV = mDistortions[6]
    # mWorstDistortionSTV = mDistortions[7]
    
    plt.figure()
    plt.plot(nArray, nAvgDistortionPlurality, c = "red", linestyle = "dotted", label = "Plurality Average Distortion")
    plt.plot(nArray, nWorstDistortionPlurality, c = "red", label = "Plurality Worst Case Distortion")

    plt.plot(nArray, nAvgDistortionBorda, c = "blue", linestyle = "dotted", label = "Borda Average Distortion")
    plt.plot(nArray, nWorstDistortionBorda, c = "blue", label = "Borda Worst Case Distortion")
    
    plt.plot(nArray, nAvgDistortionCopeland, c = "green", linestyle = "dotted", label = "Copeland Average Distortion")
    plt.plot(nArray, nWorstDistortionCopeland, c = "green", label = "Copeland Worst Case Distortion")

    plt.plot(nArray, nAvgDistortionSTV, c = "orange", linestyle = "dotted", label = "STV Average Distortion")
    plt.plot(nArray, nWorstDistortionSTV, c = "orange", label = "STV Worst Case Distortion")

    plt.xlabel("Number of Voters (n)")
    plt.ylabel("Distortion")
    plt.title("Normal Distortion vs. n (m = 10)")
    plt.legend()
    plt.show()

    # plt.figure()
    # plt.plot(mArray, mAvgDistortionPlurality, c = "red", linestyle = "dotted", label = "Plurality Average Distortion")
    # plt.plot(mArray, mWorstDistortionPlurality, c = "red", label = "Plurality Worst Case Distortion")

    # plt.plot(mArray, mAvgDistortionBorda, c = "blue", linestyle = "dotted", label = "Borda Average Distortion")
    # plt.plot(mArray, mWorstDistortionBorda, c = "blue", label = "Borda Worst Case Distortion")

    # plt.plot(mArray, mAvgDistortionCopeland, c = "green", linestyle = "dotted", label = "Copeland Average Distortion")
    # plt.plot(mArray, mWorstDistortionCopeland, c = "green", label = "Copeland Worst Case Distortion")

    # plt.plot(mArray, mAvgDistortionSTV, c = "orange", linestyle = "dotted", label = "STV Average Distortion")
    # plt.plot(mArray, mWorstDistortionSTV, c = "orange", label = "STV Worst Case Distortion")

    # new_list = range(math.floor(min(mArray)), math.ceil(max(mArray))+1)
    # plt.xticks(new_list)
    # plt.xlabel("Number of Candidates (m)")
    # plt.ylabel("Distortion")
    # plt.title("Bimodal Distortion vs. m (n = 4)")
    # plt.legend()
    # plt.show()

def plotCorrect(nArray, nCorrects):
    nCorrectP = nCorrects[0]
    nCorrectB = nCorrects[1]
    nCorrectC = nCorrects[2]
    nCorrectS = nCorrects[3]

    # mCorrectP = mCorrects[0]
    # mCorrectB = mCorrects[1]
    # mCorrectC = mCorrects[2]
    # mCorrectS = mCorrects[3]
    
    plt.figure()
    plt.plot(nArray, nCorrectP, c = "red", label = "Plurality")

    plt.plot(nArray, nCorrectB, c = "blue", label = "Borda")

    plt.plot(nArray, nCorrectC, c = "green", label = "Copeland")

    plt.plot(nArray, nCorrectS, c = "orange", label = "STV")

    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    plt.xlabel("Number of Voters (n)")
    plt.ylabel("% of Time OPT Chosen by Voting Mechanism")
    plt.title("Poisson Correct % vs. n (m = 4)")
    plt.legend()
    plt.show()

    # plt.figure()
    # plt.plot(mArray, mCorrectP, c = "red", label = "Plurality")

    # plt.plot(mArray, mCorrectB, c = "blue", label = "Borda")

    # plt.plot(mArray, mCorrectC, c = "green", label = "Copeland")

    # plt.plot(mArray, mCorrectS, c = "orange", label = "STV")

    # new_list = range(math.floor(min(mArray)), math.ceil(max(mArray))+1)
    # plt.xticks(new_list)
    # plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    # plt.xlabel("Number of Candidates (m)")
    # plt.ylabel("% of Time OPT Chosen by Voting Mechanism")
    # plt.title("Bimodal Correct % vs. m (n = 500)")
    # plt.legend()
    # plt.show()

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
    # n = 50
    # m = 20
    # rounds = 2000
    mechanisms = ["Plurality", "Borda", "Copeland", "STV"]

    nArray = [10,50,100,200,500,1000]
    # nArray = range(2, n + 1)
    nAvgDistortionPlurality = []
    nWorstDistortionPlurality = []
    nCorrectPlurality = []

    nAvgDistortionBorda = []
    nWorstDistortionBorda = []
    nCorrectBorda = []

    nAvgDistortionSTV = []
    nWorstDistortionSTV = []
    nCorrectSTV = []
    
    nAvgDistortionCopeland = []
    nWorstDistortionCopeland = []
    nCorrectCopeland = []

    for n in nArray:
        #print("n =", n)
        for mechanism in mechanisms:
            maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(2000, n, 10, mechanism)
            #print(correctPercent)
            if mechanism == "Plurality":
                nWorstDistortionPlurality.append(maxD)
                nAvgDistortionPlurality.append(avgD)
                nCorrectPlurality.append(correctPercent)
                
            elif mechanism == "Borda":
                nWorstDistortionBorda.append(maxD)
                nAvgDistortionBorda.append(avgD)
                nCorrectBorda.append(correctPercent)

            elif mechanism == "STV":
                nWorstDistortionSTV.append(maxD)
                nAvgDistortionSTV.append(avgD)
                nCorrectSTV.append(correctPercent)
                
            else:
                nWorstDistortionCopeland.append(maxD)
                nAvgDistortionCopeland.append(avgD)
                nCorrectCopeland.append(correctPercent)

    # mArray = [2,3,4,5,6,7,8,9,10,15,20]
    # # mArray = [10]
    # mAvgDistortionPlurality = []
    # mWorstDistortionPlurality = []
    # mCorrectPlurality = []

    # mAvgDistortionBorda = []
    # mWorstDistortionBorda = []
    # mCorrectBorda = []

    # mAvgDistortionCopeland = []
    # mWorstDistortionCopeland = []
    # mCorrectCopeland = []

    # mAvgDistortionSTV = []
    # mWorstDistortionSTV = []
    # mCorrectSTV = []
    
    # for m in mArray:
    #     #print("m =", m)
    #     for mechanism in mechanisms:
    #         maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(2000, 500, m, mechanism)

    #         if mechanism == "Plurality":
    #             mWorstDistortionPlurality.append(maxD)
    #             mAvgDistortionPlurality.append(avgD)
    #             mCorrectPlurality.append(correctPercent)
    #             # plot(voters, candidates, OPT, winner, mechanism)
                
    #         elif mechanism == "Borda":
    #             mWorstDistortionBorda.append(maxD)
    #             mAvgDistortionBorda.append(avgD)
    #             mCorrectBorda.append(correctPercent)
    #             # plot(voters, candidates, OPT, winner, mechanism)

    #         elif mechanism == "STV":
    #             mWorstDistortionSTV.append(maxD)
    #             mAvgDistortionSTV.append(avgD)
    #             mCorrectSTV.append(correctPercent)
    #             #plot(voters, candidates, OPT, winner, mechanism)
                
    #         else:
    #             mWorstDistortionCopeland.append(maxD)
    #             mAvgDistortionCopeland.append(avgD)
    #             mCorrectCopeland.append(correctPercent)
    #             # plot(voters, candidates, OPT, winner, mechanism)


    nDistortions = [nAvgDistortionPlurality, nWorstDistortionPlurality, nAvgDistortionBorda,
                    nWorstDistortionBorda, nAvgDistortionCopeland, nWorstDistortionCopeland,
                    nAvgDistortionSTV, nWorstDistortionSTV]
    
    # mDistortions = [mAvgDistortionPlurality, mWorstDistortionPlurality, mAvgDistortionBorda,
    #                 mWorstDistortionBorda, mAvgDistortionCopeland, mWorstDistortionCopeland,
    #                 mAvgDistortionSTV, mWorstDistortionSTV]


    # nCorrects = [nCorrectPlurality, nCorrectBorda, nCorrectCopeland, nCorrectSTV]
    # mCorrects = [mCorrectPlurality, mCorrectBorda, mCorrectCopeland, mCorrectSTV]
    
    # plot(voters, candidates, OPT, winner)
    
    plotDistortion(nArray, nDistortions)

    # plotCorrect(nArray, nCorrects)
    # plotCorrect(nArray, nCorrects)

def main2():

    vs = [500]
    cs = [8,9,10,15,20]
    # vs = [1000]
    # cs = [3]
    for i in vs:
        for j in cs:

            print("")
            print("Voters: ", i)
            print("Candidates: ", j)
            print("")

            print("Plurality")
            maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(2000, i, j, "Plurality")
            print("Percent Correct: ", correctPercent)
            # print("Winner: ",winner)
            print("Average Distortion: ", avgD)
            
            print("")
            print("STV")
            maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(2000, i, j, "STV")
            print("Percent Correct: ", correctPercent)
            # print("Winner: ",winner)
            print("Average Distortion: ", avgD)

            print("")
            print("Borda Count")
            maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(2000, i, j, "Borda")
            print("Percent Correct: ", correctPercent)
            # print("Winner: ",winner)
            print("Average Distortion: ", avgD)

            print("")
            print("Copeland")
            maxD, avgD, correctPercent, voters, candidates, OPT, winner = simulateRounds(2000, i, j, "Copeland")
            print("Percent Correct: ", correctPercent)
            # print("Winner: ",winner)
            print("Average Distortion: ", avgD)


main()
#main2()



