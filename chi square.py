# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 18:52:06 2018

@author: dave
"""



import pandas as pd
import os
import numpy as np
import scipy.stats as stats

def makeaone(instr):
    if instr == 'Y':    
        return 1
    else:
        return 0




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
file_name = 'sos_usps_irs_emp_file.csv'
sos_updated_file = pd.read_csv(file_name,parse_dates=True)
sos_updated_file['positive_status'] = 0


sos_updated_file['positive_status'] = np.vectorize(makeaone)(sos_updated_file['entitystatus'])


'''
sum the data to the month
'''
mon_sum_total = sos_updated_file.groupby('entityformdatemon', as_index=False)['rowcount','positive_status'].sum()
#mon_sum_yes = sos_updated_file.groupby('entityformdatemon', as_index=False)['positive_status'].sum()


observed = mon_sum_total.drop('positive_status', 1)
expected = mon_sum_total.drop('rowcount', 1)

chi = stats.chisquare(f_obs= observed,   # Array of observed counts
                f_exp= expected)   # Array of expected counts

chi_squared_stat = (((observed-expected)**2)/expected).sum().sum()

print(chi_squared_stat)