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
from h2o.automl import H2OAutoML
from h2o.grid.grid_search import H2OGridSearch
import math


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
train, valid, test = sos_df.split_frame([0.6, 0.3], seed=1234)

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
sos_gbm_v1 = H2OGradientBoostingEstimator(
    model_id="sos_gbm_v1",
    ntrees=100,
    stopping_rounds=2,
    score_each_iteration=True,
    max_depth = 50,
    seed=1234,
    #learn_rate = .99
    sample_rate = .99, # The range is 0.0 to 1.0, and this value defaults to 0.6320000291. 
    #Higher values may improve training accuracy.  
  
    #type='classifier'
    )

'''
train the model

first variable is the thing to predict
second the indep variables
to get this to use regression I had to make the dep variable a string
'''
sos_gbm_v1.train(sos_df_X, sos_df_y, training_frame=train, validation_frame=valid)

'''
hit ratio is not for random forest
'''
sos_gbm_v1.score_history()
sos_gbm_v1.varimp()
sos_gbm_v1.logloss #http://wiki.fast.ai/index.php/Log_Loss


'''
more trees 1000
calibrate model true
'''
sos_gbm_v2 = H2OGradientBoostingEstimator(
    model_id="sos_gbm_v2",
    ntrees=1000,
    stopping_rounds=2,
    score_each_iteration=True,
    max_depth = 10,
    seed=1234,
    sample_rate = .99, # The range is 0.0 to 1.0, and this value defaults to 0.6320000291. 
    #Higher values may improve training accuracy.  
    #binomial_double_trees=True #For binary classification: Build 2x as many trees (one per class)
    #type='classifier'.
    #calibrate_model=True
    )

sos_gbm_v2.train(sos_df_X, sos_df_y, training_frame=train, validation_frame=valid)

'''
more trees 10000
calibrate model true
'''
sos_gbm_v3 = H2OGradientBoostingEstimator(
    model_id="sos_gbm_v3",
    ntrees=10000,
    stopping_rounds=2,
    score_each_iteration=True,
    max_depth = 10, #max depth mkes the model worse?
    seed=1234,
    #histogram_type = 'random',
    sample_rate = .99, # The range is 0.0 to 1.0, and this value defaults to 0.6320000291. 
    #Higher values may improve training accuracy.  
    #binomial_double_trees=True #For binary classification: Build 2x as many trees (one per class)
    #type='classifier'.
    #calibrate_model=True
    )

sos_gbm_v3.train(sos_df_X, sos_df_y, training_frame=train, validation_frame=valid)
sos_gbm_v3.logloss

'''
automated ML
'''
aml = H2OAutoML(max_runtime_secs = 360,max_models = 10) 
aml.train( sos_df_X, sos_df_y, training_frame=train,  leaderboard_frame=valid )
# Print Leaderboard (ranked by xval metrics)
lb = aml.leaderboard

perf = aml.leader.model_performance(test)
perf.auc()

perf1 = aml.leader.model_performance(train)
perf1.auc()


gbm_final_grid = H2OGradientBoostingEstimator(distribution='bernoulli',
                    ## more trees is better if the learning rate is small enough 
                    ## here, use "more than enough" trees - we have early stopping
                    ntrees=10000,
                    ## smaller learning rate is better
                    ## since we have learning_rate_annealing, we can afford to start with a 
                    #bigger learning rate
                    learn_rate=0.05,
                    ## learning rate annealing: learning_rate shrinks by 1% after every tree 
                    ## (use 1.00 to disable, but then lower the learning_rate)
                    learn_rate_annealing = 0.99,
                    ## score every 10 trees to make early stopping reproducible 
                    #(it depends on the scoring interval)
                    score_tree_interval = 10,
                    ## fix a random number generator seed for reproducibility
                    seed = 1234,
                    ## early stopping once the validation AUC doesn't improve by at least 0.01% for 
                    #5 consecutive scoring events
                    stopping_rounds = 5,
                    stopping_metric = "AUC",
                    stopping_tolerance = 1e-4)





# create hyperameter and search criteria lists (ranges are inclusive..exclusive))# create 
hyper_params_tune = {'max_depth' : list(range(5,10+1,1)),
                'sample_rate': [x/100. for x in range(20,101)],
                'col_sample_rate' : [x/100. for x in range(20,101)],
                'col_sample_rate_per_tree': [x/100. for x in range(20,101)],
                'col_sample_rate_change_per_level': [x/100. for x in range(90,111)],
                'min_rows': [2**x for x in range(0,int(math.log(train.nrow,2)-1)+1)],
                'nbins': [2**x for x in range(4,11)],
                'nbins_cats': [2**x for x in range(4,13)],
                'min_split_improvement': [0,1e-8,1e-6,1e-4],
                'histogram_type': ["UniformAdaptive","QuantilesGlobal","RoundRobin"]}

search_criteria_tune = {'strategy': "RandomDiscrete",
                   'max_runtime_secs': 3600,  ## limit the runtime to 60 minutes
                   'max_models': 100,  ## build no more than 100 models
                   'seed' : 1234,
                   'stopping_rounds' : 5,
                   'stopping_metric' : "AUC",
                   'stopping_tolerance': 1e-3
                   }

hyper_params = {'max_depth' : range(1,30,2)}            
#Build grid search with previously made GBM and hyper parameters
final_grid = H2OGridSearch(gbm_final_grid, hyper_params = hyper_params_tune,
                                    grid_id = 'final_grid',
                                    search_criteria = search_criteria_tune)
#Train grid search
final_grid.train(x=sos_df_X, 
           y=sos_df_y,
           ## early stopping based on timeout (no model should take more than 1 hour - modify as needed)
           max_runtime_secs = 360, 
           training_frame = train,
           validation_frame = valid)


sorted_final_grid = final_grid.get_grid(sort_by='auc',decreasing=True)


best_model = h2o.get_model(sorted_final_grid.sorted_metric_table()['model_ids'][0])


performance_best_model = best_model.model_performance(test)



params_list = []
for key, value in best_model.params.items():
    params_list.append(str(key)+" = "+str(value['actual']))
params_list
























 
#final_gbm_predictions = sos_gbm_v1.predict(test)



#h2o.cluster().shutdown()
print('end') #just for my sanity