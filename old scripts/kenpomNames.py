import csv
import json
import re



def cleanName(teamName):
    teamName = re.sub('\d+','',teamName)
    teamName = teamName.replace(' ','').lower()
    teamName=teamName.replace('ncstate','northcarolinast.')
    teamName=teamName.replace('uconn','connecticut')
    teamName=teamName.replace('miami','miamifl')
    teamName=teamName.replace('st.francis(bkn)','st.francisny')
    teamName=teamName.replace('st.francis(pa)','st.francispa')
    teamName=teamName.replace('miami(oh)','miamioh')
    teamName=teamName.replace('olemiss','mississippi')

    teamName=teamName.replace('state','st.')
    return teamName



file = './data/kenpom2018.json'
with open(file) as f:
    jsonString = f.readline()
    
    data = json.loads(jsonString)

fileName = './data/ESPN_NCAA_Dict.csv'

fields=[]
with open(fileName) as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    fields = headers+['kenpom']
    records =[]
    for row in reader:
        data = {}
        for h in headers:
            data[h] = row[h]
        data['kenpom'] = cleanName(data['NCAA'])
        records.append(data)


outCsv = 'nameMap.csv'
with open(outCsv,'w') as f:
    csv = csv.DictWriter(f,fields)
    csv.writeheader()
    csv.writerows(records)
            
    
