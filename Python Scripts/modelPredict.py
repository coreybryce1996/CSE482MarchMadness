import csv
import json
import numpy
import re

from sklearn import linear_model
from sklearn import kernel_ridge
from sklearn import svm
from sklearn import ensemble
from sklearn import cluster

#from sklearn.decomposition import PCA
from sklearn.neural_network import MLPClassifier

# !!!!!!!-------------------------------------------
'''
you can probably ignore this because I got mapping of team names between kenpom, espn, and ncaa mostly working
'''

'''
create X feature vector and Y labels for kenpom data
dictFeatures = train or test from kenpom
returns X where each row is a tuple of kenpom features; Y row is + if team1 won, - team2 won
'''
def createKenpomXY(dictFeatures,scores):

    X=[]
    Y=[]

    nameMap = createNameMap()
    
    for game in scores:
        
        
        try:
            t1Name = nameMap[game['team']]['kenpom']+game['season']
            t2Name = nameMap[game['opponent']]['kenpom']+game['season']

            t1 = dictFeatures[t1Name]
            t2 = dictFeatures[t2Name]
            t1S = int(game['teamscore'])
            t2S =int(game['oppscore'])

            loc = 0

            if game['location'] == 'V':
                loc = -1
            elif game['location'] == 'H':
                loc = 1


            Xn = getKenpomFeatures(t1)+getKenpomFeatures(t2)+(loc,)
            
            
            Yn=-1
            if t1S > t2S:
                Yn=+1
            
            

            
            X.append(Xn)
            Y.append(Yn)

        except:
            pass
            #print("error",t1Name, t2Name)
    
    return(X,Y)


'''
create X feature vector and Y labels for espn data
dictFeatures = train or test from espn
returns X where each row is a tuple of espn features; Y row is + if team1 won, - team2 won
'''
def createEspnXY(dictFeatures,scores):

    X=[]
    Y=[]
    nameMap = createNameMap()
    
    for game in scores:
        
        
        try:
            t1Name = nameMap[game['team']]['ESPN']+game['season']
            t2Name = nameMap[game['opponent']]['ESPN']+game['season']

            t1 = dictFeatures[t1Name]
            t2 = dictFeatures[t2Name]
            t1S = int(game['teamscore'])
            t2S =int(game['oppscore'])

            loc = 0

            if game['location'] == 'V':
                loc = -1
            elif game['location'] == 'H':
                loc = 1


            Xn = getEspnFeatures(t1)+getEspnFeatures(t2)+(loc,)
            

            Yn=-1
            if t1S > t2S:
                Yn=+1
            
            X.append(Xn)
            Y.append(Yn)

        except:
            pass
            #print("error",t1Name, t2Name)
    
    return(X,Y)

#END ignore










'''
This cleans up any rank information from kenpom
'''
def cleanName(teamName):
    # remove digits 
    teamName = re.sub('\d+','',teamName)
    # remove spaces
    teamName = teamName.replace(' ','').lower()
    return teamName

'''
This function reads from nameMap.csv, it creates a dictionary that maps NCAA team names to ESPN and Kenpom abbreviations / spelling
key = ncaa name
'''
def createNameMap():
    fileName = '../data/nameMap.csv'

    nameMap = {}
    with open(fileName) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        
        nameMap={}
        for row in reader:
            data = {}
            for h in headers:
                data[h] = row[h]
            
            nameMap[data['NCAA']]= data
    return nameMap

    
'''
create testing and training data from kenpom
takes in the years
returns two dictionaries
key = kenpom team name
'''
def getKenpomTrainTest(trainRange, testRange):
    ds = 'kenpom'
    test = {}
    train = {}


    for year in trainRange:
        
        file = '../data/%s%d.json' % (ds,year)
        

        with open(file) as f:
            jsonString = f.readline()

        
        data = json.loads(jsonString)
        for team in data:
            teamName = cleanName(team['Team']) + str(year)

            train[teamName] = team


    for year in testRange:
        
        file = '../data/%s%d.json' % (ds,year)
        

        with open(file) as f:
            jsonString = f.readline()
        
        data = json.loads(jsonString)
        for team in data:
            teamName = cleanName(team['Team']) + str(year)

            test[teamName] = team
    

    return(train,test)

'''
create testing and training data from espn bpi
takes in the years
returns two dictionaries
key = espn team name
'''
def getEspnTrainTest(trainRange, testRange):
    ds = 'espnBPI'
    test = {}
    train = {}


    for year in trainRange:
        
        file = '../data/%s%d.json' % (ds,year)
        

        with open(file) as f:
            jsonString = f.readline()

        
        data = json.loads(jsonString)
        for team in data:
            teamName = " ".join(team['TEAM'].split(' ')[:-1]) + str(year)

            train[teamName] = team


    for year in testRange:
        
        file = '../data/%s%d.json' % (ds,year)
        

        with open(file) as f:
            jsonString = f.readline()
        
        data = json.loads(jsonString)
        for team in data:
            teamName = " ".join(team['TEAM'].split(' ')[:-1]) + str(year)

            test[teamName] = team
    

    return(train,test)



'''
this gets the game information for every season
'''
def getGameScores(trainRange, testRange):

    trainScores=[]
    testScores=[]

    for year in trainRange:
        fileName = '../data/ncaa%d.csv' % year

        with open(fileName) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            
            for row in reader:
                data = {}
                for h in headers:
                    data[h] = row[h]
                data['season'] = str(year)
                
                trainScores.append(data)

    for year in testRange:
        fileName = '../data/ncaa%d.csv' % year

        with open(fileName) as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames
            
            for row in reader:
                data = {}
                for h in headers:
                    data[h] = row[h]
                data['season'] = str(year)
                
                testScores.append(data)

    return(trainScores,testScores)


'''
get a tuple of values from kenpom that we want
'''
def getKenpomFeatures(team):
    return (team['AdjEM'],team['AdjD']['value'],team['AdjO']['value'],team['AdjT']['value'],team['AdjEM-NCSOS']['value'],team['AdjEM-StrengthofSchedule']['value'],team['OppD']['value'],team['OppO']['value'],team['Luck']['value'])




'''
get a tuple of values from espn that we want
'''
def getEspnFeatures(team):
    change = 0 
    try:
        change = int(team['7-Day RK CHG'])
    except:
        pass

    return (team['BPI Off'],team['BPI Def'],team['BPI'],change)



'''
create X feature vector and Y labels for espn and kenpom data
espnFeatures = train or test from espn
kenpomFeatures = train or test from kenpom
scores = array of scores 
returns X where each row is a tuple of 2 team features; Y row is + if team1 won, - team2 won
'''
def createXY(espnFeatures,kenpomFeatures,scores):
    X=[]
    Y=[]
    # define a dictionary so we can map team names to data sources
    nameMap = createNameMap()
    
    for game in scores:
        
        
        try:
            #format names for espn ie  Michigan St.=> Michigan State2018
            t1espnName = nameMap[game['team']]['ESPN']+game['season']
            t2espnName = nameMap[game['opponent']]['ESPN']+game['season']
            #get the data from espn bpi features dictionary
            t1eFeatures = espnFeatures[t1espnName]
            t2eFeatures = espnFeatures[t2espnName]

            #format names for kenpom ie  Michigan St.=> michiganst.2018
            t1kenpomName = nameMap[game['team']]['kenpom']+game['season']
            t2kenpomName = nameMap[game['opponent']]['kenpom']+game['season']
            #get the data from kenpom features dictionary
            t1kFeatures = kenpomFeatures[t1kenpomName]
            t2kFeatures = kenpomFeatures[t2kenpomName]

            #get the game score 
            t1S = int(game['teamscore'])
            t2S = int(game['oppscore'])

            #create a feature for home, away, or neutral
            loc = 0
            if game['location'] == 'V':
                loc = -1
            elif game['location'] == 'H':
                loc = 1

            # create a tuple of ESPN team1 feature's, ESPN t2 F's, location, Kenpom t1 F's, Kenpom t2 F's 
            Xn = getEspnFeatures(t1eFeatures)+getEspnFeatures(t2eFeatures)+(loc,) + getKenpomFeatures(t1kFeatures)+getKenpomFeatures(t2kFeatures)
            
            # set the label
            
            Yn=-1
            if t1S > t2S:
                Yn=+1
            

            
            
            


            X.append(Xn)
            Y.append(Yn)

        except:
            pass
            #print("error",t1Name, t2Name)
    #pca = PCA(n_components=20)
    #pcs = pca.fit_transform(X)
    return(X,Y)



def main():
    
    trainRange = range(2016,2018)
    testRange = range(2018,2019)

    # get team information
    (kTrainDict,kTestDict) = getKenpomTrainTest(trainRange,testRange)
    (eTrainDict,eTestDict) = getEspnTrainTest(trainRange,testRange)


    # get games played
    (trainScores,testScores) = getGameScores(trainRange,testRange)

    # sort games by date
    trainScores.sort(key=lambda x: x['day']+x['month']+x['year'])
    testScores.sort(key=lambda x: x['day']+x['month']+x['year'])



    # create x and y for training and testing
    (xTrain,yTrain)=createXY(eTrainDict,kTrainDict,trainScores)
    (xTest,yTest)=createXY(eTestDict,kTestDict,testScores)
    '''
    # define a model
    model = linear_model.LinearRegression()
    # fit that model
    model.fit(xTrain,yTrain)
    # predict
    yPred = model.predict(xTest)
    '''
    L = 55
    
    model = MLPClassifier(hidden_layer_sizes=L, solver="lbfgs", max_iter=len(xTrain))
    #model = MLPRegressor(hidden_layer_sizes=2, solver="relu")
    #model = linear_model.LinearRegression()
    model.fit(xTrain,yTrain)
    yPred = model.predict(xTest)
    
    match=0

    for i in range(len(xTest)):
        game = testScores[i]
        
        #print(game['team'],game['opponent'],yPred[i],yTest[i])
        # count if prediction sign == actual result
        if(numpy.sign(yPred[i])==numpy.sign(yTest[i])):
            match+=1

    acc = match/len(xTest)
    print("accuracy:",acc)


main()