from matplotlib import pyplot as plt
import json
import numpy

def main(file):
    
    topTeams = []
    bottomTeams = []
    nTeams = 21
    for year in range(2002,2019):
        
        file = "./data/kenpom%d.json" % year
        

        with open(file) as f:
            jsonString = f.readline()
        
        data = json.loads(jsonString)


        topTeams += data[:nTeams]

        bottomTeams += data[64-nTeams:64]
    

    efficiency=[float(team['AdjEM']) for team in topTeams]
    wins = [int(team['W-L'].split('-')[0]) for team in topTeams]
    
    plt.plot(efficiency,wins, 'g+')
    
    efficiency=[float(team['AdjEM']) for team in bottomTeams]
    wins = [int(team['W-L'].split('-')[0]) for team in bottomTeams]
    
    plt.plot(efficiency,wins, 'rx')

    '''
    x1 = [float(team['AdjO']['value']) for team in data]
    x2 = [float(team['AdjD']['value']) for team in data]
    plt.scatter(x1,x2)
    '''
    plt.show()

main("./data/kenpom2018.json")