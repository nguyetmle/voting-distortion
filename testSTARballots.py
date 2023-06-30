import math
def main():
    voters = [5,7,13,45,8,82,97,23,33]
    cans = [("1",44),("2",67),("3",32),("4",7),("5",74)]
##    ballots = []
    voterNum = 1
    totalScores = {}
    for voter in voters:
        distances = {}
        minDis = 1000
        maxDis = 0
        for can in cans:
            distance = abs(voter-can[1])
            distances[can] = distance
            totalScores[can] = 0
            if distance >= maxDis:
                maxDis = distance
            if distance <= minDis:
                minDis = distance
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
        for can in cans:
            dis = distances[can]
            i = 0
            for score in scoringMatrix:
                if dis in score:
                    distances[can] = i
                    totalScores[can] += i
                i += 1
        sorted_list = sorted(distances, key = distances.get)
        sorted_dict = dict(sorted_list)
        print("Voter #"+str(voterNum)+"s ballot:")
        print(sorted_dict)
        voterNum += 1
    print()
    sorted_tot = sorted(totalScores, key = totalScores.get)
    finalScores = dict(sorted_tot)
    print("Final Scores:")
    print(finalScores)
main()
            
                
                
