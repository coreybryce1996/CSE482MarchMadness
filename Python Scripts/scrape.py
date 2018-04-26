import requests
import re
import sys
import json

def bytesToString(bytes):
    return "".join(map(chr,bytes))

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

    
    
    
    # return the headers and the text after the header
    return (fields[2:], tableText[match.end():])

def getTableData(fields, tableText):
    # The table is really weird and has multiple headers
    # matches is the html between the heads
    matches = re.findall("(?<=</thead>).*?(?=<thead>)",tableText)

    # array to hold all of the teams
    data = []

    # iterate over the text between headers
    for bodyText in matches:
        
        # each team is in a row, split by table row (tr)
        rows = re.split("</tr>",bodyText)
        
        # for each team, lets get the fields
        for row in rows:

            # get anything that is not an html tag
            values = re.findall("[^<>]+(?=[<])",row)
            
            try:
                # create a dict
                record = {}

                # lets map all of the values to the to their respective property name
                for index in range(len(fields)):
                    record[fields[index]]=values[index]

                # append the record
                data.append(record)
            except:
                pass
            
    return data




def main(url):
    # download the webpage
    response = requests.get(url)

    # convert the response from bytes to string, remove new lines
    # regex needs everything to be on one line
    content = bytesToString(response.content).replace('\n','')
    
    #content=content[0:1000]
    #print(re.sub('(\w+)=.*"','',content))

    #match everything between <table ...> and </table>, this includes <table ...>
    tableText = re.search("(<table.*>).*(?=</table>)",content).group(0)

    # remove any spaces 
    tableText = tableText.replace(' ','')

    # get the table fields, and the text following the first table head
    (fields,tableText) = getTableFields(tableText)
    
    # get data from the table
    data = getTableData(fields,tableText)
    
    # export as json
    export = json.dumps(data)
    print(export)

    
    

main(sys.argv[1])