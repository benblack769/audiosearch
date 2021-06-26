import base64
import numpy as np

def hex64_dataset_to_ndarray(dataset_dict, vector_len):
    keys = []
    values = []
    for item in dataset_dict:
        key = np.frombuffer(base64.decodebytes(item['key'].encode("utf-8")))
        if len(key) != vector_len:
            raise ValueError(f"key is not right length. Expected length {vector_len} got length {len(key)}")
        keys.append(key)
        values.append(item['value'])
    return np.stack(keys), values
