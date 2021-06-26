import subprocess

class SafePopen:
    def __init__(self, *args, **kwargs):
        self.proc = subprocess.Popen(*args, **kwargs)

    def __enter__(self):
        return self.proc

    def __exit__(self, type, value, traceback):
        self.proc.kill()


with SafePopen("python -m nearest_neighbors_db.start_server integration_test/test_embeddings.json 3".split()) as proc1:
    pass
