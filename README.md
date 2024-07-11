
# Dive log ML pipeline

>  that learns how to rate the dives from your logbook like you do.

## Problem statement

SCUBA diving is a popular sport and hobby that is enjoyed by millions of people around the world including myself. Divers often keep a log of their dives, which includes information such as the date, time, location, depth, duration, and other details about the dive. All of those details nowdays are measured and kept by so called dive computers - wearable devices that track lots of different parameters with only one goal in mind - to keep the diver safe from various adverse effects.

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

>Project uses Mage.AI as a main data pipeline orchestration engine, ingests dives export from subsurface then trains classifier on them while keeping experiments tracked through MLFlow.
>Then it uses Notion API to export the results.

### Setup



todo
Contribute and test

pre-commit install and autoupdate
pytest and coverage
integrations tests


### Architecture Diagram

pending


## Acknowledgements & Credits & Support

If you're interested in contributing to this project, need to report issues or submit pull requests, please get in touch via 
- [GitHub](https://github.com/alex-kolmakov)
- [LinkedIn](https://linkedin.com/in/aleksandr-kolmakov)


### Acknowledgements
Acknowledgement to #DataTalksClub for mentoring us through the MLops Engineering Zoom Camp over the last 10 weeks. It has been a privilege to take part in the  2024 Cohort, go and check them out!

![image](https://github.com/alex-kolmakov/divesite-species-analytics/assets/3127175/d6504180-31a9-4cb7-8cd0-26cd2d0a12ad)



