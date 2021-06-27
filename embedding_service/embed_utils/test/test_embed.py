from ..embedder import Embedder
import tensorflow as tf
import os
import numpy as np


def test_linearlizer():
    cur_dir = os.path.dirname(__file__)
    input_fname = cur_dir+"/test.npy"
    input_vec = np.load(input_fname)
    out_dims = 48
    embedder = Embedder(80, 192, out_dims, cur_dir+"/weights/")
    out_vec = embedder.embed(input_vec)
    assert out_vec.shape == (out_dims,)
