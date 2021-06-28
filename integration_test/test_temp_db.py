import subprocess
import requests
import time
from utils.safe_popen import SafePopen

def test_temp_db():
    with SafePopen("python temp_db/server.py".split()) as proc1:
        # wait for server to open
        time.sleep(5)

        good_request = requests.request(
            "post",
            "http://127.0.0.1:8604/upload",
            files={
                "file": open("integration_test/test.mp3", 'rb')
            }
        )
        request_result = good_request.json()
        assert request_result['type'] == "SUCCESS"
        id = request_result['id']
        good_download_request = requests.request(
            "get",
            "http://127.0.0.1:8604/download/"+id
        )
        print(good_download_request.content)
        assert len(good_download_request.content) > 1000
