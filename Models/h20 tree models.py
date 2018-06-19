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
#os.listdir() #for QA

'''
get h2o up and running
unsure parameters; need to test
'''
h2o.init(max_mem_size = "4G")             #specify max number of bytes. uses all cores by default.
h2o.remove_all()                          #clean slate, in case cluster was already running

'''
load the models I'd like to try
'''
from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.estimators.random_forest import H2ORandomForestEstimator
from h2o.grid import H2OGridSearch
from h2o.estimators.deeplearning import H2OAutoEncoderEstimator, H2ODeepLearningEstimator
from h2o.estimators.glm import H2OGeneralizedLinearEstimator



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
sos_df_X = sos_df.col_names[2:10]+sos_df.col_names[12:22]+sos_df.col_names[23:25]+sos_df.col_names[26:]
sos_df_y = sos_df.col_names[10] 

'''
build model
# **model_id:** Not required, but allows us to easily find our model in the [Flow](http://localhost:54321/) interface  
# **ntrees:** Maximum number of trees used by the random forest. Default value is 50. We can afford to increase this, as our early-stopping criterion will decide when the random forest is sufficiently accurate.  
# **stopping_rounds:** Stopping criterion described above. Stops fitting new trees when 2-tree rolling average is within 0.001 (default) of the two prior rolling averages. Can be thought of as a convergence setting.  
# **score_each_teration:** predict against training and validation for each tree. Default will skip several.  
# **seed:** set the randomization seed so we can reproduce results
'''
sos_rf_v1 = H2ORandomForestEstimator(
    model_id="sos_rf_v1",
    ntrees=1000,
    stopping_rounds=2,
    #score_each_iteration=True,
    max_depth = 10,
    seed=1234,
    #sample_rate = .99, # The range is 0.0 to 1.0, and this value defaults to 0.6320000291. 
    #Higher values may improve training accuracy.  
    binomial_double_trees=True #For binary classification: Build 2x as many trees (one per class)
    #type='classifier'
    )

'''
train the model

first variable is the thing to predict
second the indep variables
to get this to use regression I had to make the dep variable a string
'''
sos_rf_v1.train(sos_df_X, sos_df_y, training_frame=train, validation_frame=valid)

'''
hit ratio is not for random forest
'''
sos_rf_v1.score_history()
sos_rf_v1.varimp()
sos_rf_v1.logloss #http://wiki.fast.ai/index.php/Log_Loss


'''
more trees 1000
calibrate model true
'''
sos_rf_v2 = H2ORandomForestEstimator(
    model_id="sos_rf_v2",
    ntrees=1000,
    stopping_rounds=2,
    score_each_iteration=True,
    max_depth = 10,
    seed=1234,
    sample_rate = .99, # The range is 0.0 to 1.0, and this value defaults to 0.6320000291. 
    #Higher values may improve training accuracy.  
    binomial_double_trees=True #For binary classification: Build 2x as many trees (one per class)
    #type='classifier'.
    #calibrate_model=True
    )

sos_rf_v2.train(sos_df_X, sos_df_y, training_frame=train, validation_frame=valid)

'''
more trees 10000
calibrate model true
'''
sos_rf_v3 = H2ORandomForestEstimator(
    model_id="sos_rf_v3",
    ntrees=10000,
    stopping_rounds=2,
    score_each_iteration=True,
    max_depth = 10,
    seed=1234,
    #histogram_type = 'random',
    sample_rate = .99, # The range is 0.0 to 1.0, and this value defaults to 0.6320000291. 
    #Higher values may improve training accuracy.  
    binomial_double_trees=True #For binary classification: Build 2x as many trees (one per class)
    #type='classifier'.
    #calibrate_model=True
    )

sos_rf_v3.train(sos_df_X, sos_df_y, training_frame=train, validation_frame=valid)
sos_rf_v3.logloss























#h2o.cluster().shutdown()
print('end') #just for my sanity