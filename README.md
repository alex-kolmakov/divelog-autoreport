
# Dive Log Autoreport

>  that learns how to rate dives and gives advice on how to improve the worst ones.

[![Linting and tests](https://github.com/alex-kolmakov/divelog-autoreport/actions/workflows/lint_and_test.yaml/badge.svg)](https://github.com/alex-kolmakov/divelog-autoreport/actions/workflows/lint_and_test.yaml)

![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Mage](https://img.shields.io/badge/-mage-purple?style=for-the-badge&link=https%3A%2F%2Fmage.ai%2F)
![dlt](https://img.shields.io/badge/-dlt-teal?style=for-the-badge&link=https%3A%2F%2Fdlthub.com%2F)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![mlflow](https://img.shields.io/badge/mlflow-%23d9ead3.svg?style=for-the-badge&logo=numpy&logoColor=blue)
![lance](https://img.shields.io/badge/-lancedb-white?style=for-the-badge&link=https%3A%2F%2Flancedb.com%2F)
![Notion](https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white)



## Problem statement

SCUBA diving is a popular hobby that is enjoyed by millions of people around the world including myself. Divers need to keep a log of their dives, which includes information such as the time, location, depth, duration, temperature and other details. Nowadays, all of them are measured and stored by wearable devices that track lots of different parameters with only one goal in mind - to keep the diver safe from dangerous adverse effects.

![image](https://github.com/user-attachments/assets/52d2ee9e-7a54-49d8-a44b-633aae10f34a)

Once the data has been measured it needs to be stored in the digital format for us to access. And there are not so many alternatives for digital logbooks, and even fewer options when it comes to open-source tools that could be easily integrated and built upon. This is why for this task we are going to be using - [Subsurface](https://github.com/subsurface/subsurface)

As with any other hobby, the subjective quality and rating of a dive can vary from amazing to horrendous. Any diver with decent experience will tell you just by looking at the [dive profiles](https://en.wikipedia.org/wiki/Dive_profile) below:

| Dive #1  | Dive #2 |
| ------------- | ------------- |
| ![Dive #1](https://github.com/alex-kolmakov/divelog-autoreport/assets/3127175/5d043a91-39bb-4b77-a49c-bd19b82cf04a) | ![Dive #2](https://github.com/alex-kolmakov/divelog-autoreport/assets/3127175/86bc990c-55e9-4c14-9db9-310b88b3c4bb)|


that Dive #1 is much worse than Dive #2. 

Furthermore, even if we know that the dive was not great - how do we improve? What went wrong? What could have been done better?

This is where Retrieval Augmented Generation (RAG) based on the [DAN](https://www.diversalertnetwork.org/) content comes into play. DAN is a non-profit organization that provides expert medical advice and research to help divers stay safe. They have a vast amount of content that can be used to generate insights on the dives and provide recommendations on how to improve.

Now the question is:

```
> Can the model learn how to rate dives from the logbook like a diver does? 
> And then helps to improve by providing insights on the worst dives?
```

If you are interested in why dives are different and how can anyone tell ~~(or who was the diver in the pictures :P)~~ - send me a message and I will be happy to explain!


## Project overview

It consists of 4 pipelines:

 - **Dives data** - a pipeline that loads the data from the Subsurface logbook, parses data from XML format.
 
 - **DAN RAG** - a pipeline that loads the data from the DAN website, parses the content and vectorizes it for RAG. Then evaluates prompts based on relevance and faithfulness using llm as a judge.
 
 - **Train model** - a pipeline that trains the model on the data, uses HyperOpt to pick the best parameters by looking at [ROC_AUC](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc) and accuracy. After MAX_EVALUATIONS of attempts to optimize hyperparameters, it saves the best model to the MLflow registry.

 - **Generate reports** - final pipeline that:
    - loads the model from the MLflow registry 
    - predicts the rating for the dives
    - generates reports on each dive
    - augments reports with insights using vectorized DAN content
    - sends final reports to Notion

### Architecture Diagram

![Autodivelog drawio (6)](https://github.com/user-attachments/assets/9684b41c-2f5e-49f8-a1de-0b6fa8b54412)


### File structure

```
├── divelog
│   ├── custom                         # async functions and dlt pipeline are stored here
│   ├── data_loade                     # data loader for the dives
│   ├── pipelines                      # mage stores pipeline definitions here
│   ├── requirements.txt               # python dependencies
│   ├── transformers                   # data enrichment, report generation and more
│   └── utils                          # dlt functions and notion api helpers
├── documentation
└── tests
├── llm_pipeline_experiments.ipynb     # llm pipeline as one notebook for easy access
├── anonymized_subsurface_export.ssrf  # anonymized data for testing
├── credentials.json                   # should be here if you are using your own GDrive
├── env.sample                         # sample env file
├── docker-compose.yml
├── Dockerfile                         # mage dockerfile
└── mlflow.dockerfile                  # mlflow dockerfile
```

### Setup

Start by running codespace: 

<a href='https://codespaces.new/alex-kolmakov/divelog-autoreport'><img src='https://github.com/codespaces/badge.svg' alt='Open in GitHub Codespaces' style='max-width: 100%;'></a>


https://github.com/user-attachments/assets/86db3084-5a48-4e6e-8e30-10c82f390b68



Copy the sample env file:

```bash
cp env.sample .env
```

Start the mage and mlflow containers
```bash
docker-compose up --build
```




For detailed setup instructions, please refer to the [setup documentaion](./documentation/setup.md).



## Acknowledgements & Credits

If you're interested in contributing to this project, need to report issues or submit pull requests, please get in touch via 
- [GitHub](https://github.com/alex-kolmakov)
- [LinkedIn](https://linkedin.com/in/aleksandr-kolmakov)

Before submitting your pull request, please refer to the [contribution guidelines](./documentation/contribution.md). It will guide you through the process of setting up the environment with pre-commit hooks and running the linting and tests.


### Acknowledgements
Acknowledgement to #DataTalksClub for mentoring and providing a safe platform to learn. It has been a privilege to take part in the  2024 Cohort, go and check them out!

![image](https://github.com/alex-kolmakov/divesite-species-analytics/assets/3127175/d6504180-31a9-4cb7-8cd0-26cd2d0a12ad)



