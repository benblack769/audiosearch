import os
import datetime


def get_files_to_clear(folder, file_timeout):
    cur_time = datetime.datetime.now()

    files_to_remove = []
    for fname in os.listdir(folder):
        path = os.path.join(folder, fname)
        mtime = datetime.datetime.fromtimestamp(os.stat(path).st_mtime)
        time_since_upload = cur_time - mtime
        if time_since_upload.seconds > file_timeout:
            files_to_remove.append(path)

    return files_to_remove
