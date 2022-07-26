import urllib.request
from bs4 import BeautifulSoup
# from PIL import Image, ImageFilter
# from io import BytesIO
# import requests
import re 
import json


def scrape(search_result):

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

    # url = "https://www.bing.com/images/search"

    # headers = {
    #     "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0"
    # }
    # params = {"q": {search_result}, "form": "HDRSC2", "first": "1", "scenario": "ImageBasicHover"}
    # r = requests.get(url, headers=headers, params=params)

    # soup = BeautifulSoup(r.text, "html.parser")
    # links = soup.find_all("div", {"class": "img_cont hoff"})
    # one_link = links[1:20]
    # one_link = re.search("(?P<url>https?://[^\s]+)", str(one_link)).group("url")  
    # img_object = requests.get(one_link, headers=headers)

    # img = Image.open(BytesIO(img_object.content))
    # d = img.resize((1125,1500))
    # d = d.filter(ImageFilter.GaussianBlur(5))
    # #d.show()
    # d.save(f'./images/{search_result}.png')

    filename = './data/results.json'
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


