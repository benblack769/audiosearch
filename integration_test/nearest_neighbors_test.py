import subprocess
import requests
import time
import os
from utils.safe_popen import SafePopen


def test_nearest_neighbors():
    os.environ['NN_EMBEDDING_DATASET'] = "integration_test/test_embeddings.json"
    os.environ['NN_EMBEDDING_LENGTH'] = "3"

    with SafePopen("python -m nearest_neighbors_db.start_server".split()) as proc1:
        # wait for server to open
        time.sleep(3.5)

        good_request = requests.request(
            "get",
            "http://127.0.0.1:8804/ranking",
            json={
                "query":"AAAAAAAA8D8AAAAAAAAAAAAAAAAAAPg/",
                "start_rank": 0,
                "end_rank": 10,
                "comparator": "cosine"
            }
        )
        assert good_request.json()['type'] == "SUCCESS"
        bad_request = requests.request(
            "get",
            "http://127.0.0.1:8804/ranking",
            json={
                "query":"AAAAAAAA8D8AAAAAAAAAAAAAAAAAAPg/",
                "start_rank": 0,
                "end_rank": 10,
            }
        )
        assert bad_request.json()['type'] == "FORMAT_ERROR"
        dataset_size = requests.request(
            "get",
            "http://127.0.0.1:8804/dataset_size"
        )
        assert dataset_size.json() == {
            "type": "SUCCESS",
            "size": 2,
        }
