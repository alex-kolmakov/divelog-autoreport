if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
import joblib
import pandas as pd
import requests
import json

NOTION_API_TOKEN = 'secret_wrPAJoosQ1gYTE5OmZm4e2IuzaI0HfhloocmSY3A36E'
NOTION_DATABASE_ID = 'ed1fccc483ee4d1a9cf7dc84a599dc22'

# Headers for Notion API requests
headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Function to generate the report
def generate_report(dive_features, model):
    dive_number = dive_features['dive_number']
    
    # Prepare the feature vector for the model
    feature_vector = dive_features[['avg_depth', 'max_depth', 'depth_variability', 
                                    'avg_temp', 'max_temp', 'temp_variability', 
                                    'avg_pressure', 'max_pressure', 'pressure_variability',
                                    'min_ndl']].values
    
    # Predict the likelihood of adverse conditions
    adverse_conditions_prob = model.predict_proba([feature_vector])[0][1]
    
    report = {
        "Dive Number": dive_number,
        "Average Depth": dive_features['avg_depth'],
        "Maximum Depth": dive_features['max_depth'],
        "Depth Variability": dive_features['depth_variability'],
        "Average Temperature": dive_features['avg_temp'],
        "Maximum Temperature": dive_features['max_temp'],
        "Temperature Variability": dive_features['temp_variability'],
        "Average Pressure": dive_features['avg_pressure'],
        "Maximum Pressure": dive_features['max_pressure'],
        "Pressure Variability": dive_features['pressure_variability'],
        "Minimal NDL": dive_features['min_ndl'],
        "SAC Rate": dive_features['sac_rate'],
        "Likelihood of Adverse Conditions": adverse_conditions_prob,
        "Issues": []
    }
    
    # Potential issues
    if dive_features['sac_rate'] > 19.0:
        report["Issues"].append("High SAC rate")
    if adverse_conditions_prob > 0.7:
        report["Issues"].append("Adverse conditions predicted")
    
    return report

# Function to send data to Notion
def send_to_notion(report, api_token, database_id):
    url = "https://api.notion.com/v1/pages"
    
    properties = {
        "Dive Number": {
            "title": [
                {
                    "text": {
                        "content": str(report["Dive Number"])
                    }
                }
            ]
        },
        # "Average Depth": {
        #     "number": report["Average Depth"]
        # },
        # "Maximum Depth": {
        #     "number": report["Maximum Depth"]
        # },
        # "Depth Variability": {
        #     "number": report["Depth Variability"]
        # },
        # "Average Temperature": {
        #     "number": report["Average Temperature"]
        # },
        # "Maximum Temperature": {
        #     "number": report["Maximum Temperature"]
        # },
        # "Temperature Variability": {
        #     "number": report["Temperature Variability"]
        # },
        # "Average Pressure": {
        #     "number": report["Average Pressure"]
        # },
        # "Maximum Pressure": {
        #     "number": report["Maximum Pressure"]
        # },
        # "Pressure Variability": {
        #     "number": report["Pressure Variability"]
        # },
        "Minimal NDL": {
            "number": report["Minimal NDL"]
        },
        "SAC Rate": {
            "number": report["SAC Rate"]
        },
        "Likelihood of Adverse Conditions": {
            "number": report["Likelihood of Adverse Conditions"]
        },
        "Issues": {
            "multi_select": [
                {"name": item} for item in report['Issues']
            ]
        }
        
    }
    
    data = {
        "parent": {"database_id": database_id},
        "properties": properties
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()

# Function to retrieve all pages in a Notion database
def get_all_pages(database_id, headers):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    return data.get('results', [])

# Function to update a page in Notion
def update_page(page_id, report, headers):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    
    properties = {
        "Dive Number": {
            "title": [
                {
                    "text": {
                        "content": str(report["Dive Number"])
                    }
                }
            ]
        },
        # "Average Depth": {
        #     "number": report["Average Depth"]
        # },
        # "Maximum Depth": {
        #     "number": report["Maximum Depth"]
        # },
        # "Depth Variability": {
        #     "number": report["Depth Variability"]
        # },
        # "Average Temperature": {
        #     "number": report["Average Temperature"]
        # },
        # "Maximum Temperature": {
        #     "number": report["Maximum Temperature"]
        # },
        # "Temperature Variability": {
        #     "number": report["Temperature Variability"]
        # },
        # "Average Pressure": {
        #     "number": report["Average Pressure"]
        # },
        # "Maximum Pressure": {
        #     "number": report["Maximum Pressure"]
        # },
        # "Pressure Variability": {
        #     "number": report["Pressure Variability"]
        # },
        "Minimal NDL": {
            "number": report["Minimal NDL"]
        },
        "SAC Rate": {
            "number": report["SAC Rate"]
        },
        "Likelihood of Adverse Conditions": {
            "number": report["Likelihood of Adverse Conditions"]
        },
        "Issues": {
            "multi_select": [
                {"name": item} for item in report['Issues']
            ]
        }
    }
    
    data = {
        "properties": properties
    }
    
    response = requests.patch(url, headers=headers, data=json.dumps(data))
    return response.status_code, response.json()

# Function to add or update a page in Notion
def add_or_update_page(report, headers, database_id):
    pages = get_all_pages(database_id, headers)
    page_id = None
    for page in pages:
        title = page['properties']['Dive Number']['title'][0]['text']['content']
        if title == str(report["Dive Number"]):
            page_id = page['id']
            break
    
    if page_id:
        status_code, response = update_page(page_id, report, headers)
        if status_code == 200:
            print(f"Successfully updated report for Dive {report['Dive Number']}")
        else:
            print(f"Failed to update report for Dive {report['Dive Number']}: {response}")
    else:
        status_code, response = send_to_notion(report, NOTION_API_TOKEN, NOTION_DATABASE_ID)
        if status_code == 200:
            print(f"Successfully added report for Dive {report['Dive Number']}")
        else:
            print(f"Failed to add report for Dive {report['Dive Number']}: {response}")

@data_exporter
def export_data(features, model_performance, *args, **kwargs):
    """
    Exports data to Notion and generates reports.

    Args:
        features: DataFrame containing the dive features
        model_performance: Dictionary containing the filename of the model
        args: Additional arguments
        kwargs: Additional keyword arguments

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """

    model = joblib.load(model_performance['filename'])

    for index, dive_features in features.iterrows():
        report = generate_report(dive_features, model)
        add_or_update_page(report, headers, NOTION_DATABASE_ID)

