#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep



playlist_URL = input("Enter the link of the playlist: ")

path = r"C:\seleniumDrivers\chromedriver.exe"
options = Options()
options.add_argument("--headless")
browser = webdriver.Chrome(executable_path = path, options = options)
browser.get(playlist_URL)
browser.maximize_window()


# In[22]:


sleep(10)
video_links = browser.find_elements(by=By.XPATH, value="//a[@class='yt-simple-endpoint inline-block style-scope ytd-thumbnail']")
video_links = [vlink.get_attribute("href") for vlink in video_links[1:]]

# stats = browser.find_element(by=By.ID, value='stats')
# stats = browser.find_element(by=By.XPATH, value="//div[@id ='stats'")

pt_title = browser.find_element(by=By.XPATH, value='//div[@class = "dynamic-text-container style-scope yt-dynamic-sizing-formatted-string"]').text


stats = browser.find_element(by=By.XPATH, value='//span[@class = "style-scope yt-formatted-string"]')
n_vid_str= stats.text
n_vid = 0
for i in list(n_vid_str):
    try:
        n = int(i)
        n_vid *=10
        n_vid += n
    except:
        continue

print("Title of the playlist: ", pt_title)
print("Total no. of videos: ", n_vid)


# In[23]:


print("==========Scrapping data==========")

idx = [i.text for i in browser.find_elements(by=By.XPATH, value="//div[@id ='index-container']")][-1]

s_time = 0
idl = []
while  int(idx) != n_vid:
    browser.execute_script("window.scrollBy(0,2000)","")
    idx = [i.text for i in browser.find_elements(by=By.XPATH, value="//div[@id ='index-container']")][-1]
    idl.append(idx)
    print(idx)
    if len(idl)>100:
        if idl[-1] == idl[-20]:
            break


# In[24]:


cmn_link_part = video_links[0][:-1:]
for i in range(len(video_links)+1, n_vid+1):
    video_links.append(cmn_link_part+str(i))

titles = [title.text for title in browser.find_elements(by=By.XPATH, value="//a[@id ='video-title']")]
times = browser.find_elements(by=By.XPATH, value="//span[@class ='style-scope ytd-thumbnail-overlay-time-status-renderer']")

time_list = [t.get_attribute("aria-label") for t in times]

data_dict = {'video_title':titles,
             'video_url':video_links[:int(idx)],
            'time_duration':time_list}

print("==========Finished Scrapping==========")


# In[25]:


spc = [r"/", "?", "+", "-", "&", "%", "$", "@", "!", "(", ")" ,"*", "|",
       "\\", "{", "}", ">", "<", ",", "~", "^"]

df = pd.DataFrame(data_dict)
for i in spc:
    pt_title = pt_title.replace(i, "_")
df.to_csv(pt_title+".csv", index=False)


# In[ ]:




