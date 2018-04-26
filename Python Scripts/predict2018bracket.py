import csv
import numpy
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
import json
import re


def getKenpomNames():
    fileName = '../teamsData/TeamSpellings.csv'
    names={}
    with open(fileName) as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            names[row['TeamID']]=row
             

    return names

def getTourney(fileName):


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

        stats = (team1Stats)+(team2Stats)

        '''
        try:
            xN = (team1Stats)+(team2Stats)
        except:
            print("breaking")
        '''
        
        
        #stats = numpy.array(team1Stats)-numpy.array(team2Stats)

        #xN = (location)+stats
        xN = stats


        X.append(xN)
        Y.append(yN)
    
    return (X,Y)

def getTourneyX(roundData,kenpomData):
    X = []

    for game in roundData:


        season = 2018
        team1id = game[0]
        team2id = game[1]
        

        
        team1Stats = list(kenpomData[str(season) +':'+str(team1id)].values())
        team2Stats = list(kenpomData[str(season) +':'+str(team2id)].values())
        stats = (team1Stats)+(team2Stats)
        xN = stats

        X.append(xN)

    return X


def createBracket(tournData,kenpomData,model):

    # note there are 5 rounds
    # first, 16, 8, 4, final

    #this will be a 2d array containing results from each
    games = [[]]

    games[0] = tournData.copy()

    
    # iterate over every round
    for rnd in range(6):
        games.append([])
        # create X vector for current round
        test = getTourneyX(games[rnd],kenpomData)
        # predict Y vector for current round
        predicted = model.predict(test)
        numGamesInRound=len(games[rnd])
        # iterate over the games
        for i in range(0,numGamesInRound,2):
            # create the next round matchup
            match = [0,0,0]

            #select winner of game
            if numpy.sign(predicted[i])==1:
                match[0] = games[rnd][i][0]
            else:
                match[0] = games[rnd][i][1]
            games[rnd][i][2]= predicted[i]

            if(numGamesInRound!=1):
                #select winner of other game
                if numpy.sign(predicted[i+1])==1:
                    match[1] = games[rnd][i+1][0]
                else:
                    match[1] = games[rnd][i+1][1]
                games[rnd][i+1][2]= predicted[i+1]
                #add this matchup to the next round data
            games[rnd+1].append(match)
            
        
        
    kenpomNames = getKenpomNames()

    for rnd in range(6):
        print("Round",rnd+1)
        for game in games[rnd]:

            #print(str(game[0])+','+str(game[1]))
            
            team1Name = kenpomNames[str(game[0])]["TeamNameSpelling"]
            team2Name = kenpomNames[str(game[1])]["TeamNameSpelling"]

            if(numpy.sign(game[2])==1):
                print(team1Name, "beats",team2Name, "by", numpy.abs(game[2]))
            else:
                print(team2Name, "beats",team1Name, "by", numpy.abs(game[2]))
            
        print("")





def formatFirstRound(gameData):

    fRound = []

    for game in gameData[:32]:
        match = [game["WTeamID"],game["LTeamID"],0]
        fRound.append(match)

    return fRound



    
def main():

    # get the data from csv
    trainTournData = getTourney("../tournamentData/TourneyCompactResults.csv")
    testTournData = getTourney("../tournamentData/2018FirstRound.csv")
    oldKenpomData = getKenpomData('../season_teamid_kenpom.csv')
    curKenpomData = getKenpomData('../regularSeasonData/kenpom2018stats.csv')
    formattedTourn = formatFirstRound(testTournData)



    

    # format our data
    (xTrain,yTrain) = createTourneyXY(trainTournData,oldKenpomData)

    # create our model
    model = LinearRegression()
   
    # fit our model using training data
    model.fit(xTrain,yTrain)
    # run the model on our data

    createBracket(formattedTourn,curKenpomData,model)
    

    
main()






            