import subprocess
import requests
import time
import os

class SafePopen:
    def __init__(self, *args, **kwargs):
        self.proc = subprocess.Popen(*args, **kwargs)

    def __enter__(self):
        return self.proc

    def __exit__(self, type, value, traceback):
        self.proc.kill()

os.environ['EMBED_WEIGHTS'] = "integration_test/weights/"
os.environ['EMBED_CONFIG'] = "integration_test/train_opt.yaml"
os.environ['NN_EMBEDDING_DATASET'] = "integration_test/test_dataset.json"
os.environ['NN_EMBEDDING_LENGTH'] = "48"

with SafePopen("python -m nearest_neighbors_db.start_server".split()) as proc1, \
     SafePopen("python embedding_service/server.py".split()) as proc2, \
     SafePopen("python search_backend/server.py".split()) as proc3, \
     SafePopen("python -m http.server".split()) as proc4:
        time.sleep(7)
        good_request = requests.request(
            "get",
            "http://127.0.0.1:8504/submit",
            data={
                "urls": ["http://127.0.0.1:8000/integration_test/test.mp3","http://127.0.0.1:8000/integration_test/test.mp3"],
                "weights": [1., -0.2],
                "start_rank": 0,
                "end_rank": 2,
                "comparator": "cosine",
            }
        )
        data = good_request.json()
        assert data['type'] == "SUCCESS"
        assert len(data['ranked']) == 2

print("all tests passed")
