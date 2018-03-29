import csv
import numpy
from sklearn.linear_model import LinearRegression


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
        numpy.array(winningTeamStats)
        numpy.array(losingTeamStats)

        tempWinningLosingStats = numpy.concatenate((winningTeamStats, losingTeamStats))
        tempLosingWinningStats = numpy.concatenate((losingTeamStats, winningTeamStats))


        if winningTeamId in self.teamStats and winningTeamId in self.played:
            self.teamStats[winningTeamId] = (self.teamStats[winningTeamId] * self.played[winningTeamId] + tempWinningLosingStats) / (self.played[winningTeamId] + 1)
            self.played[winningTeamId] += 1
        else:
            self.teamStats[winningTeamId] = tempWinningLosingStats
            self.played[winningTeamId] = 1

        if losingTeamId in self.teamStats and losingTeamId in self.played:
            self.teamStats[losingTeamId] = (self.teamStats[losingTeamId] * self.played[losingTeamId] + tempLosingWinningStats) / (self.played[losingTeamId] + 1)
            self.played[losingTeamId] += 1
        else:
            self.teamStats[losingTeamId] = tempLosingWinningStats
            self.played[losingTeamId] = 1


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
    winningFeatures = [ game[field] for field in fieldFeatures[0:halfFeatures]]
    losingFeatures = [ game[field] for field in fieldFeatures[halfFeatures:]]

    winningTeamStats = [winningScore] + winningFeatures
    losingTeamStats = [losingScore] + losingFeatures

    return (game["Wteam"], game["Lteam"],winningTeamStats,losingTeamStats)




    
def main():

    # get the data from csv
    data = getRegularSeason()
    teamStats = getTeamStats(data[0])

    allSeasonsStats = {}
    for game in data:    
        season = game['Season']

        if season not in allSeasonsStats:
            allSeasonsStats[season] = SeasonStats()
            
        teamStats = getTeamStats(game)
        allSeasonsStats[season].addGameStat(teamStats[0], teamStats[1], teamStats[2], teamStats[3])

    #print(allSeasonsStats[2003].teamStats)
main()






            