from flask import request, send_from_directory
from werkzeug.utils import secure_filename
import json
import os

import pandas as pd

from func import *


def route(app):
    host = 'http://127.0.0.1:5000'

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/analytics/load_file/<format_dataset>', methods=['POST'])
    def load_file(format_dataset):
        if 'file' not in request.files:
            return err("Bad request")

        file = request.files['file']

        allowed_format = ['csv', 'excel']
        format_file = file.filename.split('.')[len(file.filename.split('.')) - 1]

        if format_file != format_dataset or format_file not in allowed_format:
            return err("Dataset is bad format")

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        try:
            dataset = pd.read_csv(os.path.join(f'./uploads/', filename))
        except:
            return err("Dataset not found")

        data = {}
        try:
            for col in dataset.columns:
                data[col] = [float(val) for val in dataset[col].values[:5]]
        except:
            return err('Dataset values is not number')

        columns = [col for col in dataset.columns]

        return json.dumps({
            'status': True,
            'data': {
                'message': "File load",
                'filename': filename,
                'dataset': {
                    'columns': columns,
                    'data': data
                }
            }
        })

    @app.route('/analytics/result', methods=['POST'])
    def result():
        dataset_name = request.form['filename']
        if dataset_name.strip() == '':
            return
        try:
            dataset = pd.read_csv(os.path.join(f'./uploads/', dataset_name))
        except:
            return err("Dataset not found")

        print(dataset)

        correlation(dataset)

        return json.dumps({
            'status': True,
            'data': {
                'message': "Analytics ready"
            }
        })
