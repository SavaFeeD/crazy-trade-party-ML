from flask import request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import json
import os

import pandas as pd
import numpy as np

from func import *


def route(app):
    host = 'http://127.0.0.1:5000'

    @app.after_request
    def after_request(response):
        response.headers['Access-Control-Allow-Origin'] = "*"
        response.headers.add("Access-Control-Allow-Headers", "*")
        response.headers.add("Access-Control-Allow-Methods", "*")
        return response

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/analytics/load_file', methods=['POST'])
    def load_file():
        if 'file' not in request.files:
            return err("Bad request")
        file = request.files['file']

        allowed_format = ['csv', 'excel']

        format_file = file.filename.split('.')[len(file.filename.split('.')) - 1]

        if format_file not in allowed_format:
            return err("Dataset is bad format")

        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return jsonify({
            'status': True,
            'body': {
                'message': "File load",
                'filename': filename
            }
        })

    @app.route('/analytics/get_info_dataset', methods=['GET'])
    def get_info_for_anal():
        file = None

        if 'filename' not in request.args:
            return err("Bad request: filename is not found")
        try:
            dataset = pd.read_csv(os.path.join(f'./uploads/', request.args['filename']))
        except:
            return err("Bad request: file with filename is not found")

        if len(dataset.columns) > 8:
            columns = [col for col in dataset.columns[:4]]
            columns.extend([col for col in dataset.columns[-4:]])
        else:
            columns = [col for col in dataset.columns]

        data = []
        data_ = []
        type_table = None

        def processing(cell):
            if type(cell) == str:
                cell = cell.replace(',', '.')
                try:
                    float(cell)
                except:
                    return err('Dataset error: give me only int and float data')

            return cell

        for col in dataset.columns:
            dataset[col] = dataset[col].apply(processing)
            dataset[col] = dataset[col].astype(float)

        try:
            if len(dataset[columns[0]].values) > 3:

                if len(dataset.columns) > 8:
                    # big - cols, big - rows (test dataset: heart)
                    start = [float(val) for val_arr in [dataset.iloc[i].values for i in range(2)] for val in val_arr]
                    start1 = start[:int(len(start) / 2)]
                    start2 = start[int(len(start) / 2):]
                    start = [start1, start2]
                    start_split = []
                    for s in start:
                        start_split.append([s[:4], s[-4:]])
                    start = start_split

                    end = [float(val) for val in dataset.iloc[len(dataset.columns)].values]
                    end = [end[:4], end[-4:]]

                    type_table = "big_to_big"
                else:
                    # small - cols, big - rows (test dataset: big)
                    start = [dataset.iloc[i].values.tolist() for i in range(2)]
                    end = [float(val) for val in dataset.iloc[len(dataset.columns)].values]

                    type_table = "small_to_big"

                data_ = {
                    "start": start,
                    "end": end
                }
            else:
                if len(dataset.columns) > 8:
                    #  big - cols, small - rows (test dataset: small-row, big-cols)
                    start = [dataset.iloc[i].values.tolist() for i in range(len(dataset[dataset.columns[0]].values))]
                    start_ = []
                    for row in start:
                        start_.append([row[:4], row[-4:]])
                    start = start_

                    type_table = "big_to_small"
                else:
                    #  small - cols, small - rows (test dataset: small)
                    start = [dataset.iloc[i].values.tolist() for i in range(len(dataset[dataset.columns[0]].values))]

                    type_table = "small_to_small"

                data_ = {
                    "start": start,
                    "end": None
                }
        except:
            return err('Dataset processing error')

        if len(columns) == 8:
            columns = [columns[0:4], columns[4:8]]

        filename = request.args['filename']

        return jsonify({
            'status': True,
            'body': {
                "type_table": type_table,
                'filename': filename,
                'columns_len': len(dataset.columns),
                'row_len': len(dataset[dataset.columns[0]].values),
                'all_columns': [col for col in dataset.columns],
                'dataset': {
                    'columns': columns,
                    'data': data_
                }
            }
        })

    @app.route('/analytics/result', methods=['POST'])
    def result():
        data = json.loads(request.data)

        dataset_name = data['file']
        desc = data['desc']
        charts = data['chart']

        if dataset_name.strip() == '':
            return
        try:
            dataset = pd.read_csv(os.path.join(f'./uploads/', dataset_name))
        except:
            return err("Dataset not found")

        if desc:
            describe = description(dataset, desc)
        else:
            describe = []

        if charts:
            print(dataset)
            charts = get_charts(dataset, charts)
        else:
            charts = []

        return jsonify({
            'status': True,
            'body': {
                'message': "Analytics ready",
                'describe': describe,
                'charts': charts
            }
        })
