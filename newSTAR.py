from numpy import random
import math
from vote import Vote
from election import Election
import time
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'summer-research-2023-bf67a99398ee.json'

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1M5cjRWLJ0Ef4CHCmB46yDDnxNB8-9zT5oipe4TT_W8s'

service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()

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
    #return "There is no ranked majority winner"

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
                if pairDict[(can,secondCan)] < pairDict[(secondCan,can)]:
                    finalDict[can] = False
    winnerExists = False
    for can in candidates:
        if finalDict[can] == True:
            winnerExists = True
            return can
    if winnerExists == False:
       return False

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
    #return "No outright scored majority winner"

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
                if pairDict[(can,secondCan)] < pairDict[(secondCan,can)]:
                    finalDict[can] = False
    winnerExists = False
    for can in candidates:
        if finalDict[can] == True:
            winnerExists = True
            return can
    if not winnerExists:
        return False
                      
""" def writeOut(voters,candidates,winners):
    inputfile = open("allTests.txt","r")
     """
def main():
    n = 10000
    m = 100
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
    """ winList = rankedWinners(voters, candidates) """
    starWinner = STAR(voters,candidates)
    
    winners = [pWinner,bWinner,cWinner,stvWinner,starWinner]
    print("**** The optimal candidate was: ****")
    print(OPTcandidate.id)
    print("The election winners by mechanism are:")
    print("Plurality: ",end="")
    print(pWinner.id)
    print("Borda: ",end="")
    print(bWinner.id)
    print("Copeland: ",end="")
    print(cWinner.id)
    print("STV: ",end="")
    print(stvWinner.id)
    print("STAR: ",end="")
    #print(starWinner.id)
    starResult = None
    if starWinner:
        starResult = starWinner.id
    else:
        starResult = False
        
    sMajWinner = sMajorityCheck(voters,candidates)
    sMajResult = None
    print("**** The candidate who had the outright scoring majority is: ****")
    #print(sMajWinner)
    if sMajWinner:
        sMajResult = sMajWinner.id
    else:
        sMajResult = False
        
    sConWinner = sCondorcetCheck(voters,candidates)
    sConResult = None
    print("**** The candidate who beat every other candidate in a scored head to head is: ****")
    #print(sConWinner)
    if sConWinner:
        sConResult = sConWinner.id
    else: 
        sConResult = False
    print(sConResult)

    rMajResult = None
    print("**** The candidate who had the outright ranked majority is: ****")
    #print(rMaj)
    if rMaj:
        rMajResult = rMaj.id
    else: 
        rMajResult = False

    rConResult = None
    print("**** The candidate who beat every other candidate in a ranked head to head is: ****")
    print(rCon) 
    if rCon:
        rConResult = rCon.id
    else:
        rConResult = False


    insert_data_option = 'INSERT_ROWS' 

    
    test = [[OPTcandidate.id, pWinner.id, bWinner.id, cWinner.id, stvWinner.id, starResult, sMajResult, sConResult, rMajResult, rConResult, n, m]]

    print(test)




    request = sheet.values().append(spreadsheetId=SAMPLE_SPREADSHEET_ID, 
                                range="m=100!A2", valueInputOption="USER_ENTERED", insertDataOption=insert_data_option, body={"values":test}).execute() 
    
      

    """ winnerMixUp = False
    for win in winners:
        if OPTcandidate != win:
            winnerMixUp = True
    if winnerMixUp:
        vCoords = []
        for voter in voters:
             """

    
    
if __name__ == "__main__":
    for i in range(100):
        if i%50 == 0:
            time.sleep(30)
        else:

            print("Test #"+str(i+1))
            main()
            print()
            print("===============================")
            print()
