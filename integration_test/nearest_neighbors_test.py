import subprocess
import requests
import time

class SafePopen:
    def __init__(self, *args, **kwargs):
        self.proc = subprocess.Popen(*args, **kwargs)

    def __enter__(self):
        return self.proc

    def __exit__(self, type, value, traceback):
        self.proc.kill()


with SafePopen("python -m nearest_neighbors_db.start_server integration_test/test_embeddings.json 3".split()) as proc1:
    # wait for server to open
    time.sleep(1.5)

    good_request = requests.request(
        "get",
        "http://127.0.0.1:8804/ranking",
        json={
            "query":"AAAAAAAA8D8AAAAAAAAAAAAAAAAAAPg/",
            "start_rank": 0,
            "end_rank": 10,
            "comparitor": "cosine"
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


print("All tests passed!")
