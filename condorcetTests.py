##condorcet tests
import random
def main():
    ballots = []
    exampleBallot = ["A","B","C","D","E"]
    allPairs = []
    for let in exampleBallot:
        for secondLet in exampleBallot:
            if let != secondLet:
                pair = (let,secondLet)
                allPairs.append(pair)
    ##print(allPairs)

    for i in range(10000):
        ball = ["E","A","B","C","D"]
        random.shuffle(ball)
        ballots.append(ball)
    for i in range(10000):
        newBallot = ["A","B","C","D","E"]
        random.shuffle(newBallot)
        ballots.append(newBallot)
    ##print(ballots)

    pairDict = {pair: 0 for pair in allPairs}
    ##print(pairDict)
    for ballot in ballots:
        #print(ballot)
        for indx in range(0,len(ballot)-1):
            for i in range(indx+1,len(ballot)):
                pair = (ballot[indx],ballot[i])
                #print(pair)
                pairDict[pair] += 1
    print(pairDict) 
    finalDict = {let: True for let in exampleBallot}
    for let in exampleBallot:
        for secondLet in exampleBallot:
            if let != secondLet:
                if pairDict[(let,secondLet)] < pairDict[(secondLet,let)]:
                    finalDict[let] = False
    print(finalDict)
    winnerExists = False
    for let in exampleBallot:
        if finalDict[let] == True:
            winnerExists = True
            print("The condorcet winnner is "+let+"!")
    if not winnerExists:
        print("There is no condorcet winner")
main()