# -*- coding: utf-8 -*-
"""
This script will load data and manipulate the huds usps data

"""

"""
packages
"""
import pandas as pd
import os
import numpy as np


'''
might not need this, created to make zip a string again
'''


def makezipstr(innum):
    innum = str(innum)
    return innum.zfill(5)


"""
SET WORKING DIRECTORY
load the data with the dependent variable
"""
os.chdir("C:\\Users\\dave\\Desktop\\Class\\Data")
os.listdir()

'''
load the data
unsure if I want to automate download
'''
file_name = 'finalsosdata.csv'
sos_updated_file = pd.read_csv(file_name, parse_dates=True)

'''
data based on usps hud zip
'''
zip_to_county = pd.read_csv("ZIP_COUNTY_032018.csv", parse_dates=True)


'''
Killed an hour looking for as_index=False; Python you are lame at data munging
This groups the data by zip
That way the join does not create a many to one
'''
zip_to_county_sum = zip_to_county.groupby('zip', as_index=False)[
    'res_ratio', 'bus_ratio', 'oth_ratio', 'tot_ratio'].mean()

# make sure data looks ok
print(zip_to_county_sum.head())


'''
create new zip column to map data
inplace = true or it does not work, weird
'''
zip_to_county_sum['principalzipcode'] = np.vectorize(
    makezipstr)(zip_to_county_sum['zip'])
# test new column
print(zip_to_county_sum.head())

'''
merge new data with prior data based on zip
'''
sos_updated_file = pd.merge(
    sos_updated_file, zip_to_county_sum, how='left', on='principalzipcode')


'''
move the summed file back out to working directory
I can do a manual QA on the csv
'''
file_name = 'zip_to_county_sum.csv'
zip_to_county_sum.to_csv(file_name, encoding='utf-8', index=False)

file_name = 'sos_usps_file.csv'
sos_updated_file.to_csv(file_name, encoding='utf-8', index=False)


#sos_base_file.rename(index=str, columns={"principalzipcode": "zip"},inplace=True)

#zip_to_county['principalzipcode'] = zip_to_county['zip']

#result = pd.merge(sos_base_file,zip_to_county, how='left', on='principalzipcode')

#result = pd.merge(sos_base_file,zip_to_county,  on='principalzipcode')
