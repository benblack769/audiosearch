from ..utils.load_dataset import hex64_dataset_to_ndarray, hex64_to_ndarray
import numpy as np
import base64
import json
import pytest


def test_hex64_to_ndarray():
    vec1 = np.array([1.0,0,1.5])
    key1 = base64.b64encode(vec1.tobytes()).decode("utf-8")
    print(key1)
    with pytest.raises(ValueError):
        hex64_to_ndarray(key1, 4)

    assert np.equal(hex64_to_ndarray(key1, 3), vec1).all()

test_hex64_to_ndarray()
def test_hex64_dataset_to_ndarray():
    vector_len = 3
    vec1 = np.array([1.0,0,1.5])
    vec2 = np.array([0,3.1,.5])
    key1 = base64.b64encode(vec1.tobytes()).decode("utf-8")
    key2 = base64.b64encode(vec2.tobytes()).decode("utf-8")
    val1 = {"result": "green"}
    val2 = [1, 2]
    data = [
        {
            "key": key1,
            "value": val1,
        },
        {
            "key": key2,
            "value": val2,
        }
    ]
    keys, values = hex64_dataset_to_ndarray(data, vector_len)

    assert np.equal(keys, np.stack([vec1,vec2])).all() and values == [val1, val2]
test_hex64_dataset_to_ndarray()
