if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
import joblib
import pandas as pd


# Function to generate the report
def generate_report(dive_features, model):
    dive_number = dive_features['dive_number']
    
    # Prepare the feature vector for the model
    feature_vector = dive_features[['avg_depth', 'max_depth', 'depth_variability', 
                                    'avg_temp', 'max_temp', 'temp_variability', 
                                    'avg_pressure', 'max_pressure', 'pressure_variability',
                                    'min_ndl', 'max_ascend_speed', 'high_ascend_speed_count']].values
    
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
    if adverse_conditions_prob > 0.8:
        report["Issues"].append("Adverse conditions predicted")
    
    return report


# Function to update the report with names
def update_report_with_names(report, all_dives):
    dive_number = report.get("Dive Number")
    dive = all_dives.loc[all_dives['dive_number'] == dive_number]
    
    if not dive.empty:
        dive_name = dive['dive_site_name'].values[0]
        trip_name = dive['trip_name'].values[0]
        report.update({
            "Dive Site": dive_name,
            "Trip": trip_name
        })
    return report

@transformer
def generate_reports(dive_data, inference_model_and_features, *args, **kwargs):
    # Convert dive_data and features to DataFrames
    dives = pd.DataFrame(dive_data['parse_divelog'][0]).groupby(by=['dive_number']).first().reset_index()
    features = pd.DataFrame(inference_model_and_features['feature_engineering'][0])
    
    # Load the trained model
    model = joblib.load(inference_model_and_features['model_training'][0]['filename'])
    
    reports = []
    for index, dive_features in features.iterrows():
        report = generate_report(dive_features, model)
        report = update_report_with_names(report, dives)
        reports.append(report)
    return pd.DataFrame(reports)
