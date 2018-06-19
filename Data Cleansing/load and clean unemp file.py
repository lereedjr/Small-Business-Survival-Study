# -*- coding: utf-8 -*-
"""
Created on Mon May 28 18:47:35 2018
This script will load data and manipulate the unemployment data
@author: dave
"""


"""
packages
"""
import pandas as pd
import os
import numpy as np

'''
zip made a string
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
load the cleaned usps and sos data
unsure if I want to automate download
'''
file_name = 'sos_usps_irs_file.csv'
sos_updated_file = pd.read_csv(file_name,parse_dates=True)
#print(sos_updated_file.head())

'''
data from BLS unemployment 
'''
emp_file = pd.read_csv("zipunempload.csv",parse_dates=True)
#print(emp_file.head())

'''
create new zip column to map data
inplace = true or it does not work, weird
'''
sos_updated_file['principalzipcode'] = sos_updated_file['principalzipcode'].astype(str)
emp_file['principalzipcode'] = np.vectorize(makezipstr)(emp_file['Zip'])
emp_file['principalzipcode'] = emp_file['principalzipcode'].astype(str)

'''
merge new data with prior data based on zip
'''
sos_updated_file = pd.merge(sos_updated_file,emp_file, how='left', on='principalzipcode')
print(sos_updated_file.head())

file_name = 'sos_usps_irs_emp_file.csv'
sos_updated_file.to_csv(file_name, encoding='utf-8', index=False)






















