import csv
import numpy
from sklearn.linear_model import LinearRegression


class SeasonStats:

    teamStats = []

    played = []

    def __init__(self,numTeams):
        self.teamStats = [[0]] *numTeams
        self.played = [0] *numTeams

    def addGameStat(self,winningTeamId, losingTeamId, winningTeamStats, losingTeamStats):
        


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
    fieldFeatures = [ header for header in data[0]][7:]

    winningScore = game["Wscore"]
    losingScore = game["Lscore"]
    winningFeatures = [ game[field] for field in fieldFeatures[1:halfFeatures]]
    losingFeatures = [ game[field] for field in fieldFeatures[halfFeatures:]]

    winningTeamStats = [winningScore] + winningFeatures
    losingTeamStats = [losingScore] + losingFeatures

    return (game["Wteam"], game["Lteam"],winningTeamStats,losingTeamStats)




    
def main():

    # get the data from csv
    data = getRegularSeason()


main()






            