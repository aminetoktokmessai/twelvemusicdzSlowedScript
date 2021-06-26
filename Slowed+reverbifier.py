import sys, io, os
from os.path import expanduser
import subprocess as sp
from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo
from pathlib import Path
import urllib
import urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from PIL.ImageQt import ImageQt
from selenium import webdriver
import time
from selenium.webdriver.support.ui import Select
import preview_thread, core, video_thread
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

songName = "example.mp3"
localFilePath = "C:\\Users\\ASUS\\Downloads\\"+songName
Path = "C:\\Users\\ASUS\\Downloads\\chromedriver.exe"
video_id = "ad-2sXcjrBs"
slowedPath = "C:\\Users\\ASUS\\Desktop\\slowed.mp4"

def upload(path):
    channel = Channel()
    channel.login("client_secrets.json","api key.txt")
    print("done")
    video = LocalVideo(path)
    video.set_title(songName[:-4]+" [S L O W E D + R E V E R B]")
    video.set_description("Check out our playlists & suggest songs to edit in the comments below")
    video.set_embeddable(True)
    video.set_privacy_status("private")
    video.set_public_stats_viewable(True)
    video = channel.upload_video(video)
    print(video.id)
    print(video)

def getThumbnail():
    try:
        driver.get("https://i.ytimg.com/vi/"+video_id+"/maxresdefault.jpg")
        img = driver.find_element_by_xpath('/html/body/img')
        src = img.get_attribute('src')
        time.sleep(1)
        urllib.request.urlretrieve(src, "thumbnail.jpg")
    except:
        driver.get("https://i.ytimg.com/vi/"+video_id+"/hqdefault.jpg")
        img = driver.find_element_by_xpath('/html/body/img')
        src = img.get_attribute('src')
        time.sleep(1)
        urllib.request.urlretrieve(src, "thumbnail.jpg")
    im = Image.open("thumbnail.jpg")
    enhancer = ImageEnhance.Brightness(im)
    im_output = enhancer.enhance(0.8)
    im_output.save('thumbnail.jpg')

def slowReverbify():
    driver.get("https://www.slowedreverb.com/")
    time.sleep(0.1)
    driver.find_element_by_id("file").send_keys(localFilePath)
    time.sleep(0.05)
    driver.find_element_by_xpath('//span[text()="Slower"]').click()
    time.sleep(0.1)
    driver.find_element_by_xpath('//span[text()="Submit"]').click()
    wait = WebDriverWait(driver, 60)
    while True:
        try :   
            wait.until(EC.visibility_of_element_located((By.XPATH,'//span[text()="Download"]'))).click()
            break
        except: continue
    tempfile = ""
    tempB = True
    while tempB:
        time.sleep(1)
        keyword = 'finished'
        for fname in os.listdir("C:\\Users\\ASUS\\Downloads"):
            if keyword in fname:
                print(fname[-3:])
                if fname[-3:]=="mp3":
                    print(fname, "has the keyword")
                    tempfile = fname
                    tempB = False
                    break
    p = sp.Popen('ffmpeg -r 1 -loop 1 -i thumbnail.jpg -i '+"C:\\Users\\ASUS\\Downloads\\"+tempfile+' -acodec copy -r 1 -shortest -vf scale=1280:720 C:\\Users\\ASUS\\Desktop\\slowed.mp4')
    (output, err) = p.communicate()
    p_status = p.wait()
    time.sleep(5)
    upload(slowedPath)
    print("done")
    os.remove("C:\\Users\\ASUS\\Downloads\\"+tempfile)
    os.remove("C:\\Users\\ASUS\\Desktop\\slowed.mp4")

try:
    driver = webdriver.Chrome(Path)
    getThumbnail()
    slowReverbify()
    pass
finally:
    driver.quit()
