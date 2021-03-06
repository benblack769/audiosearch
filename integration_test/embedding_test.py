import subprocess
import requests
import time
import os
from utils.safe_popen import SafePopen

def test_embedding():
    os.environ['EMBED_WEIGHTS'] = "integration_test/weights/"
    os.environ['EMBED_CONFIG'] = "integration_test/train_opt.yaml"

    with SafePopen("python embedding_service/server.py".split()) as proc1, \
         SafePopen("python -m http.server".split()) as proc2:

        # wait for server to open
        time.sleep(10)

        good_request = requests.request(
            "get",
            "http://127.0.0.1:8704/embedding",
            json={
                "url":"http://127.0.0.1:8000/integration_test/test.mp3",
            }
        )
        assert good_request.json()['type'] == "SUCCESS"
        bad_format_request = requests.request(
            "get",
            "http://127.0.0.1:8704/embedding",
            json={
                "query":"AAAAAAAA8D8AAAAAAAAAAAAAAAAAAPg/",
            }
        )
        assert bad_format_request.json()['type'] == "FORMAT_ERROR"
        bad_url_error = requests.request(
            "get",
            "http://127.0.0.1:8704/embedding",
            json={
                "url":"http://s3-us-west-2.amazonaws.com/fma-dataset-embeddings/mp3_files/020/120373.mp3",
            }
        )
        assert bad_url_error.json()['type'] == "URL_ERROR"
