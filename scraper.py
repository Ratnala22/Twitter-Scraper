from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

chromedriver_path=r"D:\chromedriver-win64\chromedriver-win64\chromedriver.exe"
service=Service(chromedriver_path)

# Add Chrome options to ignore SSL errors
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")

driver=webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://x.com/login")
time.sleep(3)

login=driver.find_element(By.XPATH,"//input[@type='text']")
login.send_keys("Enter your x account email ID")
login.send_keys(Keys.ENTER)

time.sleep(2)

username=driver.find_element(By.XPATH,"//input[@type='text']")
username.send_keys("your username")
username.send_keys(Keys.ENTER)

time.sleep(2)

password=driver.find_element(By.XPATH,"//input[@type='password']")
password.send_keys("Enter your password")
password.send_keys(Keys.ENTER)

time.sleep(5)

search_box=driver.find_element(By.XPATH,"//input[@aria-label='Search query']")
search_box.send_keys("Account Name you wanna scrape tweets from") #ex. Harkirat Singh
search_box.send_keys(Keys.ENTER)

time.sleep(3)

people=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div').click()

time.sleep(3)
profile=driver.find_element(By.XPATH,'//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/section/div/div/div[1]').click()

soup=BeautifulSoup(driver.page_source,'html.parser')
postings=soup.findAll("div",class_="css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-1udbk01 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim")

soup=BeautifulSoup(driver.page_source,'html.parser')
postings=soup.findAll("div",class_="css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-1udbk01 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim")
tweets=[]
while True:
    for post in postings:
        tweets.append(post.text)
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
    soup=BeautifulSoup(driver.page_source,'html.parser')
    postings=soup.findAll("div",class_="css-146c3p1 r-8akbws r-krxsd3 r-dnmrzs r-1udh08x r-1udbk01 r-bcqeeo r-1ttztb7 r-qvutc0 r-37j5jr r-a023e6 r-rjixqe r-16dba41 r-bnwqim")
    tweets2=list(set(tweets))
    if len(tweets2)>200:
        break

df = pd.DataFrame(tweets2, columns=["tweets"])
csv_file_path = "tweets.csv"  
df.to_csv(csv_file_path, index=False)
input("Press Enter to close...")
driver.quit()