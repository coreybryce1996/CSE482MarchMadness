import json
import re

for year in range(2008,2019):
    eFile = "./data/espnBPI%d.json" % year

    with open(eFile) as f:
        jsonString = f.readline()
    
    eData = json.loads(jsonString)

    kFile = "./data/kenpom%d.json" % year

    with open(kFile) as f:
        jsonString = f.readline()
    
    kData = json.loads(jsonString)

    data =[]
    eDict ={}
    for eTeam in eData:
        teamName = "".join(eTeam['TEAM'].split(' ')[:-1]).lower()
        teamName=teamName.replace('ncstate','northcarolinast.')
        teamName=teamName.replace('uconn','connecticut')
        teamName=teamName.replace('miami','miamifl')
        teamName=teamName.replace('st.francis(bkn)','st.francisny')
        teamName=teamName.replace('st.francis(pa)','st.francispa')
        teamName=teamName.replace('miami(oh)','miamioh')
        teamName=teamName.replace('olemiss','mississippi')

        teamName=teamName.replace('state','st.')

        

        
        
        eDict[teamName]=eTeam

    for kTeam in kData:
        teamName = kTeam['Team'].split(' ')[0].lower()
        eTeam =eDict.get(teamName)
        if eTeam is  None:
            
            print('Not Found',teamName)
