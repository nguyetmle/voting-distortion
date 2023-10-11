#Test matplotlib
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from numpy import random

def test():
    print("Test started")
    voterX = []
    voterY = []
    for i in range(150):
        x = random.randint(1,101)
        voterX.append(x)
        y = random.randint(1,101)
        voterY.append(y)
    candX = []
    candY = []
    for i in range(5):
        x = random.randint(1,101)
        candX.append(x)
        y = random.randint(1,101)
        candY.append(y)
    winnerIndx = random.randint(0,5)
    winnerX = candX[winnerIndx]
    winnerY = candY[winnerIndx]
    optIndx = random.randint(0,5)
    optX = candX[optIndx]
    optY = candY[optIndx]

    plt.figure()
    plt.scatter(voterX,voterY,c = "cyan",s = 24,marker = '>', label = "Voters")
    plt.scatter(candX,candY,c = "navy",s = 24,label = "Candidates")
    plt.scatter([optX],[optY],c = "green",s = 56,label = "Optimal")
    plt.scatter([winnerX],[winnerY],c = "red",s = 24, label = "Winner")
    plt.xlim(0,101)
    plt.ylim(0,101)

    plt.title("Testing the matplotlib scatter plot")
    plt.legend()
    plt.show()
    
def main():
    inputfile = open("Test99.txt","r",encoding='UTF-8')
    lines = inputfile.readlines()
    vCoords = lines[5].replace('Voter Coordinates: ','')
    vCoords = vCoords.replace('(','')
    vCoords = vCoords.replace(')','')
    vCoords = vCoords.replace(' ','')
    vCoords = vCoords.split(';')
    vCoords.remove('\n')
    vCoordsX = []
    vCoordsY = []
    for coords in vCoords:
        pair = coords.split(',')
        vCoordsX.append(float(pair[0]))
        vCoordsY.append(float(pair[1]))

    cCoords = lines[6].replace('Candidate Coordinates: ','')
    cCoords = cCoords.replace('(','')
    cCoords = cCoords.replace(')','')
    cCoords = cCoords.replace(' ','')
    cCoords = cCoords.split(';')
    cCoords.remove('\n')
    cCoordsX = []
    cCoordsY = []
    for coords in cCoords:
        pair = coords.split(',')
        cCoordsX.append(float(pair[0]))
        cCoordsY.append(float(pair[1]))

    optX = cCoordsX[2]
    optY = cCoordsY[2]
    pWinX = cCoordsX[0]
    pWinY = cCoordsY[0]
    bWinX = cCoordsX[2]
    bWinY = cCoordsY[2]
    cWinX = cCoordsX[0]
    cWinY = cCoordsY[0]
    stvX = cCoordsX[2]
    stvY = cCoordsY[2]
    starX = cCoordsX[2]
    starY = cCoordsY[2]
    plt.figure()
    plt.scatter(vCoordsX,vCoordsY,c = "cyan",s = 24,marker = '>', label = "Voters")
    plt.scatter(cCoordsX,cCoordsY,c = "navy",s = 24,label = "Candidates")
    plt.scatter([optX],[optY],c = "green",s = 150,label = "Optimal")
    plt.scatter([pWinX],[pWinY],c = "red",s = 125, label = "Plurality")
    plt.scatter([bWinX],[bWinY],c = "yellow",s = 100,label = "Borda")
    plt.scatter([cWinX],[cWinY],c = "orange",s = 75,label = "Copeland")
    plt.scatter([stvX],[stvY],c = "pink",s = 50, label = "STV")
    plt.scatter([starX],[starY],c = "black",s = 24,label = "STAR")
    plt.xlim(0,101)
    plt.ylim(0,101)

    plt.title("Example of election with no ranked condorcet winner - Test #99")
    plt.legend()
    plt.show()
    inputfile.close()
main()