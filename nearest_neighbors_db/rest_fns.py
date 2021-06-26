from .utils.load_dataset import hex64_to_ndarray
from . import app
import json
from flask import request
from .utils.metric import compute_metric
import numpy as np



@app.route("/ranking", methods=["GET"])
def get_ranking():
    try:
        response_data = json.loads(request.get_data())

        query = response_data["query"]
        start_idx = int(response_data["start_rank"])
        end_idx = int(response_data["end_rank"])
        comparitor = response_data["comparitor"]

        query_vec = hex64_to_ndarray(query, app.config['VECTOR_LEN'])

        keys = app.config['KEYS']
        values = app.config['VALUES']
        metric = compute_metric(keys, query_vec, comparitor)
        ranking = np.argsort(metric)
        indicies = ranking[start_idx:max(end_idx, len(ranking))]
        selected_values = [values[i] for i in indicies]

    except (ValueError, KeyError, json.decoder.JSONDecodeError) as e:
        print(repr(e))
        return json.dumps(
            {
                "type": "FORMAT_ERROR",
                "message": str(e),
            }
        )

    return json.dumps(
        {
            "type": "SUCCESS",
            "values": selected_values,
        }
    )



@app.route("/dataset_size", methods=["GET"])
def get_dataset_size():
    return json.dumps(
        {
            "type": "SUCCESS",
            "size": len(app.config['KEYS']),
        }
    )
