# -*- coding: utf-8 -*-
"""
Created on Sun May 20 17:02:11 2018

@author: dave

code from 
https://github.com/h2oai/h2o-tutorials/blob/master/tutorials/gbm-randomforest/GBM_RandomForest_Example.py
https://stackoverflow.com/questions/40179875/h2o-python-api-retrieve-best-models-from-gridsearch

"""

import h2o
import os


print('start')

'''
set working directory
'''
os.chdir("C:\\Users\\dave\\Desktop\\Class\\Data")
# os.listdir() #for QA

'''
get h2o up and running
unsure parameters; need to test
'''
h2o.init(max_mem_size="4G")  # specify max number of bytes. uses all cores by default.
h2o.remove_all()  # clean slate, in case cluster was already running

'''
load the models I'd like to try
'''
from h2o.estimators.deeplearning import H2OAutoEncoderEstimator, H2ODeepLearningEstimator

'''
import data
'''
sos_df = h2o.import_file(os.path.realpath("sos_usps_irs_emp_file.csv"))

'''
data understanding
move all this to Jupyter?
'''
sos_df.describe()
sos_df.col_names

'''
split data set
 60% for training  
 20% for validation (hyper parameter tuning)  
 20% for final testing  
'''
train, valid, test = sos_df.split_frame([0.6, 0.2], seed=1234)

'''
make sure I know what the code does
'''
print('train \r')
train.describe()
print('valid \r')
valid.describe()
print('test \r')
test.describe()


'''
set up the indep and dep variables
the second input on the array is where the aaray stops
'''
sos_df_X = sos_df.col_names[2:10]+sos_df.col_names[12:22] + \
    sos_df.col_names[23:25]  # +sos_df.col_names[26:]
sos_df_y = sos_df.col_names[10]

'''
NN
'''
sos_nn_v1 = H2ODeepLearningEstimator(model_id="sos_nn_v1", epochs=100,
                                     variable_importances=True,  # this can be slow
                                     hidden=[10, 10, 10, 10, 10])

sos_nn_v1.train(sos_df_X, sos_df_y, training_frame=train,
                validation_frame=valid)
'''
output
'''
sos_nn_v1.score_history()
sos_nn_v1.varimp()
sos_nn_v1.logloss  # http://wiki.fast.ai/index.php/Log_Loss


'''
loop through activation
'''
models_act = []
m_names_act = []

for i, method in enumerate(["Tanh", "Maxout", "Rectifier", "RectifierWithDropout"]):
    # print(i)
    # print(method)
    models_act.append(H2ODeepLearningEstimator(model_id="sos_nn_"+method,
                                               activation=method, hidden=[10, 10, 10, 10, 10], epochs=100))
    models_act[i].train(sos_df_X, sos_df_y,
                        training_frame=train, validation_frame=valid)
    m_names_act.append("DL" + method + "Activation")


# h2o.cluster().shutdown()
print('end')  # just for my sanity
