import pandas as pd
import json


def err(message):
    return json.dumps({
        'status': False,
        'data': {
            'message': f"{message}"
        }
    })


def correlation(dataset):
    return dataset
