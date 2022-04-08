# -*- coding: utf-8 -*-

#Take the HoR session links and manipulate them into the html-friendly link

import pandas as pd

df=pd.read_csv("session_links.csv")

type(df)
len(df)

newlist=[]

for x in range(len(df)):
    start_link=df.iloc[x][0]
    print('start link: ', start_link)
    temp=start_link.replace('Votes', 'Votes/MemberVotes')
    final_link=temp+'&page=1'
    print('final link: ', final_link)
    newlist.append(final_link)
    
#append corrected links to original df
df['Corrected Links']=newlist
df.head()

#export to new csv file
df.to_csv('corrected_links.csv')


