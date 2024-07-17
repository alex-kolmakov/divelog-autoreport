
# Dive log ML pipeline

>  that learns how to rate the dives from your logbook like you do.

## Problem statement

SCUBA diving is a popular hobby that is enjoyed by millions of people around the world including myself. Divers need to keep a log of their dives, which includes information such as the time, location, depth, duration, temperature and other details. Nowdays all of them are measured and stored by wearable devices that track lots of different parameters with only one goal in mind - to keep the diver safe from dangerous adverse effects. 

Once the data has been measured it needs to be stored in the digital format for us to access. And there are not so many alternatives for the digital log books, and even less options when it comes open source tools that could be easily integrated and build upon.
Which is why for this task we are going to be using - [Subsurface](https://github.com/subsurface/subsurface)

As with any other hobby - subjective quality and rating of the dive can vary from amazing to horrendous. And any diver with decent experience will tell you by looking at the pictures below:

| Dive #1  | Dive #2 |
| ------------- | ------------- |
| ![Dive #1](https://github.com/alex-kolmakov/divelog-autoreport/assets/3127175/5d043a91-39bb-4b77-a49c-bd19b82cf04a) | ![Dive #2](https://github.com/alex-kolmakov/divelog-autoreport/assets/3127175/86bc990c-55e9-4c14-9db9-310b88b3c4bb)|


That the dive number one is much worse then dive number two.
I will not go into the detail on why (or who was the diver in the pictures :P) but the question is:

```
> Can we train a model to rate and grade the dives?
```


## Project overview

3 pipelines that learn your diving preferences and rates the dives from your Subsurface logbook.

 - **Load data** - pipeline that loads the data from the Subsurface logbook, parses data from xml format and provides it as a clean dataframe through Global data product.
 - **Train model** - pipeline that trains the model on the data, uses HyperOpt to pick the best parameters looking at ROC_AUC, recall and precision. After *NUMBER_OF_ITERATIONS* saves the best model to the MLflow registry.
 - **Batch inference** - pipeline that loads the model from the MLflow registry and predicts the rating for the dives in the logbook. It then exports the data to the Notion page using the Notion API.

### Architecture Diagram

![Autodivelog drawio (2)](https://github.com/user-attachments/assets/7bdb24bb-8f9e-4eab-bfcc-e1de3473000e)



### Setup

For the quick start you can use the github codespaces and run the following command:

```docker-compose up --build -d```

video here

It will launch the docker container with all the necessary dependencies and then you can proceed to Mage UI to launch pipelines.
Since we are using Global Data product - if you try to run the last pipeline without running the first one - it will start the prerequisite pipeline automatically. But to have more visibility - my advice is to run them in order: 

Load data -> Train model -> Batch inference.

There is also an option to run this pipeline by setting up your own Google Drive and Notion API credentials. This will allow you to load the data from your own logbook and export the results to your Notion page. For this - please refer to the [additional documentaion](./documentation/setup.md).

todo
Contribute and test

pre-commit install and autoupdate
pytest and coverage
integrations tests





## Acknowledgements & Credits & Support

If you're interested in contributing to this project, need to report issues or submit pull requests, please get in touch via 
- [GitHub](https://github.com/alex-kolmakov)
- [LinkedIn](https://linkedin.com/in/aleksandr-kolmakov)


### Acknowledgements
Acknowledgement to #DataTalksClub for mentoring us through the MLops Engineering Zoom Camp over the last 10 weeks. It has been a privilege to take part in the  2024 Cohort, go and check them out!

![image](https://github.com/alex-kolmakov/divesite-species-analytics/assets/3127175/d6504180-31a9-4cb7-8cd0-26cd2d0a12ad)



