import argparse
from .utils.load_dataset import hex64_dataset_to_ndarray
from . import app
import json
from . import rest_fns
import os

if __name__ == "__main__":
    dataset_name = os.environ['NN_EMBEDDING_DATASET']
    vector_len = int(os.environ['NN_EMBEDDING_LENGTH'])

    with open(dataset_name) as datafile:
        raw_dataset = json.load(datafile)
    keys, values = hex64_dataset_to_ndarray(raw_dataset, vector_len)
    app.config.update(
        KEYS=keys,
        VALUES=values,
        VECTOR_LEN=vector_len
    )
    app.run(port=8804, debug=False)
