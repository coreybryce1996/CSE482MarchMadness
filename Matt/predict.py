from matplotlib import pyplot as plt
import json
import numpy

from sklearn import linear_model


def createTrainTest(testRange, trainRange,ds):

    topTeamsTest = []
    bottomTeamsTest = []

    topTeamsTrain = []
    bottomTeamsTrain = []

    nTeams = 21
    for year in testRange:
        
        file = './data/%s%d.json' % (ds,year)
        

        with open(file) as f:
            jsonString = f.readline()
        
        data = json.loads(jsonString)


        topTeamsTest += data[:nTeams]

        bottomTeamsTest += data[64-nTeams:64]

    for year in trainRange:
        
        file = './data/%s%d.json' % (ds,year)
        

        with open(file) as f:
            jsonString = f.readline()
        
        data = json.loads(jsonString)


        topTeamsTrain += data[:nTeams]

        bottomTeamsTrain += data[64-nTeams:64]

        return(topTeamsTrain,bottomTeamsTrain,topTeamsTest,bottomTeamsTest)

def main():
    '''
    file = "./data/espnBPI%d.json"
    (topTrain, botTrain, topTest,botTest)=createTrainTest(range(2008,2018),range(2018,2019),file)
    


    
    xpTrain=[(team['BPI Off'],team['BPI Def']) for team in topTrain]
    xnTrain=[(team['BPI Off'],team['BPI Def']) for team in botTrain]

    xpTest=[(team['BPI Off'],team['BPI Def']) for team in topTest]
    xnTest=[(team['BPI Off'],team['BPI Def']) for team in botTest]
    '''

    dataSource = "kenpom"
    (topTrain, botTrain, topTest,botTest)=createTrainTest(range(2002,2018),range(2018,2019),dataSource)

    xpTrain=[(team['AdjEM'],team['AdjD']['value'],team['AdjO']['value'],team['AdjT']['value'],team['AdjEM-NCSOS']['value'],team['AdjEM-StrengthofSchedule']['value'],team['OppD']['value'],team['OppO']['value'],team['Luck']['value']) for team in topTrain]
    xnTrain=[(team['AdjEM'],team['AdjD']['value'],team['AdjO']['value'],team['AdjT']['value'],team['AdjEM-NCSOS']['value'],team['AdjEM-StrengthofSchedule']['value'],team['OppD']['value'],team['OppO']['value'],team['Luck']['value']) for team in botTrain]

    xpTest=[(team['AdjEM'],team['AdjD']['value'],team['AdjO']['value'],team['AdjT']['value'],team['AdjEM-NCSOS']['value'],team['AdjEM-StrengthofSchedule']['value'],team['OppD']['value'],team['OppO']['value'],team['Luck']['value']) for team in topTest]


    xTrain = xnTrain+xpTrain
    yTrain = [-1 for i in xnTrain]+[1 for i in xpTrain]

    #xTest = xnTest+xpTest
    #yTest = [-1 for i in xnTest]+[1 for i in xpTest]
    xTest = [xpTest[0], xpTest[3]]

    

    regr = linear_model.LinearRegression()
    regr.fit(xTrain,yTrain)
    yPred = regr.predict(xTest)

    '''
    same=0
    for i in range(len(yPred)):
        yt= numpy.sign(yTest[i])
        yp= numpy.sign(yPred[i])
        print(yt,yp)
        if(yt==yp):
            same+=1
     print("accuracy",same/len(yPred))
    '''
    

    print(topTrain[0]['Team'], yPred[0])
    print(topTrain[1]['Team'], yPred[1])
        

   
        


    #plt.show()

main()