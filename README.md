
# Dive Log Autoreport

>  that learns how to rate the dives from your logbook like you do.

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Google Drive](https://img.shields.io/badge/Google%20Drive-4285F4?style=for-the-badge&logo=googledrive&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![mlflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue)![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=black)





## Problem statement

SCUBA diving is a popular hobby that is enjoyed by millions of people around the world including myself. Divers need to keep a log of their dives, which includes information such as the time, location, depth, duration, temperature and other details. Nowdays all of them are measured and stored by wearable devices that track lots of different parameters with only one goal in mind - to keep the diver safe from dangerous adverse effects. 

![image](https://github.com/user-attachments/assets/52d2ee9e-7a54-49d8-a44b-633aae10f34a)

Once the data has been measured it needs to be stored in the digital format for us to access. And there are not so many alternatives for the digital log books, and even less options when it comes open source tools that could be easily integrated and build upon.
Which is why for this task we are going to be using - [Subsurface](https://github.com/subsurface/subsurface)

As with any other hobby - subjective quality and rating of the dive can vary from amazing to horrendous. And any diver with decent experience will tell you just by looking at the [dive profiles](https://en.wikipedia.org/wiki/Dive_profile) below:

| Dive #1  | Dive #2 |
| ------------- | ------------- |
| ![Dive #1](https://github.com/alex-kolmakov/divelog-autoreport/assets/3127175/5d043a91-39bb-4b77-a49c-bd19b82cf04a) | ![Dive #2](https://github.com/alex-kolmakov/divelog-autoreport/assets/3127175/86bc990c-55e9-4c14-9db9-310b88b3c4bb)|


That the Dive #1 is much worse than the Dive #2.
And the question is:

```
> Can we train a model to rate the dives?
```

If you are interested in why dives are different and how can anyone tell ~~(or who was the diver in the pictures :P)~~ - send me a message and I will be happy to explain!


## Project overview

It consists of 3 pipelines that learn your diving preferences and rate the dives from your Subsurface logbook.

 - **Load data** - pipeline that loads the data from the Subsurface logbook, parses data from xml format and provides it as a clean dataframe through Global data product.
 - **Train model** - pipeline that trains the model on the data, uses HyperOpt to pick the best parameters looking at ROC_AUC, recall and precision. After *NUMBER_OF_ITERATIONS* saves the best model to the MLflow registry.
 - **Batch inference** - pipeline that loads the model from the MLflow registry and predicts the rating for the dives in the logbook. It then exports the data to the Notion page using the Notion API.

### Architecture Diagram

![Autodivelog drawio (2)](https://github.com/user-attachments/assets/7bdb24bb-8f9e-4eab-bfcc-e1de3473000e)


### Setup

Start by running codespace: 

<a href='https://codespaces.new/alex-kolmakov/divelog-autoreport'><img src='https://github.com/codespaces/badge.svg' alt='Open in GitHub Codespaces' style='max-width: 100%;'></a>

And run the following command:

```docker-compose up --build -d```



https://github.com/user-attachments/assets/d5224774-6bb1-451c-90d0-e4ba223e1775


Since we are using Global Data product - if you try to run the last pipeline without running the first one - it will start the prerequisite pipeline automatically. But to have more visibility - my advice is to run them in order: 

**Load data** -> **Train model** -> **Batch inference**.




There is also an option to run this pipeline by setting up your own Google Drive and Notion API credentials. This will allow you to load the data from your own logbook and export the results to your Notion page. For this - please refer to the [additional documentaion](./documentation/setup.md).


### Contribute and test

> Project uses Github Actions CI/CD and pre-commit hooks for testing and linting.

Before submitting your pull request please refer to the [contribution guidelines](./documentation/contribution.md). It will guide you through the process of setting up the environment with a precommit hooks and running the linting and tests.


## Acknowledgements & Credits

If you're interested in contributing to this project, need to report issues or submit pull requests, please get in touch via 
- [GitHub](https://github.com/alex-kolmakov)
- [LinkedIn](https://linkedin.com/in/aleksandr-kolmakov)


### Acknowledgements
Acknowledgement to #DataTalksClub for mentoring us through the MLops Engineering Zoom Camp over the last 10 weeks. It has been a privilege to take part in the  2024 Cohort, go and check them out!

![image](https://github.com/alex-kolmakov/divesite-species-analytics/assets/3127175/d6504180-31a9-4cb7-8cd0-26cd2d0a12ad)



