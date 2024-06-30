
# Dive log ML pipeline

> This project is my first step on refining the process of extracting insights from my digital logbook. Main goal here is to automatically mark problematic dives that I do for further review. And also to streamline Notion export of the my logbook.


## Articles 

Project is described in depth on the following articles:

- I want to do this - but there is no clear schedule yet


## Project overview

>Project uses Mage.AI as a main data pipeline orchestration engine, ingests dives export from subsurface then trains classifier on them while keeping experiments tracked through MLFlow.
>Then it uses Notion API to export the results.

### Setup

To use this project we will need data exported from the subsurface program. There is a file with my anonimized dive data - feel free to use you own, there is a link on how to export it
It is important to mention that this project uses gdrive api to fetch fresh exports from the folder. To get it working you need to setup, download and provide path to the credentials.json file
Now we will need notion application token to utilise export feature.
All this should be provided to the .env file.

### Architecture Diagram

pending

### Data modelling



## Acknowledgements & Credits & Support

If you're interested in contributing to this project, need to report issues or submit pull requests, please get in touch via 
- [GitHub](https://github.com/alex-kolmakov)
- [LinkedIn](https://linkedin.com/in/aleksandr-kolmakov)


### Acknowledgements
Acknowledgement to #DataTalksClub for mentoring us through the Data Engineering Zoom Camp over the last 10 weeks. It has been a privilege to take part in the Spring '24 Cohort, go and check them out!

![image](https://github.com/alex-kolmakov/divesite-species-analytics/assets/3127175/d6504180-31a9-4cb7-8cd0-26cd2d0a12ad)



