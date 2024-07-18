import pytest
import xml.etree.ElementTree as ET
import pandas as pd

# Assuming the functions are imported from the module
from divelog.transformers.parse_divelog import (
    time_to_minutes,
    extract_all_dive_profiles_refined,
)


def test_time_to_minutes():
    assert time_to_minutes("1:30") == 90
    assert time_to_minutes("0:45") == 45
    assert time_to_minutes("2:00") == 120
    assert time_to_minutes("60") == 60.0
    assert time_to_minutes("90") == 90.0


def test_extract_all_dive_profiles_refined():
    # Load the XML file
    with open("anonymized_subsurface_export.ssrf", "r") as file:
        tree = ET.parse(file)
        root = tree.getroot()

    df = extract_all_dive_profiles_refined(root)

    assert not df.empty, "The dataframe is empty"
    assert set(df.columns) == {
        "dive_number",
        "trip_name",
        "dive_site_name",
        "time",
        "depth",
        "temperature",
        "pressure",
        "rbt",
        "ndl",
        "sac_rate",
        "rating",
    }
    assert len(df) == 37882, "Dataframe should have 37882 rows"
    assert df["depth"].iloc[200] == 4.7
    assert df["rating"].iloc[200] == 4
    assert df["sac_rate"].iloc[200] == 41.418
    assert df["time"].iloc[200] == 720
