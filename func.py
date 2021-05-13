import pandas as pd
import json
from flask import jsonify


def err(message):
    return jsonify({
        'status': False,
        'data': {
            'message': f"{message}"
        }
    })


def correlation(dataset):
    return dataset
