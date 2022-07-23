import urllib.request
from bs4 import BeautifulSoup
import re 
import json

search_result = 'Bottle'

url = f'https://www.google.com/search?q={search_result}'


if ' ' in search_result:
    search_result_space = search_result.replace(' ', '+')
    url = f'https://www.google.com/search?q={search_result_space}'

 
request = urllib.request.Request(url)
request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
raw_response = urllib.request.urlopen(request).read()
html = raw_response.decode("utf-8")
soup = BeautifulSoup(html, 'html.parser')
element = soup.find("div", {"id": "result-stats"})
formatted1 = re.sub("\(.*?\)","()", element.get_text())
formatted2 = re.sub('\D', '', formatted1)
final_format = int(formatted2)


filename = './results.json'
dictObj = []

with open(filename) as fp:
    dictObj = json.load(fp)

if ' ' in search_result:
    search_result_dash = search_result.replace(' ', '-')
    if str(search_result_dash) not in dictObj:
        with open(filename,'r+') as file:
                dictObj = json.load(file)
                dictObj[str(search_result_dash)] = final_format
                file.seek(0)
                json.dump(dictObj, file, indent = 4)

    dictObj.update({search_result_dash: final_format,})

    with open(filename, 'w') as json_file:
        json.dump(dictObj, json_file, 
                            indent=4,  
                            separators=(',',': '))

else:
    if str(search_result) not in dictObj:
        with open(filename,'r+') as file:
                dictObj = json.load(file)
                dictObj[str(search_result)] = final_format
                file.seek(0)
                json.dump(dictObj, file, indent = 4)

    dictObj.update({search_result: final_format,})

    with open(filename, 'w') as json_file:
        json.dump(dictObj, json_file, 
                            indent=4,  
                            separators=(',',': '))