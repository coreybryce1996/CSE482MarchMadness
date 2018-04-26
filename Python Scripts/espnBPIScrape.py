import requests
import re
import sys
import json


def getTableFields(tableText):
    match = re.search("(<thead>).*?(?=</thead>)",tableText)
    headerText = match.group(0)

    fields = []
    columns = re.split("</th>",headerText)

    for column in columns:
        column+="</th>"
        # get text between tags
        text = "".join(re.findall("[^<>]+(?=[<])",column))
        if(text!=""):
            fields.append("".join(text))

    
    return (fields, tableText[match.end():])



def getTableData(tableText):
    match = re.search("(?<=<tbody>).*?(?=</tbody>)",tableText)
    bodyText = match.group(0)

    rows = re.findall("(?<=<tr>).*?(?=</tr>)",bodyText)
    
    data = []
    for row in rows:

        cols = re.split('/td>',row)

        values = []
        for col in cols:
            
            values.append( " ".join(re.findall("[^<>]+(?=[<])",col)))
            
        
        data.append(values)
       
    return data
    
def createDict(fields,data):
    dictData = []

    for team in data:
        record={}
        for i in range(len(fields)):
            try:
                value = float(team[i])
            except:
                    value = team[i]



            record[fields[i]]=value
        dictData.append(record)
    return dictData


    
def getContent(url):
    # download the webpage
    response = requests.get(url)
    
    # convert the response from bytes to string, remove new lines
    # regex needs everything to be on one line
    content = response.text
    #match everything between <table ...> and </table>, this includes <table ...>
    tableText = re.search("(<table.*>).*(?=</table>)",content).group(0)


    (fields,bodyText) = getTableFields(tableText)
    data = getTableData(bodyText)


    return createDict(fields,data)





def main():
    numPages = 15

    data = []
    for pageNum in range(1,numPages+1):
        url = 'https://www.espn.com/mens-college-basketball/bpi/_/view/bpi/page/%d' % pageNum
        pageData = getContent(url)
        for item in pageData:
            data.append(item)
    jsonString = json.dumps(data)

    with open('espnBPI.json','w') as f:
        f.write(jsonString)

main()