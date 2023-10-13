from numpy import random
import math
from vote import Vote
from election import Election
import os
""" import matplotlib.pyplot as plt """
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account


# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1M5cjRWLJ0Ef4CHCmB46yDDnxNB8-9zT5oipe4TT_W8s'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

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
    stvTie = election.isTie
    return winner, stvTie

def pluralityVeto(ballots):
    points = {}
    for ballot in ballots:
        if ballot[0] in points:
            points[ballot[0]] += 1
        else:
            points[ballot[0]] = 1
    k = -1
    numToRemove = len(points) - 1
    while numToRemove>0:
        for ballot in ballots:
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

def getBallots(voters, candidates):
    ballots = []
    for voter in voters:
        distances = {}
        for candidate in candidates:
            distance = abs(voter.x - candidate.x)
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
    return False

def rCondorcetCheck(candidates,ballots):
    allPairs = []
    for can in candidates:
        for secondCan in candidates:
            if can != secondCan:
                pair = (can,secondCan)
                allPairs.append(pair)
    pairDict = {pair: 0 for pair in allPairs}
    for ballot in ballots:
        for indx in range(0,len(ballot)-1):
            for i in range(indx+1,len(ballot)):
                pair = (ballot[indx],ballot[i])
                pairDict[pair] += 1
    finalDict = {can: True for can in candidates}
    for can in candidates:
        for secondCan in candidates:
            if can != secondCan:
                if pairDict[(can,secondCan)] <= pairDict[(secondCan,can)]:
                    finalDict[can] = False
    for can in candidates:
        if finalDict[can] == True:
            return can
    return False

def rankedWinners(voters, candidates):
    ballots = getBallots(voters, candidates)
    pWinner = plurality(ballots)
    bWinner = borda(ballots)
    cWinner = copeland(ballots,candidates)
    stvWinner, stvTie = STV(ballots)
    pVetoWinner = pluralityVeto(ballots)
    rMajWinner = rMajorityCheck(voters,candidates,ballots)
    rConWinner = rCondorcetCheck(candidates,ballots)
    return pWinner, bWinner, cWinner, stvWinner, pVetoWinner, stvTie, rMajWinner, rConWinner

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
    return False

def sCondorcetCheck(voters,candidates):
    allPairs = []
    for can in candidates:
        for secondCan in candidates:
            if can != secondCan:
                pair = (can, secondCan)
                allPairs.append(pair)
    pairDict = {pair: 0 for pair in allPairs}
    for voter in voters:
        ballot = voter.scores
        for can in candidates:
            for secondCan in candidates:
                if can != secondCan:
                    if ballot[can] > ballot[secondCan]:
                        pair = (can,secondCan)
                        pairDict[pair] += 1
    finalDict = {can: True for can in candidates}
    for can in candidates:
        for secondCan in candidates:
            if can != secondCan:
                if pairDict[(can,secondCan)] <= pairDict[(secondCan,can)]:
                    finalDict[can] = False
    for can in candidates:
        if finalDict[can] == True:
            return can
    return False
                      
def writeOut(voters,candidates,normal=True,errorList=False,winners=False,criteria=False,distortions=False,stvTie=False):
    n = len(voters)
    m = len(candidates)
    inputfile = open("1D_metricTests.txt","r+",encoding='UTF-8')
    file = inputfile.read()
    lines = file.split("\n")
    testNum = 0
    for line in lines:
        if line[0:4]=="Test":
            words = line.split()
            testNum = words[1]
    nextTest = int(testNum)+1
    inputfile.write("Test: "+str(nextTest)+"\n")
    inputfile.write("There were "+str(n)+" voters and "+str(m)+" candidates\n")
    if normal:
        inputfile.write("Every method found the optimal candidate and met all criteria\n")
    else:
        vCoords = []
        cCoords = []
        for can in candidates:
            coords = str(can.x)
            cCoords.append(coords)
        for voter in voters:
            coords = str(voter.x)
            vCoords.append(coords)
        for error in errorList:
            if error:
                inputfile.write(error+"\n")
        inputfile.write("Voter Coordinates: ")
        for coords in vCoords:
            inputfile.write(coords+";")
        inputfile.write("\nCandidate Coordinates: ")
        for coords in cCoords:
            inputfile.write(coords+";")
        inputfile.write("\nOptimal Candidate: "+str(winners[0].id)+"\n")
        inputfile.write("Plurality (winner,distortion): "+str(winners[1].id)+", "+str(distortions[0])+"\n")
        inputfile.write("Borda (winner,distortion): "+str(winners[2].id)+", "+str(distortions[1])+"\n")
        inputfile.write("Copeland (winner,distortion): "+str(winners[3].id)+", "+str(distortions[2])+"\n")
        if winners[4]:
            inputfile.write("STV (winner,distortion): "+str(winners[4].id)+", "+str(distortions[3])+"\n")
        else:
            inputfile.write("STV: It was a tie\n")
        if stvTie:
            inputfile.write("There was a tie somewhere in the STV election\n")
        if winners[5]:
            inputfile.write("STAR (winner,distortion): "+str(winners[5].id)+", "+str(distortions[4])+"\n")
        else:
            inputfile.write("STAR: It was a tie\n")
        inputfile.write("Plurality-Veto (winner,distortion): "+str(winners[6].id)+", "+str(distortions[5])+"\n")

        if criteria[0]:
            inputfile.write("Ranked Majority: "+str(criteria[0].id)+"\n")
        else:
            inputfile.write("Ranked Majority: None\n")
        if criteria[1]:
            inputfile.write("Ranked Condorcet: "+str(criteria[1].id)+"\n")
        else:
            inputfile.write("Ranked Condorcet: None\n")
        if criteria[2]:
            inputfile.write("Scored Majority: "+str(criteria[2].id)+"\n")
        else:
            inputfile.write("Scored Majority: None\n")
        if criteria[3]:
            inputfile.write("Scored Condorcet: "+str(criteria[3].id)+"\n")
        else:
            inputfile.write("Scored Condorcet: None\n")
    inputfile.write("=========================================\n")
    inputfile.close()
    return nextTest

def writeStats(winners, criteria, distortion, totalTests, stvTie):
    
    
    """ inputfile = open("1D_metricTests.txt","r",encoding='UTF-8')
    file = inputfile.read()
    tests = file.split("=========================================")
    OPT = []
    PLUR = []
    PLURd = []
    BORD = []
    BORDd = []
    COPE = []
    COPEd = []
    STV = []
    STVd = []
    STAR = []
    STARd = []
    testNum = 0
    for test in tests[:-1]:
        lines = test.split("\n")
        lines.remove("")
        lines = lines[:-1]
        for line in lines:
            if line[0:5] == "Test:":
                testNum += 1
                print(testNum,end='')
    
    inputfile.close() """

##Function to create and save a graph whenever there is an interesting result
##Needs: currentTest, voters, candidates, winners
""" def plot(currentTest, voters, candidates, winners,fails):
    n = len(voters)
    m = len(candidates)
    filename = str(n)+"_"+str(m)+"_"+"Test"+currentTest
    origDir = "c:/Users/leocl/OneDrive/Documents/SSRI 2023/Plots/Distortion/"
    plotName = ""
    for fail in fails:
        if fail == fails[-1]:
            origDir += fail
            plotName += fail
        else:
            origDir += fail+"_"
            plotName += fail+"_"
    plotName += "Test #"+currentTest
    if not os.path.isdir(origDir):
        os.mkdir(origDir)
    origDir += "/"
    saveAs = origDir+filename
    voterX = []
    voterY = []
    candX = []
    candY = []
    for voter in voters:
        voterX.append(voter.x)
        voterY.append(voter.y)
    for candidate in candidates:
        candX.append(candidate.x)
        candY.append(candidate.y)
    optX = winners[0].x
    optY = winners[0].y
    pluX = winners[1].x
    pluY = winners[1].y
    borX = winners[2].x
    borY = winners[2].y
    copX = winners[3].x
    copY = winners[3].y
    if winners[4]:
        stvX = winners[4].x
        stvY = winners[4].y
    if winners[5]:
        staX = winners[5].x
        staY = winners[5].y

    plt.figure()
    plt.scatter(voterX,voterY,c = "cyan",s = 20,marker = '>', label = "Voters")
    plt.scatter(candX,candY,c = "navy",s = 25,label = "Candidates")
    plt.scatter([optX],[optY],c = "green",s = 150,label = "Optimal")
    plt.scatter([pluX],[pluY],c = "red",s = 125,label = "Plurality")
    plt.scatter([borX],[borY],c = "yellow",s = 100,label = "Borda")
    plt.scatter([copX],[copY],c = "orange",s = 75,label = "Copeland")
    if winners[4]:
        plt.scatter([stvX],[stvY],c = "pink",s = 50,label = "STV")
    if winners[5]:
        plt.scatter([staX],[staY],c = "black",s = 25,label = "STAR")
    plt.xlim(0,101)
    plt.ylim(0,101)
    plt.title(plotName)
    plt.legend()
    plt.savefig(saveAs)
    plt.close()
    plt.show() """

def main():
    n = 1000
    m = 15
    voters = []
    candidates = []
    for i in range(n):
        x = round(random.normal(50, 20), 1)
        voter = SVoter(x, i)
        voters.append(voter)

    for i in range(m):
        x = round(random.normal(50, 20), 1)
        candidate = SCandidate(x, i)
        candidates.append(candidate)

    minDistance = float('inf')
    OPTcanidate = candidates[0]
    for candidate in candidates:
        sumDistance = 0
        for voter in voters:
            distance = abs(voter.x - candidate.x)
            sumDistance += distance
        if sumDistance < minDistance:
            minDistance = sumDistance
            OPTcandidate = candidate

    pWinner,bWinner,cWinner,stvWinner,pVetoWinner,stvTie,rMaj,rCon = rankedWinners(voters, candidates)
    starWinner = STAR(voters,candidates)
    sMajWinner = sMajorityCheck(voters,candidates)
    sConWinner = sCondorcetCheck(voters,candidates)
    pSumDistance = 0
    bSumDistance = 0
    cSumDistance = 0
    stvSumDistance = 0
    starSumDistance = 0
    pVetoSumDistance = 0
    for voter in voters:
        pDistance = abs(voter.x - pWinner.x)
        pSumDistance += pDistance
        bDistance = abs(voter.x - bWinner.x)
        bSumDistance += bDistance
        cDistance = abs(voter.x - cWinner.x)
        cSumDistance += cDistance
        pVetoDistance = abs(voter.x - pVetoWinner.x)
        pVetoSumDistance += pVetoDistance
        if stvWinner:
            stvDistance = abs(voter.x - stvWinner.x)
            stvSumDistance += stvDistance
        if starWinner:
            starDistance = abs(voter.x - starWinner.x)
            starSumDistance += starDistance
    
    pDistortion = pSumDistance / minDistance
    bDistortion = bSumDistance / minDistance
    cDistortion = cSumDistance / minDistance
    pVetoDistortion = pVetoSumDistance / minDistance
    if stvWinner:
        stvDistortion = stvSumDistance / minDistance
        stvResult = stvWinner.id
    else:
        stvDistortion = False
        stvResult = False
    if starWinner:
        starDistortion = starSumDistance / minDistance
        starResult = starWinner.id
    else:
        starDistortion = False
        starResult = False

    distortions = [pDistortion,bDistortion,cDistortion,stvDistortion,starDistortion,pVetoDistortion]
    criteria = [rMaj,rCon,sMajWinner,sConWinner]
    winners = [OPTcandidate,pWinner,bWinner,cWinner,stvWinner,starWinner,pVetoWinner]
    """ print("There were "+str(n)+" voters and "+str(m)+" candidates") """

    errorList = [False,False,False,False]
    fails = []
    winnerMixUp = False
    for win in winners:
        if OPTcandidate != win:
            winnerMixUp = True
            errorList[0] = "At least one of the winners was not the optimal candidate"
    if winnerMixUp:
        fails.append("WinnerMixUp")
    tieExists = False
    if stvWinner==False or starWinner==False or stvTie==True:
        tieExists = True
        errorList[1] = "At least one of STV or STAR included a tie somewhere along the way"
        fails.append("TieExists")
    critFail = False
    for criterion in criteria:
        if criterion:
            for win in winners:
                if criterion != win:
                    critFail = True
                    errorList[2] = "At least one of the voting methods did not meet all avaliable criteria"
    if critFail:
        fails.append("CriteriaFail")
    noCondorcet = False
    if rCon==False or sConWinner==False:
        noCondorcet = True
        errorList[3] = "There was no condorcet winner for at least one of the condorcet tests"
        fails.append("NoCondorcet")
    if winnerMixUp or tieExists or critFail or noCondorcet:
        testNum = writeOut(voters,candidates,False,errorList,winners,criteria,distortions,stvTie)
        """ plot(str(testNum),voters,candidates,winners,fails) """
    else:
        writeOut(voters,candidates)  

    if rMaj:
        rMajResult = rMaj.id
    else:
        rMajResult = False
    if rCon:
        rConResult = rCon.id
    else:
        rConResult = False
    if sMajWinner:
        sMajResult = sMajWinner.id
    else:
        sMajResult = False
    if sConWinner:
        sConResult = sConWinner.id
    else:
        sConResult = False

    insert_data_option = 'INSERT_ROWS' 

    
    test = [[OPTcandidate.id,pWinner.id,pDistortion,bWinner.id,bDistortion,cWinner.id,cDistortion,
             stvResult,stvDistortion,starResult,starDistortion,pVetoWinner.id,pVetoDistortion,rMajResult,rConResult,sMajResult,sConResult,n,m,1]]

    print(test)

    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="Plurality-Veto!A3", valueInputOption="USER_ENTERED", insertDataOption=insert_data_option, body={"values":test}).execute() 
    
    
if __name__ == "__main__":
    for i in range(1000):
        main()
        time.sleep(0.75)