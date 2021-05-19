import pandas as pd
import numpy as np
import json
from flask import jsonify
from collections import Counter


def err(message):
    return jsonify({
        'status': False,
        'data': {
            'message': f"{message}"
        }
    })


def description(dataset, fields):
    pd.set_option('display.max_columns', None)

    df = dataset[fields]

    return {
        "values": df.apply(pd.DataFrame.describe, axis=1).values.tolist(),
        "columns": df.describe().columns.tolist(),
        "index": df.describe().index.tolist()
    }


def get_charts(dataset, charts):
    data = []

    for chart in charts:
        # if chart.type == 'line':
        #     labels = dataset[charts.data.x]
        #     dataset_labels = f'{charts.data.x}/{charts.data.y}'
        #     dataset_data = dataset[charts.data.y]
        #
        #     chart = {
        #         'labels': labels,
        #         'datasets': {
        #             'labels': dataset_labels,
        #             'data': dataset_data
        #         }
        #     }
        #     data.append(chart)
        # else:
        for col_chart in chart.data:
            df = dataset[col_chart]
            print(Counter(df))

            labels = []
            dataset_labels = chart.type
            dataset_data = []

            chart = {
                'labels': labels,
                'datasets': {
                    'labels': dataset_labels,
                    'data': dataset_data
                }
            }
            data.append(chart)

    return data
