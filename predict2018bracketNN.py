import csv
import numpy
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Perceptron
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPRegressor
import json
import re


def getKenpomNames():
    fileName = './TeamSpellings.csv'
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
            yN = [game["WScore"],game["LScore"]]
            #yN =1;
        else:
            team2id = game["WTeamID"]
            team1id = game["LTeamID"]
            location *= -1
            #yN= -1;
            yN = [game["LScore"],game["WScore"]]

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

    kenpomNames = getKenpomNames()


    # iterate over every round
    for rnd in range(6):
        games.append([])
        # create X vector for current round
        test = getTourneyX(games[rnd],kenpomData)
        # predict Y vector for current round
        predicted = model.predict(test)
        numGamesInRound=len(games[rnd])

        print('Round',rnd+1)

        # iterate over the games
        for i in range(0,numGamesInRound,2):
            # create the next round matchup

            index =i
            match = [0,0,0,0]

            t1Score,t2Score = predicted[index]

            if t1Score > t2Score:
                match[0] = games[rnd][index][0]
                
            else:
                match[0] = games[rnd][index][1]
            

            #print( kenpomNames[str(games[rnd][index][0])]["TeamNameSpelling"],'  ',kenpomNames[str(games[rnd][index][1])]["TeamNameSpelling"],'  ',t1Score,'  ',t2Score)
            games[rnd][index][2] = t1Score
            games[rnd][index][3] = t2Score


            if numGamesInRound > 1:
                index = i+1
                t1Score,t2Score = predicted[index]
                if t1Score > t2Score:
                    match[1] = games[rnd][index][0]
                else:
                    match[1] = games[rnd][index][1]
                games[rnd][index][2] = t1Score
                games[rnd][index][3] = t2Score
                #print( kenpomNames[str(games[rnd][index][0])]["TeamNameSpelling"],'  ',kenpomNames[str(games[rnd][index][1])]["TeamNameSpelling"],'  ',t1Score,'  ',t2Score)
            
            games[rnd+1].append(match)
        print()



            
            
            
        
        
    
    
    for rnd in range(6):
        print("Round",rnd+1)
        for game in games[rnd]:
           
            team1Name = kenpomNames[str(game[0])]["TeamNameSpelling"]
            team2Name = kenpomNames[str(game[1])]["TeamNameSpelling"]
            
            print(team1Name, game[2], team2Name, game[3])
            
            
        print("")
    




def formatFirstRound(gameData):

    fRound = []

    for game in gameData[:32]:
        match = [game["WTeamID"],game["LTeamID"],0,0]
        fRound.append(match)

    return fRound



    
def main():

    # get the data from csv
    trainTournData = getTourney("./TourneyCompactResults.csv")
    testTournData = getTourney("./2018FirstRound.csv")
    oldKenpomData = getKenpomData('./season_teamid_kenpom.csv')
    curKenpomData = getKenpomData('./kenpom2018stats.csv')
    formattedTourn = formatFirstRound(testTournData)



    

    # format our data
    (xTrain,yTrain) = createTourneyXY(trainTournData,oldKenpomData)

    # create our model
    #model = LinearRegression()
    model = MLPRegressor(hidden_layer_sizes=15)
   
    # fit our model using training data
    model.fit(xTrain,yTrain)
    # run the model on our data

    createBracket(formattedTourn,curKenpomData,model)

    print()
    

    
main()






            