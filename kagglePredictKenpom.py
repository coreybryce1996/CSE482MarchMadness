import csv
import numpy
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

import re





# this pulls all data from the regular season
# returns an array of games played
# each game is a dictionary where a key is the fieldname ie Wteam Wscore Lteam Lscore
def getRegularSeason():

    fileName = "./RegularSeasonDetailedResults.csv"

    data = []

    with open(fileName) as f:
        reader = csv.DictReader(f)
        

        for row in reader:
            game = {}

            # try to parse the data as an integer, otherwise string
            for field in reader.fieldnames:
                try:
                    value = int(row[field])
                except:
                    value = row[field]
                
                game[field] = value

            data.append(game)
    
    return data

def getTourney():

    fileName = "./TourneyCompactResults.csv"

    data = []

    with open(fileName) as f:
        reader = csv.DictReader(f)
        

        for row in reader:
            game = {}

            # try to parse the data as an integer, otherwise string
            for field in reader.fieldnames:
                try:
                    value = int(row[field])
                except:
                    value = row[field]
                game[field] = value

            data.append(game)
    
    return data


def getKenpomData(fileName):

    data = {}

    with open(fileName) as f:
        reader = csv.DictReader(f)
        

        for row in reader:
            game = {}

            key = row["Season"]+':'+row['TeamID']

            # try to parse the data as an integer, otherwise string
            for field in reader.fieldnames[2:]:
                try:
                    value = float(row[field])
                except:
                    value = row[field]
                game[field] = value
            data[key]=game
            
    
    return data






def createRegularXY(gameData, kenpomData):
     # X is array of features, Y is array of results
    X = []
    Y = [] 


    


    for i in range(len(gameData)):

        game = gameData[i]
        season = game["Season"]

    

        if (game["WLoc"]=='H'):
            location = -1
        elif (game["WLoc"]=='A'):
            location = +1
        else:
            location = 0

        if i %2 ==0:
            team1id = game["WTeamID"]
            team2id = game["LTeamID"]
            yN = game["WScore"] -game["LScore"]
            
        else:
            team2id = game["WTeamID"]
            team1id = game["LTeamID"]
            location *= -1
            yN = game["LScore"]-game["WScore"]
            

        try:
            team1Stats = list(kenpomData[str(season) +':'+str(team1id)].values())
            team2Stats = list(kenpomData[str(season) +':'+str(team2id)].values())
        except:
            continue

        
        try:
            xN = numpy.concatenate(([location],team1Stats,team2Stats))
        except:
            print("breaking")
        
        
        '''
        stats = numpy.array(team1Stats)-numpy.array(team2Stats)

        xN = (location)+stats
        '''


        X.append(xN)
        Y.append(yN)
    
    return (X,Y)

def createTourneyXY(gameData, kenpomData):
    # X is array of features, Y is array of results
    X = []
    Y = [] 


    


    for i in range(len(gameData)):

        game = gameData[i]
        season = game["Season"]

    

        if (game["WLoc"]=='H'):
            location = -1
        elif (game["WLoc"]=='A'):
            location = +1
        else:
            location = 0

        if i %2 ==0:
            team1id = game["WTeamID"]
            team2id = game["LTeamID"]
            yN = game["WScore"] -game["LScore"]
            #yN =1;
        else:
            team2id = game["WTeamID"]
            team1id = game["LTeamID"]
            location *= -1
            #yN= -1;
            yN = game["LScore"]-game["WScore"]

        try:
            team1Stats = list(kenpomData[str(season) +':'+str(team1id)].values())
            team2Stats = list(kenpomData[str(season) +':'+str(team2id)].values())
        except:
            continue

        '''
        try:
            xN = (team1Stats)+(team2Stats)
        except:
            print("breaking")
        '''
        
        
        stats = numpy.array(team1Stats)-numpy.array(team2Stats)

        xN = (location)+stats
        


        X.append(xN)
        Y.append(yN)
    
    return (X,Y)



    
def main():

    # get the data from csv
    data = getRegularSeason()
    tournData = getTourney()
    oldKenpomData = getKenpomData("./season_teamid_kenpom.csv")
    
    


    

    # format our data
    (X,Y) = createTourneyXY(tournData,oldKenpomData)
    #(X,Y) = createRegularXY(data,kenpomData)
    # split our data into 3/4s training, 1/4 testing
    trainAmount = int(0.75 * len(X))
    xTrain = X[:trainAmount]
    yTrain = Y[:trainAmount]
    xTest = X[trainAmount:]
    yTest = Y[trainAmount:]

    # create our model
    model = LinearRegression()
    
    # fit our model using training data
    model.fit(xTrain,yTrain)
    # run the model on our data
    yPredicted = model.predict(xTest)


    numCorrect = 0
    total = 0
    for i in range(len(xTest)):

        print("Predicted:",yPredicted[i],"Actual:",yTest[i])
        
        #if numpy.abs(yPredicted[i]) <5:
            # if class lables match
        if numpy.sign(yTest[i]) == numpy.sign(yPredicted[i]):
            numCorrect += 1
        total +=1

    accuracy = 1.0*numCorrect/total

    print("accuracy",accuracy)

    

    
main()






            