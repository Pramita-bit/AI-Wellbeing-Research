#import libraries
import pandas as pd
import numpy as np

#import file
responses = pd.read_csv('Responses 2 .csv')

#rename columns
responses.columns = ['Timestamp','Consent','Age','Gender','Location','Educational Level','Domain','AI Usage Frequency',
              'M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12','M13','M14','M15','M16','M17','M18','M19','M20',
              'T1','T2','T3',
              'V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12',
              'W1','W2','W3','W4','W5','W6','W7','W8','W9','W10','W11','W12']
pd.set_option('display.max_rows',None)


---------------------
# DATA CLEANING #
---------------------

#to check how many null values there are
responses.isnull().sum()

#dropping the null values
responses=responses.dropna()
responses=responses.reset_index(drop=True)

# cleaning Age column
responses.loc[1,'Age']=20
responses.loc[28,'Age']=20
responses.loc[55,'Age']=19
responses.loc[58,'Age']=26
responses.loc[115,'Age']=22
responses.loc[136,'Age']=29

# cleaning Location column
responses.loc[1,'Location']='Sodepur'
responses.loc[8,'Location']='Belghoria'
responses.loc[9,'Location']='Madhyamgram'
responses.loc[12,'Location']='Kolkata'
responses.loc[20,'Location']='Semi Urban'
responses.loc[23,'Location']='Kolkata'
responses.loc[25,'Location']='Ludhiana'
responses.loc[30,'Location']='Barasat'
responses.loc[35,'Location']='Howrah'
responses.loc[40,'Location']='Murshidabad'
responses.loc[47,'Location']='Barasat'
responses.loc[52,'Location']='Dumdum'
responses.loc[1,'Location']='Sodepur'
responses.loc[67,'Location']='Punjab'
responses.loc[69,'Location']='Newtown'
responses.loc[78,'Location']='Mumbai'
responses.loc[90,'Location']='Berhampur,Odisha'
responses.loc[91,'Location']='Nadia'
responses.loc[105,'Location']='Mumbai'
responses.loc[118,'Location']='Barasat'
responses.loc[120,'Location']='Barasat'
responses.loc[122,'Location']='Howrah'
responses.loc[123,'Location']='Amarkantak, Madhya Pradesh'
responses.loc[127,'Location']='Barrackpore'
responses.loc[129,'Location']='Jalpaiguri'
responses.loc[133,'Location']='Kolkata'
responses.loc[136,'Location']='Naihati'
responses.loc[137,'Location']='Barasat'


----------------------------
# DATA STANDARDIZATION #
----------------------------

# standardizing gender categories
responses['Gender']=responses['Gender'].str.replace('Female','Woman')
responses['Gender']=responses['Gender'].str.replace('Male','Man')
responses['Gender']=responses['Gender'].str.replace('Non-binar','Non-binary')

# standardizing location categories
def map_state(city):
    city=city.lower().strip()
    wb=['Kolkata','kolkata','Barasat','Belghoria','Sodepur','Howrah','Dumdum','Nadia','Naihati','Madhyamgram','Siliguri','Semi Urban','India','Jadavpur',
       'Chandannagar','Murshidabad','Chatgpt, Gemini','Salugara','Diamond Harbour','Haldia','Newtown','Ranaghat','Darjeeling','Chandmari Darjeeling',
       'Shyamnagar','Barrackpore',
       'Kankinara','Kalimpong','Kanchrapara','Halisahar','Jalpaiguri','Chinsurah','Saltlake , Sector - 1, Kolkata - 700064 Ae Block']
    bh=['Patna']
    pn=['Ludhiana','Ludhaina','chandigarh']
    mh=['kanchan','mumbai']
    kn=['bangalore']
    sk=['Majitar, East Sikkim','gangtok']
    jh=['ranchi']
    od=['Berhampur,Odisha']
    kl=['Keralam']
    up=['noida']
    dl=['New Delhi']
    mp=['Amarkantak, Madhya Pradesh']
    ap=['visakhapatnam']
        
    wb=[x.lower()for x in wb]
    bh=[x.lower()for x in bh]
    pn=[x.lower()for x in pn]
    mh=[x.lower()for x in mh]
    kn=[x.lower()for x in kn]
    sk=[x.lower()for x in sk]
    jh=[x.lower()for x in jh]
    od=[x.lower()for x in od]
    kl=[x.lower()for x in kl]
    up=[x.lower()for x in up]
    dl=[x.lower()for x in dl]
    mp=[x.lower()for x in mp]
    ap=[x.lower()for x in ap]
#condition    
    if city in wb:
        return'West Bengal'
    elif city in bh:
        return'Bihar'
    elif city in pn:
        return'Punjab'
    elif city in mh:
        return'Maharashtra'
    elif city in kn:
        return'Karnataka'
    elif city in sk:
        return'Sikkim'
    elif city in jh:
        return'Jharkhand'
    elif city in od:
        return'Odisha'
    elif city in kl:
        return'Kerala'
    elif city in up:
        return'Uttar Pradesh'
    elif city in dl:
        return'Delhi'
    elif city in mp:
        return'Madhya Pradesh'
    elif city in ap:
        return'Andhra Pradesh'
    else:
        return city.title()
#clean format
responses['Location']=responses['Location'].apply(map_state)

# standardizing Educational Domains based on broader categories
def map_domain(study):
    study=study.lower().strip()
    ss=['Psychology','Forensic science','Geography','Economics','Law','Sociology','BA psychology hons','Journalism','BSc Psychology',
        'Political Science','Political Science and International Relations','Bachelor of Arts (Political science)','Clinical Psychology',
       'Legal field','Psychology honours','Bsc.hons Psychology',"Master's in Education",'B.A. (Hons.) psychology','Rural Study',
        'Mass Communication','Psycholgy']    
    hm=['History','International relations','Design','English Honours','English Honors',
        'MA in English','English honours (B.A)','Humanities','Arts']
    ns=['Zoology','Mathematics','Physics','IMSC','Physics']
    md=['Medical','B pharm','Paramedics','Pharmacy','B.Pharm']
    et=['B.tech','Bachelor in Engeneering and Technology, CSE AI ML','Biotechnology','Computer Sc.','Electrical and Electronics Engineering',
        'Information technology','Computer Science & Engineering','engineering','Bsc computer science','B.Tech','BTech (CSE)','Computer',
        'Data science','Computer Applications','Mechanical','Civil Engineering','Computer Science','Computer science','BE-IT','CSE',
       'BCA','B.Tech Biotechnology','Btech cse','CyberSecurity','Engeneering','Btech','Computer Application']
    bc=['Sports Management','Mba','BBA','Management','Commerce','Business Administration','Commerce, Finance, Economics','BBA(HONS)','BBA LSCM',
       'management','Commerce, business and management','B.com(h)','MBA in hr','Finance','MBA in (Finance and Marketing)','Bba Hons']
    un=['Graduation','12tg','Nothing','Bsc','MA','College','12th pass','B.A.','19','B.A Hons','B.A']

    ss=[x.lower()for x in ss]
    hm=[x.lower()for x in hm]
    ns=[x.lower()for x in ns]
    et=[x.lower()for x in et]
    bc=[x.lower()for x in bc]
    un=[x.lower()for x in un]  
    md=[x.lower()for x in md]
#condition    
    if study in ss:
        return'Social Sciences'
    elif study in hm:
        return'Humanities'
    elif study in ns:
        return'Natural Sciences'
    elif study in et:
        return'Engineering & Technology'
    elif study in bc:
        return'Business & Commerce'
    elif study in md:
        return'Medical Sciences'
    elif study in un:
        return'Other'   
    else:
        return study.title()
#clean format
responses['Domain']=responses['Domain'].apply(map_domain)


------------------------
# DATA ELIMINATION #
------------------------

# eliminating responses adhering to the age constraint and saving the discarded data
responses['Age']=responses['Age'].astype(int)
dropped_item=responses[responses['Age']>25]
responses = responses[responses['Age']<=25].reset_index(drop=True)

# eliminating responses adhering to the location constraint and saving the discarded data
states=['West Bengal','Bihar','Punjab','Maharashtra','Karnataka','Sikkim','Jharkhand','Odisha',
        'Kerala','Uttar Pradesh','Delhi','Madhya Pradesh','Andhra Pradesh','Assam']
drop_loc =  responses[~responses['Location'].isin(states)]
responses = responses[responses['Location'].isin(states)].reset_index(drop=True)


--------------------
# VISUALIZATION #
--------------------

## AI Usage Frequency pie-chart

import matplotlib.pyplot as plt
#data to plot
labels= counts.index
sizes= counts.values
#create pie
plt.pie(sizes,labels=labels)
#perfect circle
plt.axis=('equal')
plt.show

## Participant distribution based on Gender pie chart

count_gender = responses['Gender'].value_counts()
labels = count_gender.index
size = count_gender.values
my_colors=['lightcoral','cornflowerblue','orange','grey']
#create pie
plt.pie(size,labels=labels,
        autopct='%1.1f%%',
        explode= (0.03,0.03,0.3,0.3),
        colors = my_colors)
plt.title('Distribution of Participants', fontsize=15, fontweight='bold')
plt.axis=('equal')
plt.show

## Participant distribution based on Educational Level pie chart

count_el = responses['Educational Level'].value_counts()
labels = count_el.index
size = count_el.values
my_colors=['yellow','purple','orange','grey']
#create pie
plt.pie(size,labels=labels,
        autopct='%1.1f%%',
        explode= (0.03,0.03,0.3,0.3),
        colors = my_colors)
plt.title('Distribution of Participants', fontsize=15, fontweight='bold')
plt.axis=('equal')
plt.show

## Participant distribution based on location horizontal bar graph

count_location = responses['Location'].value_counts()
states = count_location.index
frequency = count_location.values
# top 5 states
top5 = count_location.head(5)
others = count_location[5:].sum()
#ascending order
final_data = top5.copy()
final_data['Others'] = others
final_data = final_data.sort_values(ascending=True)
plt.figure(figsize=(6,4))
bars = plt.barh(final_data.index, final_data.values)
#create Bar-graph
plt.ylabel('States')
plt.xlabel('No. of Participants')
plt.title('Location of Participants', fontsize=15, fontweight='bold')
plt.bar_label(bars)
plt.tight_layout()
plt.show()
plt.savefig('Location of Participants.png') #saving as png

## Participant distribution based on Domian of Education horizontal bar graph

count_domain = responses['Domain'].value_counts()
study = count_domain.index
frequency = count_domain.values
#ascending order
final_data = count_domain.sort_values(ascending=True)
plt.figure(figsize=(6,4))
bars = plt.barh(final_data.index, final_data.values, color='darkgreen')
#create Bar-graph
plt.xlabel('No. of Participants')
plt.ylabel('Domains of Education')
plt.title('Educational Domains of Participants', fontsize=15, fontweight='bold')
plt.bar_label(bars)
plt.tight_layout()
plt.show()
plt.savefig('Educational Domains of Participants.png') #saving as png


--------------
# SCORING #
--------------

# Usage Scale items
scale1 = responses[['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12','M13','M14','M15','M16','M17','M18','M19','M20']]
# Trust scale items
scale2= responses[['T1','T2','T3']]
# Vigilance Scale Items
scale3= responses[['V1','V2','V3','V4','V5','V6','V7','V8','V9','V10','V11','V12']]
#reverse Scoring
responses['W11']= 6-responses['W11']
responses['W12']= 6-responses['W12']
# Well-being Scale items
scale4= responses[['W1','W2','W3','W4','W5','W6','W7','W8','W9','W10','W11','W12']]

# Calculating total scores of each participant
responses['Motive']=scale1.sum(axis=1)
responses['Trust']=scale2.sum(axis=1)
responses['Vigilance']=scale3.sum(axis=1)
responses['Well-being']=scale4.sum(axis=1)


-------------
# SAVING #
-------------

# saving the cleaned reverse scored data set 
responses.to_csv('cleaned_reverse.csv',index=False)


-------------
# REMARKS #
-------------

# Initial cleaning is completed.
#Initial number of participants = 153
#After cleaning, the number of participants = 143
#Discarded due to age = 9
#Discarded due to location = 1
