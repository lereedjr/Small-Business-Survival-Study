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

I also acquired data from the IRS and Bureau of Labor and Statistics.


Reviewed data on the BLS and IRS
Tried using Google places
Combined entity statuses as I thought was correct
Data set not perfectly balanced but pretty close
State of business origin matters
Can't find small business without buying

# Images
logloss and AUC
test and training
most predictive

# Implementation Details and Analysis
acquired data from SOS manually
  contemplated an automated process
researched other data sources on BLS and IRS
Looked for zip level data


did not know Python
discuss models and model variations
NN
GLM
GBM
Auto ML


AUC results
logloss results
Models only performed OK
Ran into trouble with Google places


# Conclusions
Don't start a business in Dec or Feb
Location matters
Some cities far better


# Link to Video
