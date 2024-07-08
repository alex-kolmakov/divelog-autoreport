if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
import mlflow
import pandas as pd


# Function to generate the report
def generate_report(dive_features, model):
    dive_number = dive_features["dive_number"]

    # Prepare the feature vector for the model
    feature_vector = dive_features[
        [
            "avg_depth",
            "max_depth",
            "depth_variability",
            "avg_pressure",
            "max_pressure",
            "pressure_variability",
            "min_ndl",
            "max_ascend_speed",
            "high_ascend_speed_count",
        ]
    ].values.reshape(1, -1)

    # Predict the rating
    predicted_rating = (
        model.predict(feature_vector)[0] + 1
    )  # Adding 1 to match the original rating scale

    report = {
        "Dive Number": dive_number,
        "Average Depth": dive_features["avg_depth"],
        "Maximum Depth": dive_features["max_depth"],
        "Depth Variability": dive_features["depth_variability"],
        "Average Pressure": dive_features["avg_pressure"],
        "Maximum Pressure": dive_features["max_pressure"],
        "Pressure Variability": dive_features["pressure_variability"],
        "Minimal NDL": dive_features["min_ndl"],
        "SAC Rate": dive_features["sac_rate"],
        "Rating": predicted_rating,
        "Issues": [],
    }

    # Potential issues
    if predicted_rating <= 2:
        report["Issues"].append("Low rating predicted")

    return report


# Function to update the report with names
def update_report_with_names(report, all_dives):
    dive_number = report.get("Dive Number")
    dive = all_dives.loc[all_dives["dive_number"] == dive_number]
    if not dive.empty:
        dive_name = dive["dive_site_name"].values[0]
        trip_name = dive["trip_name"].values[0]
        report.update({"Dive Site": dive_name, "Trip": trip_name})
    else:
        return None
    return report


mlflow.set_tracking_uri("http://mlflow:8012")


@transformer
def generate_reports(inference_model_and_features, dive_data, *args, **kwargs):
    # Convert dive_data and features to DataFrames
    dives = (
        pd.DataFrame(dive_data["parse_divelog"][0])
        .groupby(by=["dive_number"])
        .first()
        .reset_index()
    )
    features = pd.DataFrame(inference_model_and_features["feature_engineering"][0])

    model = mlflow.sklearn.load_model(
        model_uri=inference_model_and_features["model_training"][0]["model_path"]
    )

    reports = []
    for index, dive_features in features.iterrows():
        report = generate_report(dive_features, model)
        report = update_report_with_names(report, dives)
        if report:
            reports.append(report)

    reports = pd.DataFrame(reports)

    return pd.DataFrame(reports)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
