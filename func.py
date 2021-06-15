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
        "values": df.describe().values.tolist(),
        "columns": df.describe().columns.tolist(),
        "index": df.describe().index.tolist()
    }


def get_charts(dataset, charts):
    data = {
        "bars": [

        ],
        "lines": [

        ],
        "pies": [

        ]
    }

    for chart in charts:
        # if chart['type'] == 'bar' or chart['type'] == 'line':
        pack = []
        labels = np.array([])

        for col_chart in chart['data']:
            df = dataset[col_chart]

            count = dict(Counter(df))
            label = col_chart
            dataset_data = list(count.values())

            chart = {
                'label': label,
                'data': dataset_data,
                'borderWidth': 1
            }
            labels = np.append(labels, np.array(list(count.keys())))
            pack.append(chart)

        all = {
            "labels": list(set(labels.tolist())),
            "datasets": pack,
        }
        chart['type'].append(all)
        # else:
        #     print('other')

    return data
