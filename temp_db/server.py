from flask import Flask, flash, request, redirect, url_for, send_from_directory
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
import re
from utils.clear_old_files import get_files_to_clear
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


@app.route("/download/<file_id>", methods=["GET"])
def download_file(file_id):
    print(file_id)
    abs_path = os.path.join(app.root_path, app.config['AUDIO_FOLDER'])
    print(abs_path)
    # safe metho, no need for sanitizing
    return send_from_directory(directory=abs_path, filename=file_id)


@app.route("/upload", methods=["POST"])
def upload_file():
    # if 'file' not in request.files:
    #     return json.dumps(
    #         {
    #             "type": "BAD_REQUEST_FORMAT",
    #         }
    #     )

    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    # if file.filename == '':
    #     return json.dumps(
    #         {
    #             "type": "NO_FILE",
    #         }
    #     )
    _, extension = os.path.splitext(file.filename)

    # clears old files
    abs_path = os.path.join(app.root_path, app.config['AUDIO_FOLDER'])
    files_to_remove = get_files_to_clear(abs_path, app.config['TEMPFILE_TIMEOUT'])
    for path in files_to_remove:
        os.remove(path)

    assigned_id = base64.b16encode(os.urandom(16)).decode("utf-8") + extension
    abs_path = os.path.join(app.root_path, app.config['AUDIO_FOLDER'], assigned_id)
    file.save(abs_path)

    return json.dumps(
        {
            "type": "SUCCESS",
            "id": assigned_id
        }
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Service which converts a .mp3 or .wav encoded sound file and embeds it on demand")
    parser.add_argument('--audio_folder', default="static/store/", help='Paths to folder to put audio files into')

    args = parser.parse_args()


    app.config["AUDIO_FOLDER"] = args.audio_folder
    # limits file upload size to 20MB
    app.config['MAX_CONTENT_LENGTH'] = 20*2**20
    # Files time out after 1 hour.
    app.config['TEMPFILE_TIMEOUT'] = 60*60

    abs_path = os.path.join(app.root_path, app.config['AUDIO_FOLDER'])

    if os.path.exists(abs_path):
        shutil.rmtree(abs_path)

    os.makedirs(abs_path)

    app.run(port=8604, debug=False)
