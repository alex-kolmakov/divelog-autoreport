if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import numpy as np
import pandas as pd


# Function to calculate ascend speed and count high ascend speed instances
def calculate_ascend_speed(data):
    data['time_diff'] = data.groupby('dive_number')['time'].diff().fillna(0)
    data['depth_diff'] = data.groupby('dive_number')['depth'].diff().fillna(0)
    data['ascend_speed'] = (data['depth_diff'] / data['time_diff']) * 60  # Convert to meters per minute
    data['ascend_speed'] = data['ascend_speed'].replace([np.inf, -np.inf], np.nan).fillna(0)  # Handle infinite and NaN values

    # Calculate the maximum ascend speed per dive
    max_ascend_speed = data.groupby('dive_number')['ascend_speed'].max().reset_index()
    max_ascend_speed.rename(columns={'ascend_speed': 'max_ascend_speed'}, inplace=True)
    
    # Calculate the count of high ascend speed instances per dive
    high_ascend_speed_count = data[data['ascend_speed'] > 10].groupby('dive_number')['ascend_speed'].count().reset_index()
    high_ascend_speed_count.rename(columns={'ascend_speed': 'high_ascend_speed_count'}, inplace=True)

    # Merge the two results
    ascend_speed_features = pd.merge(max_ascend_speed, high_ascend_speed_count, on='dive_number', how='left')
    ascend_speed_features['high_ascend_speed_count'] = ascend_speed_features['high_ascend_speed_count'].fillna(0)
    
    return ascend_speed_features

# Define criteria for adverse conditions
def label_adverse_conditions(features_df):
    features_df['adverse_conditions'] = (
        (features_df['sac_rate'] > 16) &  # Example threshold for high SAC rate
        ((features_df['min_ndl'] < 10)) &  # NDL criterion
        ((features_df['high_ascend_speed_count'] > 1) | (features_df['max_ascend_speed'] > 20))
    ).astype(int)
    return features_df

@transformer
def feature_extract(data, *args, **kwargs):

    data=pd.DataFrame(data['parse_divelog'][0])
    # Calculate ascend speed features
    ascend_speed_features = calculate_ascend_speed(data)

    features = data.groupby('dive_number').agg(
        avg_depth=('depth', 'mean'),
        max_depth=('depth', 'max'),
        depth_variability=('depth', 'std'),
        avg_temp=('temperature', 'mean'),
        max_temp=('temperature', 'max'),
        temp_variability=('temperature', 'std'),
        avg_pressure=('pressure', 'mean'),
        max_pressure=('pressure', 'max'),
        pressure_variability=('pressure', 'std'),
        min_rbt=('rbt', 'min'),
        min_ndl=('ndl', 'min'),
        sac_rate=('sac_rate', 'first')
    ).reset_index()

    # Merge the ascend speed features with other features
    features = features.merge(ascend_speed_features, on='dive_number')

    features = features.dropna()

    return label_adverse_conditions(features)

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
