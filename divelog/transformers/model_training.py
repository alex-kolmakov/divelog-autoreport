if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from hyperopt import hp, tpe, fmin, Trials, STATUS_OK
from xgboost import XGBClassifier
import numpy as np
import mlflow
import mlflow.sklearn
from datetime import datetime
import pandas as pd
import os

RANDOM_SEED = int(os.getenv("RANDOM_SEED", 42))
MAX_EVALUATIONS = int(os.getenv("MAX_EVALUATIONS", 100))


@transformer
def transform(data, features, *args, **kwargs):

    # Define feature columns and target
    feature_cols = [
        "avg_depth",
        "max_depth",
        "depth_variability",
        "temp_variability",
        "max_pressure",
        "pressure_variability",
        "min_ndl",
        "max_ascend_speed",
        "high_ascend_speed_count",
    ]
    X = features[feature_cols]
    y = features["rating"] - 1  # Subtract 1 to make ratings start from 0

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_SEED
    )
    print("Datasets split and prepared.")

    # Define the search space for hyperparameters
    search_space = hp.choice(
        "classifier_type",
        [
            {
                "type": "random_forest",
                "n_estimators": hp.choice("n_estimators_rf", np.arange(10, 100, 10)),
                "max_depth": hp.choice("max_depth_rf", np.arange(5, 50, 5)),
                "min_samples_split": hp.choice(
                    "min_samples_split_rf", np.arange(2, 11, 2)
                ),
            },
            {
                "type": "gradient_boosting",
                "n_estimators": hp.choice("n_estimators_gb", np.arange(10, 100, 10)),
                "max_depth": hp.choice("max_depth_gb", np.arange(3, 15, 1)),
                "learning_rate": hp.uniform("learning_rate_gb", 0.01, 0.5),
            },
            {
                "type": "xgboost",
                "n_estimators": hp.choice("n_estimators_xgb", np.arange(10, 100, 10)),
                "max_depth": hp.choice("max_depth_xgb", np.arange(3, 15, 1)),
                "learning_rate": hp.uniform("learning_rate_xgb", 0.01, 0.5),
                "gamma": hp.uniform("gamma_xgb", 0, 0.5),
            },
        ],
    )

    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://mlflow:8012")
    # Create a unique experiment name with date and description
    experiment_name = f"divelog-rating-classifier-{datetime.utcnow()}"

    # Create or get the experiment
    experiment = mlflow.get_experiment_by_name(experiment_name)
    if experiment is None:
        experiment_id = mlflow.create_experiment(experiment_name)
    else:
        experiment_id = experiment.experiment_id

    mlflow.set_experiment(experiment_name)

    # Define the objective function
    def objective(params):
        with mlflow.start_run():
            if params["type"] == "random_forest":
                model = RandomForestClassifier(
                    n_estimators=params["n_estimators"],
                    max_depth=params["max_depth"],
                    min_samples_split=params["min_samples_split"],
                    random_state=RANDOM_SEED,
                )
            elif params["type"] == "gradient_boosting":
                model = GradientBoostingClassifier(
                    n_estimators=params["n_estimators"],
                    max_depth=params["max_depth"],
                    learning_rate=params["learning_rate"],
                    random_state=RANDOM_SEED,
                )
            elif params["type"] == "xgboost":
                model = XGBClassifier(
                    n_estimators=params["n_estimators"],
                    max_depth=params["max_depth"],
                    learning_rate=params["learning_rate"],
                    gamma=params["gamma"],
                    random_state=RANDOM_SEED,
                    use_label_encoder=False,
                )

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_prob = model.predict_proba(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred, average="weighted")
            recall = recall_score(y_test, y_pred, average="weighted")
            roc_auc = roc_auc_score(
                y_test, y_prob, multi_class="ovr", average="weighted"
            )

            # Log parameters and metrics
            mlflow.log_param("model_type", params["type"])
            for key, value in params.items():
                if key != "type":
                    mlflow.log_param(key, value)
            mlflow.log_metric("accuracy", accuracy)
            mlflow.log_metric("precision", precision)
            mlflow.log_metric("recall", recall)
            mlflow.log_metric("roc_auc", roc_auc)
            mlflow.sklearn.log_model(model, "model")

            return {
                "loss": -roc_auc - accuracy,
                "status": STATUS_OK,
                "model": model,
                "run_id": mlflow.active_run().info.run_id,
            }

    print("Search ranges for models and objective func defined.")

    # Perform hyperparameter optimization
    trials = Trials()
    print("Started training and looking for the best possible function..")
    best = fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=MAX_EVALUATIONS,
        trials=trials,
    )

    best_model = trials.best_trial["result"]["model"]
    best_run_id = trials.best_trial["result"]["run_id"]

    # Register the best model
    model_name = "divelog_rating_classifier"
    model_uri = f"runs:/{best_run_id}/model"
    registration_result = mlflow.register_model(model_uri, model_name)
    # Make predictions on the testing set with the best model
    y_pred = best_model.predict(X_test)
    y_prob = best_model.predict_proba(X_test)

    # Evaluate the best model
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    roc_auc = roc_auc_score(y_test, y_prob, multi_class="ovr", average="weighted")

    model_performance = {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "roc_auc": roc_auc,
        "model_path": f"models:/{model_name}/{registration_result.version}",
    }

    return model_performance


@test
def test_output(output, *args) -> None:
    """
    Testing that model is created and can be pulled.
    """
    assert output is not None, "The output is undefined"
    try:
        model_path = mlflow.sklearn.load_model(model_uri=output["model_path"])
    except Exception:
        model_path = None
    assert model_path is not None
