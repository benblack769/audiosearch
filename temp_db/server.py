from flask import Flask, flash, request, redirect, url_for
import json
import argparse
import yaml
import requests
import tempfile
import base64
import urllib.request
import shutil
import os
import base64
import os
from utils.clear_old_files import get_files_to_clear


app = Flask(__name__)


@app.route("/download", methods=["GET"])
def download_file():
    pass


@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return json.dumps(
            {
                "type": "BAD_REQUEST_FORMAT",
            }
        )

    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return json.dumps(
            {
                "type": "NO_FILE",
            }
        )

    # clears old files
    files_to_remove = get_files_to_clear(app.config["AUDIO_FOLDER"], app.config['TEMPFILE_TIMEOUT'])
    for path in files_to_remove:
        os.remove(path)

    assigned_id = base64.b16encode(os.urandom(16)).decode("utf-8") + ".mp3"
    file.save(os.path.join(app.config["AUDIO_FOLDER"], assigned_id))

    return json.dumps(
        {
            "type": "SUCCESS",
        }
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Service which converts a .mp3 or .wav encoded sound file and embeds it on demand")
    parser.add_argument('--audio_folder', default="store", help='Paths to folder to put audio files into')

    args = parser.parse_args()

    if os.path.exists(args.audio_folder):
        shutil.rmtree(args.audio_folder)

    os.makedirs(args.audio_folder)


    app.config["AUDIO_FOLDER"] = args.audio_folder
    # limits file upload size to 20MB
    app.config['MAX_CONTENT_LENGTH'] = 20*2**20
    # Files time out after 1 hour.
    app.config['TEMPFILE_TIMEOUT'] = 60*60

    app.run(port=8604, debug=False)
