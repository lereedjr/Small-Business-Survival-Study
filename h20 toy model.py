# -*- coding: utf-8 -*-
"""
Created on Sat May 19 11:23:06 2018

https://github.com/h2oai/h2o-tutorials/blob/master/tutorials/gbm-randomforest/GBM_RandomForest_Example.py

@author: dave
"""

# coding: utf-8

# # Introduction
# This tutorial shows how H2O [Gradient Boosted Models](https://en.wikipedia.org/wiki/Gradient_boosting) and [Random Forest](https://en.wikipedia.org/wiki/Random_forest) models can be used to do supervised classification and regression. This tutorial covers usage of H2O from Python. An R version of this tutorial will be available as well in a separate document. This file is available in plain R, R markdown, regular markdown, plain Python and iPython Notebook formats. More examples and explanations can be found in our [H2O GBM booklet](http://h2o.ai/resources/) and on our [H2O Github Repository](http://github.com/h2oai/h2o-3/).
# 

# ## Task: Predicting forest cover type from cartographic variables only
# 
# The actual forest cover type for a given observation (30 x 30 meter cell) was determined from the US Forest Service (USFS). We are using the UC Irvine Covertype dataset.

# ### H2O Python Module
# 
# Load the H2O Python module.

# In[ ]:

import h2o
import os

'''
set working directory
'''
os.chdir("C:\\Users\\dave\\Desktop\\Class\\Data")
#os.listdir() #for QA


# ### Start H2O
# Start up a 1-node H2O cloud on your local machine, and allow it to use all CPU cores and up to 2GB of memory:

# In[ ]:

h2o.init(max_mem_size = "2G")             #specify max number of bytes. uses all cores by default.
h2o.remove_all()                          #clean slate, in case cluster was already running

#GUI http://127.0.0.1:54321/flow/index.html


# To learn more about the h2o package itself, we can use Python's builtin help() function.

# In[ ]:

from h2o.estimators.gbm import H2OGradientBoostingEstimator
from h2o.estimators.random_forest import H2ORandomForestEstimator


'''
acquire data
'''
covtype_df = h2o.import_file(os.path.realpath("covtypefull.csv"))

'''
split data set
 60% for training  
 20% for validation (hyper parameter tuning)  
 20% for final testing  
'''

train, valid, test = covtype_df.split_frame([0.6, 0.2], seed=1234)


#Prepare predictors and response columns
covtype_X = covtype_df.col_names[:-1]     #last column is Cover_Type, our desired response variable 
covtype_y = covtype_df.col_names[-1] 

'''
build model
# **model_id:** Not required, but allows us to easily find our model in the [Flow](http://localhost:54321/) interface  
# **ntrees:** Maximum number of trees used by the random forest. Default value is 50. We can afford to increase this, as our early-stopping criterion will decide when the random forest is sufficiently accurate.  
# **stopping_rounds:** Stopping criterion described above. Stops fitting new trees when 2-tree rolling average is within 0.001 (default) of the two prior rolling averages. Can be thought of as a convergence setting.  
# **score_each_teration:** predict against training and validation for each tree. Default will skip several.  
# **seed:** set the randomization seed so we can reproduce results
'''
rf_v1 = H2ORandomForestEstimator(
    model_id="rf_covType_v1",
    ntrees=2000,
    stopping_rounds=2,
    score_each_iteration=True,
    seed=1000000)

'''
train the model
'''

rf_v1.train(covtype_X, covtype_y, training_frame=train, validation_frame=valid)
#this ran pretty quickly

'''
'''
rf_v1.score_history()

'''
hit ratio
'''
rf_v1.hit_ratio_table(valid=True)



'''
boosted tree
'''
gbm_v1 = H2OGradientBoostingEstimator(
    model_id="gbm_covType_v1",
    seed=2000000
)


gbm_v1.train(covtype_X, covtype_y, training_frame=train, validation_frame=valid)

gbm_v1.score_history()


# In[ ]:

gbm_v1.hit_ratio_table(valid=True)

'''
improve the tree
'''

gbm_v2 = H2OGradientBoostingEstimator(
    ntrees=20,
    learn_rate=0.2,
    max_depth=10,
    stopping_tolerance=0.01, #10-fold increase in threshold as defined in rf_v1
    stopping_rounds=2,
    score_each_iteration=True,
    model_id="gbm_covType_v2",
    seed=2000000
)
gbm_v2.train(covtype_X, covtype_y, training_frame=train, validation_frame=valid)


'''
more testing
'''
gbm_v3 = H2OGradientBoostingEstimator(
    ntrees=30,
    learn_rate=0.3,
    max_depth=10,
    sample_rate=0.7,
    col_sample_rate=0.7,
    stopping_rounds=2,
    stopping_tolerance=0.01, #10-fold increase in threshold as defined in rf_v1
    score_each_iteration=True,
    model_id="gbm_covType_v3",
    seed=2000000
)
gbm_v3.train(covtype_X, covtype_y, training_frame=train, validation_frame=valid)

#shut it down
#h2o.shutdown(prompt=False)

'''
more tree
'''
rf_v2 = H2ORandomForestEstimator(
    model_id="rf_covType_v2",
    ntrees=200,
    max_depth=30,
    stopping_rounds=2,
    stopping_tolerance=0.01,
    score_each_iteration=True,
    seed=3000000)
rf_v2.train(covtype_X, covtype_y, training_frame=train, validation_frame=valid)



h2o.shutdown(prompt=False)












