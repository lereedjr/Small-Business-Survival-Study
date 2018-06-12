# -*- coding: utf-8 -*-
"""
Created on Sat May 26 10:04:13 2018

@author: dave
"""

import pandas as pd
import os
from googleplaces import GooglePlaces, types, lang
import googlemaps
import numpy as np


'''
combine all addresses parts into one
'''
def fulladdr(str1,str2,str3,str4):
    full_str = str(str1) +' '+ str(str2) +' ' + str(str3) + ' ' + str(str4)
    return full_str

'''
place where the data is
'''
os.chdir("C:\\Users\\dave\\Desktop\\Class\\Data")
os.listdir()

'''
key and call
'''
api_key = 'xxxxxxx' # hide this on git
google_places = GooglePlaces(api_key)
gmaps = googlemaps.Client(key=api_key)


'''
load the file
'''
file_name = 'Business_Entities_in_Colorado.csv'
sos_base_file = pd.read_csv(file_name,parse_dates=True)


'''
Filter the data set to 2015-2016
'''
sos_base_file = sos_base_file[sos_base_file['entityformdate'].str.contains
                              ("2016|2015")]


'''
make sure address is X if no value
'''
sos_base_file.principaladdress1 = sos_base_file.principaladdress1.fillna('X')


google_places_array = sos_base_file.copy(deep=True)
google_places_array = google_places_array.filter(['entityid','principaladdress1',
                                                  'principalcity','principalstate',
                                                  'principalzipcode','entityname'  ])

'''
create a full address
'''
google_places_array['fulladdress'] = np.vectorize(fulladdr)(google_places_array['principaladdress1'],
                   google_places_array['principalcity'],google_places_array['principalstate'],
                   google_places_array['principalzipcode']                   
                   )    
     
'''
create columsn for lat and long
'''
google_places_array['lat']  =-1
google_places_array['long']  =-1
google_places_array['type']  ='XXXXX'
google_places_array['rating']  ='XXXXX'

print(google_places_array.head())

'''
loop through sos data
'''

print('start loop')
counter = 0 #this is to load data incrementally as per Googles rules
'''
Loop through the addresses and get google info
'''
for i in google_places_array.index:
    counter = counter+1 #The index is not ordered so I create an ordered one
    
    #sos_base_file['entityformdateyear'][i] = sos_base_file.entityformdate[i][-4:]
    #temp_year = int(sos_base_file.entityformdate[i][-4:])
    #sos_base_file.loc[sos_base_file.index[i], 'entityformdateyear'] = temp_year
    #sos_base_file.loc[sos_base_file.index[i], 'entityformdateyear'] = temp_year
    if counter <= 10000 and google_places_array.principaladdress1[i] !='X':
        
        if counter % 10000 == 0 : # this exists for QA
            print (counter)
                    
        #set default values
        place = 'ABC123'
        google_places_array.at[i,'lat']=-1
        google_places_array.at[i,'long']=-1
        google_places_array.at[i,'type']='XXXXX'
        google_places_array.at[i,'rating']=-1            
        #print(addr)            
        #print(geocode_result[0]['geometry']['location']['lat'])
        #print(geocode_result[0]['geometry']['location']['lng'])
        try:
            addr=google_places_array.fulladdress[i]
            geocode_result = gmaps.geocode(addr)

            place = geocode_result[0]['place_id'] #need to trap this error        
            query_result = google_places.get_place(place_id = place)
            query_result.get_details()
        #print (query_result.types)
            google_places_array.at[i,'lat']=geocode_result[0]['geometry']['location']['lat']
            google_places_array.at[i,'long']=geocode_result[0]['geometry']['location']['lng']
            google_places_array.at[i,'type']=query_result.types
            google_places_array.at[i,'rating']=query_result.rating
        #print('detail name')
        #print (query_result.name)
        #print(query_result.rating)
        #print('\r')
        except:
            print("An error")
            print(counter)
        
print('end loop')   
        
google_places_array.to_csv('google.csv', encoding='utf-8', index=False)        
        
        
        
        
        
        
        
        
        
        
        
        
        