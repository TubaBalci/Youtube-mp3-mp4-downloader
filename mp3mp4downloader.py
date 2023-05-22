import requests
from bs4 import BeautifulSoup
from pytube import *
import os
import subprocess
import ffmpeg
import re

target = input("İndirilecek klasörün yolu:  \n\nExample:/home/developer/Desktop/musics/\n\n                         :")

sarki = input("Şarkı adını giriniz: ")

search_url = "https://www.youtube.com/results?search_query=r"+sarki
response = requests.get(search_url)
if response.status_code == 200:
    text = BeautifulSoup(response.content, "html.parser")
pattern = r'videoRenderer":{"videoId":"([^"]+)"'
video_ids = re.findall(pattern, str(text))
pattern =  r'<title>(.*?) - YouTube</title>'
songs = []
for i in range(10):
    title = requests.get("https://www.youtube.com/watch?v="+video_ids[i])
    title = BeautifulSoup(title.content, "html.parser")
    print(str(i+1)+" "+re.search(pattern,str(title)).group(1))
    songs.append(re.search(pattern,str(title)).group(1))  
secim = int(input("İndirilecek Müziği seçin: "))-1
isim = songs[secim]
sec = int(input("Video İçin  1\n\nMp3 İçin    2\n\n           :"))

def mp4(url,target, isim):
    command = [
        "yt-dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "-o", os.path.join(target, f"{isim}.mp4"),
        url
    ]

    subprocess.call(command)
    print("\nTAMAMLANDI\n")

def mp3(url,target,isim):
    command = [
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", os.path.join(target, f"{isim}.mp3"),
        url
    ]
    subprocess.call(command)
    print("\nTAMAMLANDI\n")

print (video_ids[secim]+"--"+target)
if sec == 1:
    mp4("https://www.youtube.com/watch?v="+video_ids[secim],target,isim)
elif sec == 2:
    mp3("https://www.youtube.com/watch?v="+video_ids[secim],target,isim)
else:
    print("Geçersiz format")        
