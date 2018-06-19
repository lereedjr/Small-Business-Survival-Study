# -*- coding: utf-8 -*-
"""
This script will load data and manipulate the IRS filing data

"""

"""
packages
"""
import pandas as pd
import os

"""
SET WORKING DIRECTORY
load the data with the dependent variable
"""
os.chdir("C:\\Users\\dave\\Desktop\\Class\\Data")
os.listdir()

'''
load the cleaned usps and sos data
unsure if I want to automate download
'''
file_name = 'sos_usps_file.csv'
sos_updated_file = pd.read_csv(file_name, parse_dates=True)
print(sos_updated_file.head())

'''
data from irs 
I manually changed the header name
'''
irs_file = pd.read_csv("irsfilingloading.csv", parse_dates=True)
print(irs_file.head())

'''
columns won't join if types are different
'''
#sos_updated_file['principalzipcode'] = sos_updated_file['principalzipcode'].astype(str)
irs_file['principalzipcode'] = irs_file['principalzipcode'].astype(str)

'''
merge new data with prior data based on zip
'''
sos_updated_file = pd.merge(
    sos_updated_file, irs_file, how='left', on='principalzipcode')
print(sos_updated_file.head())


file_name = 'sos_usps_irs_file.csv'
sos_updated_file.to_csv(file_name, encoding='utf-8', index=False)
