import argparse
from .utils.load_dataset import hex64_dataset_to_ndarray
from . import app
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nearest neighbors database server.")
    parser.add_argument("dataset", type=str, help="Filename of static dataset file")
    parser.add_argument("vector_len", type=int, help="Length of vector in dataset")
    args = parser.parse_args()

    with open(args.dataset) as datafile:
        raw_dataset = json.load(datafile)
    keys, values = hex64_dataset_to_ndarray(raw_dataset, args.vector_len)
    app.config.update(
        keys=keys,
        values=values
    )
    app.run(port=8804, debug=False)
