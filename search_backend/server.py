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
import numpy as np
import re


app = Flask(__name__)

def get_query(urls, weights):
    if len(urls) != len(weights) or len(urls) < 1:
        raise ValueError("urls and weights must have equal lengths")

    embeddings = []
    for url in urls:
        response = requests.get("http://127.0.0.1:8704/embedding", json={
            "url": url
        })
        data = response.json()
        embed = np.frombuffer(base64.decodebytes(data['embedding'].encode("utf-8")))
        embeddings.append(embed)
    query = np.zeros_like(embeddings[0])
    for embed, weight in zip(embeddings, weights):
        print("EMBEDDING")
        print(embed)
        print(weight)
        query += embed * weight
    return query

def get_ranking(query, start_rank, end_rank, comparator):
    response = requests.get("http://127.0.0.1:8804/ranking", json={
        "query": base64.b64encode(query.tobytes()).decode("utf-8"),
        "comparator": comparator,
        "start_rank": start_rank,
        "end_rank": end_rank,
    })
    print(response.content)
    return response.json()['values']

@app.route("/submit", methods=["GET"])
def upload_file():
    start_rank = int(request.form.get("start_rank"))
    end_rank = int(request.form.get("end_rank"))
    comparator = request.form.get("comparator")
    urls = request.form.getlist('urls')
    weights = [float(w) for w in request.form.getlist('weights')]
    query = get_query(
        urls,
        weights,
    )
    ranking = get_ranking(query, start_rank, end_rank, comparator)
    return json.dumps(
        {
            "type": "SUCCESS",
            "ranked": ranking,
        }
    )

if __name__ == "__main__":
    app.run(port=8504, debug=False)
