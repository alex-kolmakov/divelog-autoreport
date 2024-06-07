if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Define criteria for adverse conditions
def label_adverse_conditions(features_df):
    features_df['adverse_conditions'] = (
        (features_df['max_depth'] > 35) |  # Example threshold for extreme depth
        (features_df['depth_variability'] > 9) |  # Example threshold for high depth variability
        (features_df['sac_rate'] > 20.0) |  # Example threshold for high SAC rate
        (
            (features_df['min_ndl'] > 0) & 
            (features_df['min_ndl'] < 2)
        )  # Example threshold for low NDL
    ).astype(int)
    return features_df

@transformer
def feature_extract(data, *args, **kwargs):
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
        sac_rate=('sac_rate', 'first')  # SAC rate should be the same for each dive
    ).reset_index()

    features = features.dropna()

    return label_adverse_conditions(features)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
