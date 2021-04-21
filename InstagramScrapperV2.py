
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from bs4 import BeautifulSoup
import urllib
import os
from datetime import datetime

print ("Avoid using Chrome while this program is running\n")
username = input("Enter Instagram Username: ")
password = input("Enter Instagram Password: ")
url = input ("Enter Instagram Profile URL: ")
foldername = input("Enter the folder name for pictures: ")

initialTime = datetime.now()
path = r"C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
driver.get("https://www.instagram.com")


#Inputing username and password
def LoginInfo (username, password):
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).send_keys(username)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).send_keys(password)
    driver.find_element_by_xpath("""//*[@id="loginForm"]/div/div[3]/button""").click()
    time.sleep(5)

LoginInfo(username, password)
print ("\nLog in Successful\nCollecting Data...\n")

# Enter URL

#driver.get(url)
driver.get(url)
time.sleep(5)
#scrolling down

def scroll(y):
    for i in range (y):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)

#Getting Image Links
reached_page_end = False
last_height = driver.execute_script("return document.body.scrollHeight")
weblinks = []

while not reached_page_end:
    n=0
    source = BeautifulSoup(driver.page_source, "html.parser")
    for i in source.find_all('a', href = True):
        if i['href'].startswith('/p'):
            print("Link Found: https://www.instagram.com/{0}".format(i['href']))
            weblinks.append("https://www.instagram.com/"+i['href'])
    scroll(1)
    time.sleep(5)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if last_height == new_height:
        reached_page_end = True
    else:
        last_height = new_height

#removed duplicated links
editedWeblinks =[i for n, i in enumerate(weblinks) if i not in weblinks[:n]] 
print("\nThe total image link found: ", len(editedWeblinks))

#Estimated Time Completion
timeToComplete = (len(editedWeblinks)*6)/60
print("Time to download all images: ", timeToComplete, "minutes\n")

#Creating folder
parentDir = "C:/Picture/"
try:
    pathDir = os.path.join(parentDir, foldername)
    os.mkdir(pathDir)
    print ("\nThe folder is created in C:/Picture/" + foldername + '\n')
except OSError as error:
    print (error + "Failed to creted Folder: Folder Already Existed")




destinationA = parentDir + foldername + '/'+ foldername

def downloadImage(url1, num, destination):
    urlResource = urllib.request.urlopen(url1)
    imageName = destination+str(num)+'.jpg'
    with open(imageName, "wb") as output:
    #output = open(imageName, "wb")
        output.write(urlResource.read())
        output.close

driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL+'t')
num1 = 0
k = 0
for i,j in enumerate(editedWeblinks):
    #driver = webdriver.Chrome(path)
    try:
        driver.get(j)
        # LoginInfo(username,password)
        # driver.get(j)
        source2 = BeautifulSoup(driver.page_source, "html.parser")
        image_link = source2.find_all('div', {'class': 'KL4Bh'})[0].find_all('img')[0]['src']
        downloadImage(image_link, num1,destinationA)
        print("Photo#", str(num1), " Saved at ", destinationA+str(num1)+'.jpg')
        num1 +=1
        time.sleep(5)
    except:
        print ("Error Saving Image")
        continue
        
driver.quit()
print("Program Completed \nTotal Picture Saved =", i+1)
finalTime = datetime.now()
print ("Total Running Time: ", (finalTime - initialTime))

stop = input("Type any letters to stop")