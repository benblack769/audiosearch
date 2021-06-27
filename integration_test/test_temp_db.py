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


with SafePopen("python temp_db/server.py".split()) as proc1:
    # wait for server to open
    time.sleep(3)

    good_request = requests.request(
        "post",
        "http://127.0.0.1:8604/upload",
        files={
            "file": open("integration_test/test.mp3", 'rb')
        }
    )
    request_result = good_request.json()
    assert request_result['type'] == "SUCCESS"
    
print("all tests passed")
