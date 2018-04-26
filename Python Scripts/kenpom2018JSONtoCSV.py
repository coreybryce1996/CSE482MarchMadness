import csv
import numpy
import json
import re

'''
get a tuple of values from kenpom that we want
'''
def getKenpomFeatures(team):
    return (team['AdjEM'],team['AdjO']['value'],team['AdjD']['value'],team['AdjT']['value'],team['Luck']['value'],team['AdjEM-StrengthofSchedule']['value'],team['OppO']['value'],team['OppD']['value'],team['AdjEM-NCSOS']['value'])


def getKenpomNames():
    fileName = '../teamsData/TeamSpellings.csv'
    names={}
    with open(fileName) as f:
        reader = csv.DictReader(f)
        for row in reader:
            
            names[cleanName(row['TeamNameSpelling'])]=row
             

    return names

'''
This cleans up any rank information from kenpom
'''
def cleanName(teamName):
    # remove digits 
    teamName = re.sub('\d+','',teamName).strip()
    teamName = teamName.replace(' ','').lower()
    teamName = teamName.replace('.','')
    return teamName


def parseKenpomJSON():
    
    file = '../data/kenpom2018.json'

    kenpomNames = getKenpomNames()
    

    with open(file) as f:
        jsonString = f.readline()

    
    data = json.loads(jsonString)

    with open('kenpom2018stats.csv','w') as f:
        c = csv.writer(f)
        c.writerow(["Season","TeamID","AdjEM","AdjO","AdjD","AdjT","Luck","AdjEMss","OppOss","OppDss","AdjEMnc"])

        for team in data:
            teamName = cleanName(team['Team'])
            try:
                teamID = kenpomNames[teamName]["TeamID"]
                stats = getKenpomFeatures(team)
                c.writerow( (2018,teamID)+(stats))
            except:
                print(teamName)

parseKenpomJSON()


