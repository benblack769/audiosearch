from ..utils.metric import compute_metric
import numpy as np


def test_metrics():
    keys = np.array([
        [1,0,0],
        [2,0,0],
        [0,1,0],
        [1,1,0],
    ],dtype=float)
    query1 = np.array([1,0,0],dtype=float)
    query2 = np.array([0,1,0],dtype=float)
    query3 = np.array([1,1,0],dtype=float)
    assert compute_metric(keys, query1, "cosine")[0] == 0.
    assert compute_metric(keys, query1, "cosine")[1] == 0.
    assert compute_metric(keys, query2, "cosine")[0] == 1
    assert compute_metric(keys, query1, "inner")[0] == -1
    assert compute_metric(keys, query1, "inner")[1] == -2
    assert compute_metric(keys, query1, "euclid")[0] == 0
    assert compute_metric(keys, query2, "euclid")[0] == np.sqrt(2)
