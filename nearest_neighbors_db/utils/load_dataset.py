import base64
import numpy as np


def hex64_to_ndarray(vector_str, vector_len):
    key = np.frombuffer(base64.decodebytes(vector_str.encode("utf-8")))
    if len(key) != vector_len:
        raise ValueError(f"key is not right length. Expected length {vector_len} got length {len(key)}")
    return key


def hex64_dataset_to_ndarray(dataset_dict, vector_len):
    keys = []
    values = []
    for item in dataset_dict:
        keys.append(hex64_to_ndarray(item['key'], vector_len))
        values.append(item['value'])
    return np.stack(keys), values
