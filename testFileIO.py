def test(voters,candidates,normal=True,errorList=False,winners=False,criteria=False):
    n = len(voters)
    m = len(candidates)
    inputfile = open("Test_IO.txt","r+",encoding='UTF-8')
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
    testList = ["First","Second","Third"]
    for item in testList:
        inputfile.write(item)
    if normal:
        inputfile.write("Every method found the optimal candidate and met all criteria\n")
    
    inputfile.close()

def main():
    voters = []
    candidates = []
    for i in range(25):
        voters.append(i)
    for i in range(5):
        candidates.append(i)
    
    errorList = ["There were too many apples","There were too many oranges",False]
    winners = ["2","3","2","4",""]
    test(voters,candidates)
main()