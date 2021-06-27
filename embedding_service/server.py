from flask import Flask
import json
import argparse
from audio_utils.spectrify import load_data, spectrify_audios
from embed_utils.embedder import Embedder
import yaml
import requests
import tempfile
import base64
from flask import request
import urllib.request
import shutil


app = Flask(__name__)


@app.route("/embedding", methods=["GET"])
def get_embedding():
    try:
        response_data = json.loads(request.get_data())
        url = response_data['url']
        print("downlaod start")
        with tempfile.NamedTemporaryFile(suffix=".mp3") as downloaded_file:

            response = urllib.request.urlopen(url)
            print("STATUS\n\n")
            print(response.status)
            downloaded_file.write(response.read())
            # downloaded_file.write(myfile.content)
            downloaded_file.flush()
            print('download end')

            spec_datas = [load_data(downloaded_file.name,app.config['SAMPLERATE'])]

            spec_outs = spectrify_audios(
                spec_datas,
                app.config['NUM_MEL_BINS'],
                app.config['SAMPLERATE'],
                app.config['TIME_SEGMENT_SIZE'],
            )
            spectrogram = spec_outs[0]

            embedder = Embedder(app.config['NUM_MEL_BINS'], app.config['HIDDEN_SIZE'], app.config['OUTPUT_VECTOR_SIZE'], app.config['WEIGHTS_PATH'])
            out_embedding = embedder.embed(spectrogram)
    except urllib.error.HTTPError as e:
        print(repr(e))
        return json.dumps(
            {
                "type": "URL_ERROR",
                "message": repr(e),
            }
        )
    except (ValueError, KeyError) as e:
        print(repr(e))
        return json.dumps(
            {
                "type": "FORMAT_ERROR",
                "message": repr(e),
            }
        )

    embedding_text = base64.b64encode(out_embedding.tobytes()).decode("utf-8")
    return json.dumps(
        {
            "type": "SUCCESS",
            "embedding": embedding_text,
            "size": len(out_embedding),
        }
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Service which converts a .mp3 or .wav encoded sound file and embeds it on demand")
    parser.add_argument('weights', help='Paths to trained model weights folder (saved automatically during model training in the `weights` folder)')
    parser.add_argument('config_file', help='path to sound-eval config file used to train the model')

    args = parser.parse_args()

    with open(args.config_file) as config_file:
        config = yaml.safe_load(config_file)

    weights_path = args.weights

    app.config.update(**config)
    app.config['WEIGHTS_PATH'] = weights_path

    app.run(port=8704, debug=False)
