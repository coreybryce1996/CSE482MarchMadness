import csv
import numpy
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC

import re


class SeasonStats:

    teamStats = []

    played = []

    def __init__(self):
        #init a 2d array where each row has 28 team features

        # make it a dictionary
        self.teamStats = {} #numpy.zeros(numTeams,28)
        # init vector of zeros with length num teams
        self.played = {}#numpy.zeros(numTeams)

    def addGameStat(self,winningTeamId, losingTeamId, winningTeamStats, losingTeamStats):
        
        
        tempWinningLosingStats = numpy.concatenate((winningTeamStats, losingTeamStats))
        tempLosingWinningStats = numpy.concatenate((losingTeamStats, winningTeamStats))
        
        #tempWinningLosingStats = numpy.concatenate((winningTeamStats, []))
        #tempLosingWinningStats = numpy.concatenate((losingTeamStats,[]))

       
        if winningTeamId in self.teamStats and winningTeamId in self.played:
            if self.played[winningTeamId] == 22:
                self.teamStats[winningTeamId] = tempWinningLosingStats
                self.played[winningTeamId] = 1
            else:
                self.teamStats[winningTeamId] = (self.teamStats[winningTeamId] * self.played[winningTeamId] + tempWinningLosingStats) / (self.played[winningTeamId] + 1)
                self.played[winningTeamId] += 1
        else:
            self.teamStats[winningTeamId] = tempWinningLosingStats
            self.played[winningTeamId] = 1

        if losingTeamId in self.teamStats and losingTeamId in self.played:
            if self.played[losingTeamId] == 22:
                self.teamStats[losingTeamId] = tempLosingWinningStats
                self.played[losingTeamId] = 1
            else:
                self.teamStats[losingTeamId] = (self.teamStats[losingTeamId] * self.played[losingTeamId] + tempLosingWinningStats) / (self.played[losingTeamId] + 1)
                self.played[losingTeamId] += 1
        else:
            self.teamStats[losingTeamId] = tempLosingWinningStats
            self.played[losingTeamId] = 1


# this pulls all data from the regular season
# returns an array of games played
# each game is a dictionary where a key is the fieldname ie Wteam Wscore Lteam Lscore
def getRegularSeason():

    fileName = "../kaggleData/RegularSeasonDetailedResults.csv"

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

    fileName = "../kaggleData/Tourney Compact Results.csv"

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

def getTourneySeeds():

    fileName = "../kaggleData/Tourney Seeds.csv"

    data = []

    with open(fileName) as f:
        reader = csv.DictReader(f)
        

        for row in reader:
            game = {}

            # try to parse the data as an integer, otherwise string
            for field in reader.fieldnames:
                
                if field == "Seed":
                    value = int(re.search("\d+",row[field]).group(0))
                else:
                    value = int(row[field])
                game[field] = value

            data.append(game)
    
    return data






# gets the 28 features we want from a game
# returns winningID, LosingID, winningStats, losingStats

def getTeamStats(game):
    # we want the stats starting after location and forth
    
    fieldFeatures = [ header for header in game][8:]

    winningScore = game["Wscore"]
    losingScore = game["Lscore"]

    # each team has 13 fields, losing team first, winning team second
    halfFeatures = int(len(fieldFeatures)/2)
    winningFeatures = [ game[field] for field in fieldFeatures[0:halfFeatures]]
    losingFeatures = [ game[field] for field in fieldFeatures[halfFeatures:]]

    winningTeamStats = [winningScore] + winningFeatures
    losingTeamStats = [losingScore] + losingFeatures

    return (game["Wteam"], game["Lteam"],winningTeamStats,losingTeamStats)


def createRegularXYTrain(gameData):
    # X is array of features, Y is array of results
    X = []
    Y = [] 


    # this data is weird, the data is winning team stats, losing team stats
    # so if +1 denotes team 1 wins, team 1 is the winning team, will always win
    # I split this up so I can flip the data in the second half, meaning:
    # losing team stats, winning team stats
    # so now -1 denotes team 2 is the winning team, but since we flipped it is now pointing to 
    half = int(len(gameData)/2)

    for game in gameData[:half]:
        # assign location to a number +1 for home, -1 away, 0 for neutral
        if (game["Wloc"]=='H'):
            location = +1
        elif (game["Wloc"]=='A'):
            location = -1
        else:
            location = 0
        (wId,lId,wStats,lStats) = getTeamStats(game)

        Xn= numpy.concatenate(([location],wStats,lStats))
        X.append(Xn)
        Y.append(game["Wscore"]-game["Lscore"])
        

    for game in gameData[:half]:
        # assign location to a number +1 for home, -1 away, 0 for neutral
        if (game["Wloc"]=='H'):
            location = -1
        elif (game["Wloc"]=='A'):
            location = +1
        else:
            location = 0
        (wId,lId,wStats,lStats) = getTeamStats(game)

        Xn= numpy.concatenate(([location],lStats,wStats))
        X.append(Xn)
        Y.append(game["Lscore"]-game["Wscore"])

    return (X,Y)


def createRegularXY(gameData, seasonData):
    # X is array of features, Y is array of results
    X = []
    Y = [] 


    # this data is weird, the data is winning team stats, losing team stats
    # so if +1 denotes team 1 wins, team 1 is the winning team, will always win
    # I split this up so I can flip the data in the second half, meaning:
    # losing team stats, winning team stats
    # so now -1 denotes team 2 is the winning team, but since we flipped it is now pointing to 
    half = int(len(gameData)/2)

    for i in range(len(gameData)):

        game = gameData[i]
        season = game["Season"]

        if (game["Wloc"]=='H'):
            location = -1
        elif (game["Wloc"]=='A'):
            location = +1
        else:
            location = 0

        if i < half:
            team1id = game["Wteam"]
            team2id = game["Lteam"]
            yN = +1
        else:
            team2id = game["Wteam"]
            team1id = game["Lteam"]
            location *= -1
            yN = -1

        team1Stats = seasonData[season].teamStats[team1id]
        team2Stats = seasonData[season].teamStats[team2id]

        xN = numpy.concatenate(([location],team1Stats,team2Stats))

        X.append(xN)
        Y.append(yN)
    
    return (X,Y)

def createTourneyXY(gameData, seasonData,seeds):
    # X is array of features, Y is array of results
    X = []
    Y = [] 


    


    for i in range(len(gameData)):

        game = gameData[i]
        season = game["Season"]

        if season not in seasonData:
            continue

        if (game["Wloc"]=='H'):
            location = -1
        elif (game["Wloc"]=='A'):
            location = +1
        else:
            location = 0

        if i %2 ==0:
            team1id = game["Wteam"]
            team2id = game["Lteam"]
            yN = +1
        else:
            team2id = game["Wteam"]
            team1id = game["Lteam"]
            location *= -1
            yN = -1

        team1Stats = seasonData[season].teamStats[team1id]
        team2Stats = seasonData[season].teamStats[team2id]
        team1Seed = seeds[season][team1id]
        team2Seed = seeds[season][team2id]

        xN = numpy.concatenate(([location],team1Stats,[team1Seed],team2Stats,[team2Seed]))

        #xN = (location,team1Seed,team2Seed)

        X.append(xN)
        Y.append(yN)
    
    return (X,Y)



    
def main():

    # get the data from csv
    data = getRegularSeason()
    tournData = getTourney()
    seeds = getTourneySeeds()


    allSeasonsStats = {}
    for game in data:    
        season = game['Season']

        if season not in allSeasonsStats:
            allSeasonsStats[season] = SeasonStats()
            
        (wId,lId,wStats,lStats) = getTeamStats(game)
        allSeasonsStats[season].addGameStat(wId,lId,wStats,lStats)

    seasonSeeds = {}

    for seed in seeds:
        season = seed['Season']

        if season not in seasonSeeds:
            seasonSeeds[season] = {}
        
        seasonSeeds[season][seed['Team']]=seed['Seed']



    

    # format our data
    (X,Y) = createTourneyXY(tournData,allSeasonsStats,seasonSeeds)

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
    for i in range(len(xTest)):

        print("Predicted:",yPredicted[i],"Actual:",yTest[i])

        # if class lables match
        if numpy.sign(yTest[i]) == numpy.sign(yPredicted[i]):
            numCorrect += 1

    accuracy = 1.0*numCorrect/len(xTest)

    print("accuracy",accuracy)

    

    
main()






            