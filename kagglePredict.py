import csv
import numpy
from sklearn.linear_model import LinearRegression


class SeasonStats:

    teamStats = []

    played = []

    def __init__(self,numTeams):
        self.teamStats = [[0]] *numTeams
        self.played = [0] *numTeams

    def addGameStat(self,winningTeamStats, losingTeamStats):
        


# this pulls all data from the regular season
# returns an array of games played
# each game is a dictionary where a key is the fieldname ie Wteam Wscore Lteam Lscore
def getRegularSeason():

    fileName = "./kaggleData/RegularSeasonDetailedResults.csv"

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







#gets the 28 features we want
def getTeamStats(game):
    # we want the stats starting after location and forth
    fieldFeatures = [ header for header in data[0]][7:]

    winningScore = game["Wteam"]
    losingScore = game["Lteam"]
    winningFeatures = [ game[field] for field in fieldFeatures[1:halfFeatures]]
    losingFeatures = [ game[field] for field in fieldFeatures[halfFeatures:]]

    winningTeamStats = [winningScore] + winningFeatures
    losingTeamStats = [losingScore] + losingFeatures

    return (winningTeamStats,losingTeamStats)




# this data transforms game results in to features and lables
# returns (X,Y)
# X is a list of lists
# each row contains a list of feautres
# Y is a list of integers, either +1/-1

def createXY(data):

    # we want the stats starting after location and forth
    fieldFeatures = [ header for header in data[0]][7:]
    

    # X is array of features, Y is array of results
    X = []
    Y = [] 


    # this data is weird, the data is winning team stats, losing team stats
    # so if +1 denotes team 1 wins, team 1 is the winning team, will always win
    # I split this up so I can flip the data in the second half, meaning:
    # losing team stats, winning team stats
    # so now -1 denotes team 2 is the winning team, but since we flipped it is now pointing to 
    half = int(len(data)/2)

    for game in data[0:half]:

        # assign location to a number +1 for home, -1 away, 0 for neutral
        if (game["Wloc"]=='H'):
            location = +1
        elif (game["Wloc"]=='A'):
            location = -1
        else:
            location = 0


        # each team has 13 fields, winning team first, losing team second
        # get the fields with features we want
        Xn = [ location ] + [ game[field] for field in fieldFeatures]

        X.append(Xn)
        Y.append(+1)


    
    
    for game in data[half:]:

        # assign location to a number +1 for home, -1 away, 0 for neutral
        if (game["Wloc"]=='H'):
            location = -1
        elif (game["Wloc"]=='A'):
            location = +1
        else:
            location = 0


        # each team has 13 fields, losing team first, winning team second
        halfFeatures = int((len(fieldFeatures) -1)/2) +1

        winningFeatures = [ game[field] for field in fieldFeatures[1:halfFeatures]]
        losingFeatures = [ game[field] for field in fieldFeatures[halfFeatures:]]

        Xn = [ location, game[fieldFeatures[0]] ] + losingFeatures  + winningFeatures

        X.append(Xn)
        Y.append(-1)

    return (X,Y)






    
def predict():

    # get the data from csv
    data = getRegularSeason()

    # split our data into 3/4s training, 1/4 testing
    trainAmount = int(0.75 * len(data))
    train = data[:trainAmount]
    test = data[trainAmount:]

    # format our data
    (xTrain,yTrain) = createXY(train)
    (xTest,yTest) = createXY(test)


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






            