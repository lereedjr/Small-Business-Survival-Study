# Project Overview

Predicting Colorado Business Survival

Investing in a business is a serious commitment. The rewards are high for both the business owner and the community. Businesses create the jobs needed for a community to thrive. Many businesses fail however. I would like to help Colorado business owners determine the likelihood their business will succeed. I want to find driving factors that might help these businesses survive. This information will help possible business owners make the best decision about when and where to open their new business.

# Why I picked This Project
I work for a company called Pinnacol Assurance. Pinnacol is a non for profit company that provides worker's compensation insurance to 60,000 Colorado businesses. Most of these businesses are small. I am interested in doing whatever I can to help small business owners. I wanted to build a tool that would help business owners survive and thrive.

# Tools Used
I decided to use Python as my primary tool. I have not used Python previously. However, it seems it has become the lingua franca of the data sciences. Also, my staff are Python experts. I wanted to learn so I could read their code and understand their day to day work more effectively. Within Python I decided to use H2O models. They have an easy to use toolkit and a tool that automates machine learning. This tool builds a suite of models and then builds an ensemble on the set of models. The only limits are time and resources.

For data exploration I used Tableau and Excel. I used Excel when I first pulled the data as it was easy to create pivot tables for quality checks. I used Tableau for my exploratory data analysis.

I tinkered with Jupyter but found the Spyder IDE was easier to work with. I also used Git Desktop and the Atom text editor for a small portion of my work.

# Data Insights
My base data set came from the Colorado government website https://data.colorado.gov/. The Colorado Secretary of State maintains a list of all Colorado businesses. This list contains over one million businesses. The data set goes back to the 1800's. The data set contains information like address, entity type and the date the entity formed. The data is not time variant. this means older businesses have had more time to go insolvent. I decided to limit my data to only entities formed in 2015 and 2016. This seemed like enough time to neither limit nor exaggerate aging impacts. After limiting the years I removed superfluous columns and combined the eight entity status codes into a binary variable. The only issue I ran into during this process related to my inexperience with Python. I attempted to loop through the 1M record data set to update values. The code never finished. After using the Python apply function the data updates took seconds.

I also acquired data from the IRS and Bureau of Labor and Statistics. The process of researching the data was tedious and time consuming. Much of the data is old. Much of the data did not appear relevant to my question. The websites were difficult to navigate also. Once I acquired the IRS and BLS data it was necessary to alter the data. Some of the data was laid out rows wise and it needed to be columns wise. In other places the granularity was not at the zip level. This necessitated averaging the results from the BLS data.

I spent a large amount of time building an program to pull Google API data. The learning experience was great. The program worked also. I ran into two issues that prevented use of the Google data. The first is data sparsity. Google has a location review and data about the type of location. For example, I might be able to find if the location is a liquor store or a bank. both of these data items were rarely populated. It looks like many businesses have homes as locations. This is a possible driver. Regardless I was unable to use the Google data in my model. Also, I was only able to acquire 8k records or so before Google stopped giving me data. This is puzzling as I used a paid account and thought I could use 150k transactions a day.

The Colorado SOS data has a number of different entity statuses. These are listed below. I combined exists and good standing to indicate business survival.

Administratively Dissolved
Converted
Delinquent
Dissolved (Term Expired)
Exists
Good Standing
Judicially Dissolved
Noncompliant
Registered Agent Resigned
Revoked
Voluntarily Dissolved
Withdrawn

I also researched several paid sources for business data. The prices were not exorbitant but I did not want to spend more than a few dollars. I decided to run with what I could get for free.

# EDA
For my exploratory data analysis I used Tableau in combination with Excel. Use this link to view my EDA. <a href="https://github.com/sautherd1973/python/blob/master/EDA.pdf" rel="nofollow"> EDA</a> There are several thing that stood out to me during the exploratory data analysis. First, the data is fairly well balanced. The number of businesses in existence is about 60% of the total population. This removed the need to perform SMOTE or another algorithm to handle class imbalances. Next, the only city with more failed then successful businesses is Aurora. This might indicate certain regions have issue with early business termination. IRS filing data did not have an impact on entity status. This was surprising. I expected businesses to flourish in higher income areas. Business failure was marginally higher in areas of high unemployment. The month an entity forms does appear to have a large impact on entity status. The month of February has a high failure rate. All other months have a higher success rate. There are a large number of businesses forming in Colorado with out of state addresses. It did not appear being an out of state entity had an impact on business success however. I last took a look at BLS data around residential to business address ratios in the zip. This also appears to not be a driver of business success.

# Model insights

I used a variety of model types. For my own edification I tried trees, gradient boosted trees, neural networks and generalized linear models. I experimented with a large number of hyperparameters. I used grid search to expedite the model building process as well as H2O's model ensemble builder. I spent a large amount of time trying to find ways to materially improve my models. Model results were very close between most models. The first round of tuning created a large amount of differences and only small differences after that. I used area under the curve and log loss as my performance metrics. My best models had an AUC value of almost .67. The best models had a log loss value of around .64. I found my training data did much better than my validation data. So overfitting was an issue. You can see an image of the AUC curves in this link  <a href="hhttps://github.com/sautherd1973/python/blob/master/auc.gi" rel="nofollow"> AUC.</a> One can see a subset of my model results in this link .



discuss models and model variations
NN
GLM
GBM
Auto ML
AUC results
logloss results
Models only performed OK
chi square analysis


# Images
logloss and AUC
variable importance

# Conclusions
Don't start a business in Dec or Feb
Location matters
Some cities far better


# Link to Video
