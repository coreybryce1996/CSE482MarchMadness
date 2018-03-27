# CSE482MarchMadness
March Madness 2018 Predictive Model

Big Data Class for Michigan State University.

CSE 482 Project Proposal: NCAA March Madness Predictive Model
Bryce Corey - Owen McMahon - Matthew Pasco
2/8/2018 - Spring Semester

Data Sources
- http://www.cs.odu.edu/~yaohang/publications/MarchMadness.pdf
- https://arxiv.org/abs/1412.0248
- https://www.sports-reference.com/cbb/
- http://hoop-math.com
- https://kenpom.com
- https://www.kaggle.com/c/march-machine-learning-mania-2016/data
- https://www.kaggle.com/c/march-machine-learning-mania-2017/data

Abstract

The purpose of this project will be to build a predictive model for the upcoming 2018
NCAA Tournament. The predictive model will be used to classify two games and predict
the winner. This model can then be used on the tournament bracket.

Goals and Tasks of the Project:
    ● Use the Pandas Python Library to process the large amounts of data we will be using
    ● Build models from past years data, and test our current data against it to judge our
        correctness in predicting winners
    ● Use General team stats (PPG, FG%, W-L), Common Opponents (W-L amongst the
        opponents, etc) to gain a general idea which teams have a higher chance of winning
    ● Use more specific data such as Head-to-Head Matchups and Player-Matchups to
        possibly predict upsets and other match specifics.
    ● Test our predictive system for accuracy and try to determine if there are ways to improve
        it throughout the March Madness Tournament
        For the Final Product:


We would like to create a model that will receive two separate teams that are in the tournament,
and return to the user which team it predicts will win that matchup. We would like to do it this
way so that it is possible to test the multiple rounds that there are in March Madness, if we were
just to predict the outcome from the start, it would be possible that our second, third and fourth
round results would be skewed because of previous incorrect results.
In the end we would like to run our predictive system against each game during the tournament,
hopefully being able to compare the actual Tournament Results with our own.
Team Roles
Owen - Analyzing different machine learning strategies to best build our predictive modeling
system, training with previous year’s data, scraping for data if needed.
Bryce - Architect of the data; building the database and tables, finding parallels among the
datasets, work on GUI if we decide want one, scraping for data if needed.
Matt - Working on preprocessing the data, looking for trends and patterns in it using pandas,
scraping for data if needed

2018
