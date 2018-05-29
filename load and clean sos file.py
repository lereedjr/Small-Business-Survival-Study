# -*- coding: utf-8 -*-
"""
This script will load data, manipulate the data and train a model

Some code from 
https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8

"""

"""
packages
"""
import pandas as pd
import os
import numpy as np
import time


#from sklearn import preprocessing
#import matplotlib.pyplot as plt 
#plt.rc("font", size=14)
#from sklearn.linear_model import LogisticRegression
#from sklearn.cross_validation import train_test_split
#import seaborn as sns
#sns.set(style="white")
#sns.set(style="whitegrid", color_codes=True)


'''
This allows me to quickly create a year column in the array
'''
def theyear(strdate):                                                  
    return time.strptime(strdate, '%m/%d/%Y').tm_year

'''
This allows me to quickly create a year column in the array
'''
def themonth(strdate):                                                  
    return time.strptime(strdate, '%m/%d/%Y').tm_mon

def fivezip(ziplong):                                                  
    ziplong = str(ziplong)
    return ziplong[:5]


#import urllib.request
...

#I might use this for file acquisition
# Download the file from `url` and save it locally under `file_name`:
#urllib.request.urlretrieve(url, file_name)

"""
SET WORKING DIRECTORY
load the data with the dependent variable
"""
os.chdir("C:\\Users\\dave\\Desktop\\Class\\Data")
os.listdir()

sos_base_file = pd.read_csv("Business_Entities_in_Colorado.csv",parse_dates=True)
type(sos_base_file) #for my own edification on Pyhtn data types


#print(sos_base_file.shape)
#print(list(sos_base_file.columns))

'''
unique output values
'''
print("number of values in dep variable before transformation")
print(sos_base_file['entitystatus'].unique())

"""
Make the entity status binary
I use 1 to indicate business exists
I use 0 to indicate the business does not exist
"""
sos_base_file['entitystatus']=np.where(sos_base_file['entitystatus'] =='Good Standing',
             'Y', sos_base_file['entitystatus'])

sos_base_file['entitystatus']=np.where(sos_base_file['entitystatus'] =='Exists',
             'Y', sos_base_file['entitystatus'])

sos_base_file['entitystatus']=np.where(sos_base_file['entitystatus'] !='Y',
             'N', sos_base_file['entitystatus'])

sos_base_file['entitystatus'].unique() #test to see what values removed

'''
unique output values
'''
print("number of values in dep variable after transformation")
print(sos_base_file['entitystatus'].unique())



'''
Remove columns I do not think will add value
'''
del sos_base_file['principaladdress1']
del sos_base_file['principaladdress2']
del sos_base_file['mailingaddress1']
del sos_base_file['mailingaddress2']
del sos_base_file['agentfirstname']
del sos_base_file['agentmiddlename']
del sos_base_file['agentlastname']
del sos_base_file['agentorganizationname']
del sos_base_file['agentprincipaladdress1']
del sos_base_file['agentprincipaladdress2']
del sos_base_file['agentmailingaddress1']
del sos_base_file['agentmailingaddress2']

print(sos_base_file.shape)
#print(sos_base_file.head(10))


'''
create a column for the entity year and month
using a vector made this really fast
'''
sos_base_file['entityformdateyear'] = np.vectorize(theyear)(sos_base_file['entityformdate'])
sos_base_file['entityformdatemon'] = np.vectorize(themonth)(sos_base_file['entityformdate'])

'''
some zips have extra digits, it mucks up my joisn later
'''
sos_base_file['principalzipcode'] = np.vectorize(fivezip)(sos_base_file['principalzipcode'])



#sos_base_file['entityformdateyear'] = -1
#pd.to_datetime(sos_base_file['entityformdate'])
#sos_base_file['entityformdate'].dt.year

'''
Filter the data set to 2015-2016
Less years due to timing and other data sets
Too many recs for google api for example
I do this as a string of or. I could also use the year I created.
'''
sos_base_file = sos_base_file[sos_base_file['entityformdate'].str.contains("2016|2015")]

print(sos_base_file.shape)


'''
loop below no longer needed

create a year column
why not use the built in date functions?
well there is some wonky data

Also of note is pandas requires use of  the .loc function
straight assignment generates errors

This is also really slow 
'''
for i in sos_base_file.index:
    #sos_base_file['entityformdateyear'][i] = sos_base_file.entityformdate[i][-4:]
    #temp_year = int(sos_base_file.entityformdate[i][-4:])
    #sos_base_file.loc[sos_base_file.index[i], 'entityformdateyear'] = temp_year
    #sos_base_file.loc[sos_base_file.index[i], 'entityformdateyear'] = temp_year
    if i % 100000 == 0:
        print (i)
        #print(time.strptime(sos_base_file.entityformdate[i], '%m/%d/%Y').tm_year)
        #print(time.strptime(sos_base_file.entityformdate[i], '%m/%d/%Y').tm_mon)
        #print(sos_base_file['entityformdateyear'][i])
         #print(sos_base_file.entityformdate[i][-4:])
         #temp_year = sos_base_file.entityformdate[i][-4:]
         #print(temp_year)
         #print(type(int(temp_year)))
         #sos_base_file['entityformdateyear'][i] = i
         #sos_base_file.set_value(i,'entityformdateyear',temp_year)
        #sos_base_file.loc[sos_base_file.index[i], 'entityformdateyear'] = 1
        #print(sos_base_file['entityformdateyear'][i])

'''
get rid of the blank data
unsure if this will have an impact on the model
'''
sos_base_file.agentmailingcity = sos_base_file.agentmailingcity.fillna('X')
sos_base_file.mailingcity = sos_base_file.mailingcity.fillna('X')
sos_base_file.mailingstate = sos_base_file.mailingstate.fillna('X')
sos_base_file.mailingzipcode = sos_base_file.mailingzipcode.fillna('X')
sos_base_file.mailingcountry = sos_base_file.mailingcountry.fillna('X')
sos_base_file.agentmailingzipcode = sos_base_file.agentmailingzipcode.fillna('X')
sos_base_file.agentmailingcountry = sos_base_file.agentmailingcountry.fillna('X')


'''
check final layout
'''
print(sos_base_file.shape)
#print(sos_base_file.head(5))

'''
save my data to a local file
I can inspect manually
'''
file_name = 'finalsosdata.csv'
sos_base_file.to_csv(file_name, encoding='utf-8', index=False)

'''
one hot encode the data
'''
'''
#unneeded for now move to model later
cat_vars=['agentmailingzipcode']
for var in cat_vars:
    cat_list='var'+'_'+var
    print(cat_list)
    cat_list = pd.get_dummies(sos_base_file[var], prefix=var)
    sos_base_file1=sos_base_file.join(cat_list)
    sos_base_file=sos_base_file1
'''

print(sos_base_file.head(5))

'''
end sos data load and transform
'''









