import os

import openai
import lancedb
import pandas as pd

import re
import mlflow

if "custom" not in globals():
    from mage_ai.data_preparation.decorators import custom
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test

MODEL = os.getenv("LLM_MODEL", "gpt-3.5-turbo")
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_score(text):
    match = re.search(r"\s*(\d+)", text)
    if match:
        return float(match.group(1))
    else:
        return None


def retrieve_context_from_lancedb(dbtable, question, prompt):
    """Retrieve context and mean relevance score based on the provided prompt."""
    query_results = dbtable.search(question, query_type="hybrid").to_pandas()
    results = query_results.sort_values("_relevance_score", ascending=True).nlargest(
        10, "_relevance_score"
    )
    context = "\n".join(results["value"])
    mean_relevance_score = results["_relevance_score"].max()
    return context, mean_relevance_score


def create_text_report(report):
    """Convert dive report data into text."""
    return (
        f"Average depth {report['Average Depth']} meters, "
        f"Maximum depth {report['Maximum Depth']} meters, "
        f"Depth variability {report['Depth Variability']} meters, "
        f"SAC rate {report['SAC Rate']}, "
        f"High Speed Ascend instances {report['High Ascend Speed Count']}, "
        f"Max Ascend Speed {report['Max Ascend Speed']} meters per min, "
        f"Minimal NDL {report['Minimal NDL']} minutes."
    )


def select_best_context_prompt(dbtable, report):
    """Craft and evaluate multiple context retrieval prompts to select the best one."""
    question = create_text_report(report)

    prompts = [
        "Given the dive details: {question}, provide related incidents that match any of mentioned metrics.",
        "Find relevant incidents and tips related to the dive described: {question}.",
        "Search the DAN incident database for relevant data on this dive: {question}.",
    ]

    best_prompt = None
    best_max_relevance = -float("inf")

    for prompt in prompts:
        with mlflow.start_run() as run:
            full_prompt = prompt.replace("{question}", question)
            context, max_relevance_score = retrieve_context_from_lancedb(
                dbtable, question, full_prompt
            )
            mlflow.log_param("context_prompt", prompt)
            mlflow.log_metric("max_relevance_score", max_relevance_score)
            if max_relevance_score > best_max_relevance:
                best_max_relevance = max_relevance_score
                best_prompt = prompt
    return best_prompt


def evaluate_prompt_with_llm_judge(context, response):
    """Evaluate a prompt using faithfulness based on the provided context."""
    # Faithfulness scoring: how factually consistent the response is with the context (ignoring the input)
    faithfulness_prompt = (
        f"How factually consistent is the following response with the provided context? "
        f"Context: {context}\nResponse: {response}. Score faithfulness based on how much of the output can be directly inferred from the context, ignoring the input. "
        f"Use the following rubric: 1 (no claims inferred), 2 (some claims inferred but mostly inconsistent), 3 (half or more inferred), "
        f"4 (most inferred with little unsupported info), 5 (all claims directly supported)."
    )

    faithfulness_score = extract_score(
        client.chat.completions.create(
            model=MODEL, messages=[{"role": "user", "content": faithfulness_prompt}]
        )
        .choices[0]
        .message.content
    )

    return faithfulness_score


def select_best_full_prompt(context, report):
    """Combine context and question into multiple full prompts and select the best one based on faithfulness and mean relevance from LanceDB."""
    question = create_text_report(report)

    prompts = [
        "Analyze the following dive data and provide advice. Context: {context}. Dive data: {question}.",
        "Using the provided context: {context}, evaluate the dive data: {question} and offer practical advice.",
        "With the context: {context}, analyze the dive data: {question} and give recommendations.",
        "Given the context from DAN: {context}, and the dive data: {question}, what should be improved?",
    ]

    best_prompt = None
    best_overall_score = -float("inf")

    for prompt in prompts:
        with mlflow.start_run() as run:
            full_question_to_llm = prompt.replace("{context}", context).replace(
                "{question}", question
            )
            response = (
                client.chat.completions.create(
                    model=MODEL,
                    messages=[{"role": "user", "content": full_question_to_llm}],
                )
                .choices[0]
                .message.content
            )
            faithfulness_score = evaluate_prompt_with_llm_judge(context, response)
            mlflow.log_param("prompt", prompt)
            mlflow.log_metric("faithfulness_score", faithfulness_score)
            if faithfulness_score > best_overall_score:
                best_overall_score = faithfulness_score
                best_prompt = prompt

    return best_prompt, best_overall_score


@custom
def select_best_prompts(*args, **kwargs):
    db = lancedb.connect(".lancedb")
    dbtable = db.open_table("dan_articles___texts")

    test_report = {
        "Dive Number": 1,
        "Average Depth": 15.8,
        "Maximum Depth": 20,
        "Depth Variability": 7.4,
        "Average Pressure": 76.9,
        "Maximum Pressure": 209,
        "Pressure Variability": 10,
        "Minimal NDL": 14,
        "SAC Rate": 15,
        "Max Ascend Speed": 13,
        "High Ascend Speed Count": 1,
        "Rating": 1,
    }
    mlflow.set_tracking_uri("http://mlflow:8012")
    mlflow.set_experiment("Best context relevant prompt")

    # Step 1: Select the best context retrieval prompt
    best_context_prompt = select_best_context_prompt(dbtable, test_report)
    context, max_relevance_score = retrieve_context_from_lancedb(
        dbtable, create_text_report(test_report), best_context_prompt
    )
    print("Best max relevance", max_relevance_score)
    print("Best Context Prompt: ", best_context_prompt)

    mlflow.set_experiment("Best full prompt")
    # # # Step 2: Select the best full prompt (context + question)
    best_full_prompt, best_overall_score = select_best_full_prompt(context, test_report)
    print("Best fathfullness score", best_overall_score)
    print("Best Full Prompt: ", best_full_prompt)

    return ("dan_articles___texts", best_context_prompt, best_full_prompt)
