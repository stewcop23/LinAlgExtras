from bs4 import BeautifulSoup
import requests
import json

url = input("Input playlist URL: ")

r = requests.get(url)

soup = BeautifulSoup(r.content,"html.parser")

for script in soup.find_all('script'):
    if "var ytInitialData" in str(script):
        parts = script.text.split(" ")[3:]

line = ""

for part in parts:
    line += part + " "

line = line[0:-2] # there's an extra space and a semicolon


info = json.loads(line)

video_list = info['contents']['twoColumnBrowseResultsRenderer']['tabs'][0]['tabRenderer']['content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['playlistVideoListRenderer']['contents']

ids = []
youtubers = []
titles = []

for video in video_list:
    titles.append(video['playlistVideoRenderer']['title']['runs'][0]['text'])
    youtubers.append(video['playlistVideoRenderer']['shortBylineText']['runs'][0]['text'])
    ids.append(video['playlistVideoRenderer']['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'])
    
with open("output.txt","w") as file:
    for i,id in enumerate(ids):
        text = f"[{youtubers[i]} | {titles[i]}](https://www.youtube.com{id})"
        file.write(f"{text}\n")
        print(f"{text}")