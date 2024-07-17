import pandas as pd
import numpy as np
from divelog.transformers.feature_engineering import calculate_ascend_speed


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
