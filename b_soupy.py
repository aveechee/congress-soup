# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 2022

"""
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import re


url="https://clerk.house.gov/Votes/MemberVotes?CongressNum=117&Session=2nd&page=1"

page=requests.get(url)

soup=BeautifulSoup(page.content, 'html.parser')

#print(soup.prettify())

date=soup.find_all("div", class_="first-row row-comment")
chunk=soup.find_all("div", class_="role-call-vote")

#Lists
time_list=[]
congress=[]
rc_num_list=[]
rc_link_list=[]
bill_num_list=[]
bill_link_list=[]
vote_q_list=[]
bill_desc_list=[]
vote_type_list=[]
status_list=[]

#Extracts and cleans up the time/date for each bill
for time in date:
    time=time.get_text(strip=True)
    #print(time)
    time=re.sub(r'\s', "", time)
    time=time.split("|")
    print("time:")
    print(time[0])
    time_list.append(time[0])
    print("congress:")
    print(time[1])
    congress.append(time[1])


#Get the text of the RC Number
for i in chunk:
    rc_num=i.find("a")
    rc_num=rc_num.get_text()
    rc_num_list.append(rc_num)
    
#Extracts the rc link segments from each bill section
rc_base="https://clerk.house.gov"
for i in chunk:
    rc_link=i.find("a")
    rc_link=rc_link.get("href")
    rc_link=rc_base+rc_link
    print(rc_link)
    rc_link_list.append(rc_link)

#Get the text of the Bill Number
for i in chunk:
    bill_num=i.find("a", {"target":"_blank"})
    bill_num=bill_num.get_text()
    bill_num_list.append(bill_num)

#Extract the link to the bill content
for i in chunk:
    bill_link=i.find("a", {"target":"_blank"})["href"]
    print(bill_link)
    bill_link_list.append(bill_link)

#Get the text of 'Vote Question Type'
for i in chunk:
    vote_q=i.find("p", class_="roll-call-description")
    vote_q=vote_q.get_text().split(":")
    vote_q=vote_q[1]
    print(vote_q)
    vote_q_list.append(vote_q)
    
#Get the Bill Title & Description
for i in chunk:
    bill_desc=i.find("span", class_="billdesc")
    bill_desc=bill_desc.get_text()
    bill_desc_list.append(bill_desc)

#Get the type of vote
for i in chunk:
    vote_type=i.find_all("p", class_="roll-call-description")[2]
    vote_type=vote_type.get_text().split(":")
    vote_type=vote_type[1]
    print(vote_type)
    vote_type_list.append(vote_type)

#Get the Status of the vote
for i in chunk:
    status=i.find_all("p")[3]
    status=status.get_text().split(":")
    status=status[1]
    print(status)
    status_list.append(status)

#pagination-to fill in

#Create DataFrame for scraped elements
df=pd.DataFrame(list(zip(time_list, congress, rc_num_list, rc_link_list, 
                         bill_num_list, bill_link_list, vote_q_list, 
                         bill_desc_list, vote_type_list, status_list)), 
                columns=["Time", "Congress#", "rc_num", "rc_link",
                         "bill_num", "bill_link","vote_q", "bill_desc",
                         "vote_type", "status"])
                
#export to csv
df.to_csv('output.csv',index=False)








