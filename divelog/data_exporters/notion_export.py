if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
import joblib
import pandas as pd
from divelog.utils.notion_helpers import add_or_update_page


@data_exporter
def export_data(reports, *args, **kwargs):

    for index, report in reports.iterrows():
        add_or_update_page(report)

