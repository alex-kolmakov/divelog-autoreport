import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
from divelog.transformers.feature_engineering import calculate_ascend_speed
from divelog.transformers.parse_divelog import extract_all_dive_profiles_refined
from divelog.transformers.feature_engineering import feature_extract


def test_calculate_ascend_speed():
    # Sample data setup
    data = pd.DataFrame(
        {
            "dive_number": [1, 1, 1, 2, 2],
            "time": [0, 1, 2, 0, 1],
            "depth": [20, 15, 10, 30, 20],
        }
    )

    # Expected results setup
    expected_max_ascend_speed = pd.DataFrame(
        {"dive_number": [1, 2], "max_ascend_speed": [300.0, 600.0]}
    )

    expected_high_ascend_speed_count = pd.DataFrame(
        {"dive_number": [1, 2], "high_ascend_speed_count": [2, 1]}
    )

    expected_output = pd.merge(
        expected_max_ascend_speed,
        expected_high_ascend_speed_count,
        on="dive_number",
        how="left",
    )
    expected_output["high_ascend_speed_count"] = expected_output[
        "high_ascend_speed_count"
    ].fillna(0)

    # Running the function
    result = calculate_ascend_speed(data)

    # Assertions
    pd.testing.assert_frame_equal(result, expected_output)


def test_feature_extract():
    # Load the XML file
    with open("anonymized_subsurface_export.ssrf", "r") as file:
        tree = ET.parse(file)
        root = tree.getroot()

    data = {"parse_divelog": [extract_all_dive_profiles_refined(root)]}
    features = feature_extract(data)

    assert not features.empty, "The features dataframe is empty"
    expected_columns = {
        "dive_number",
        "avg_depth",
        "max_depth",
        "depth_variability",
        "avg_temp",
        "max_temp",
        "temp_variability",
        "avg_pressure",
        "max_pressure",
        "pressure_variability",
        "min_ndl",
        "sac_rate",
        "rating",
        "max_ascend_speed",
        "high_ascend_speed_count",
        "adverse_conditions",
    }
    assert set(features.columns) == expected_columns
    assert features["adverse_conditions"].isin([0, 1]).all()
