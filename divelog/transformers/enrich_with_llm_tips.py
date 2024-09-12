import openai
import lancedb
import pandas as pd
import os
from openai import OpenAI

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def retrieve_context_from_lancedb(dbtable, question, top_k=10):

    query_results = dbtable.search(question, query_type="hybrid").to_pandas()
    results = query_results.sort_values("_relevance_score", ascending=True).nlargest(
        top_k, "_relevance_score"
    )
    context = "\n".join(results["value"])

    return context


@transformer
def transform(reports_data, dlt_pipeline, *args, **kwargs):

    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
    )
    db = lancedb.connect(".lancedb")
    table_name = dlt_pipeline["dlt_pipeline"][0]
    dbtable = db.open_table(table_name)

    def update_report_with_llm_tip(report):

        question = (
            f"Dive had an average depth of {report['Average Depth']} meters "
            f"with a maximum depth of {report['Maximum Depth']} meters. The depth variability was {report['Depth Variability']} meters. "
            f"The average pressure during the dive was {report['Average Pressure']} bar, reaching a maximum of {report['Maximum Pressure']} bar, "
            f"with a pressure variability of {report['Pressure Variability']} bar. The minimal no-decompression limit (NDL) was {report['Minimal NDL']} minutes. "
            f"The diver's SAC rate was {report['SAC Rate']}. There are {report['High Ascend Speed Count']} instances of high ascend speed with highest ascend speed of {report['Max Ascend Speed']} meters per minute."
        )

        context = retrieve_context_from_lancedb(dbtable, question)

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a scuba diving safety expert specializing in incident analysis. "
                    "You have access to a database of real dive incidents and guides from DAN (Divers Alert Network)."
                    "Use the following pieces of contextual information to answer the user query:"
                    f"{context}"
                ),
            },
            {
                "role": "system",
                "content": (
                    "When provided with dive data, your goal is to analyze the dive, check for mistakes made, and provide practical advice on how to improve. "
                    "Whenever possible, reference incidents and tips from the database and explain how the diver can avoid similar mistakes in the future. "
                    "Your response should be short and to the point, providing clear actionable advice. You must focus on the provided dive, but mention facts from the database using quotes when able."
                    "Do not provide advice on the points of the dive metadata that are up to standard."
                    "Only mention bad factual data from the provided data and how to act on it from the context perspective."
                    "YOU MUST KEEP ANSWERS BELOW 500 symbols."
                ),
            },
        ]

        messages.append({"role": "user", "content": f"Dive data: '{question}'."})
        print(f"Preparing to inquire tips for dive {report['Dive Number']}")
        response = client.chat.completions.create(model="gpt-4o", messages=messages)
        return response.choices[0].message.content

    reports_data.loc[reports_data["Rating"] <= 2, "Tips"] = reports_data[
        reports_data["Rating"] <= 2
    ].apply(update_report_with_llm_tip, axis=1)
    reports_data["Tips"] = reports_data["Tips"].fillna("")
    return reports_data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
