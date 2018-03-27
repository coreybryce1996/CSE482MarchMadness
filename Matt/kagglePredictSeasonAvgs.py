import csv
import numpy
from sklearn.linear_model import LinearRegression


class SeasonStats:

    teamStats = []

    played = []

    def __init__(self,numTeams):
        #init a 2d array where each row has 28 team features
        self.teamStats = numpy.zeros(numTeams,28)
        # init vector of zeros with length num teams
        self.played = numpy.zeros(numTeams)

    def addGameStat(self,winningTeamId, losingTeamId, winningTeamStats, losingTeamStats):
        print("todo")


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







# gets the 28 features we want from a game
# returns winningID, LosingID, winningStats, losingStats

def getTeamStats(game):
    # we want the stats starting after location and forth
    
    fieldFeatures = [ header for header in game][8:]

    winningScore = game["Wscore"]
    losingScore = game["Lscore"]

    # each team has 13 fields, losing team first, winning team second
    halfFeatures = int(len(fieldFeatures)/2)
    winningFeatures = [ game[field] for field in fieldFeatures[1:halfFeatures]]
    losingFeatures = [ game[field] for field in fieldFeatures[halfFeatures:]]

    winningTeamStats = [winningScore] + winningFeatures
    losingTeamStats = [losingScore] + losingFeatures

    return (game["Wteam"], game["Lteam"],winningTeamStats,losingTeamStats)




    
def main():

    # get the data from csv
    data = getRegularSeason()
    getTeamStats(data[0])


main()






            