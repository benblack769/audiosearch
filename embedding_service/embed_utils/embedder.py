from .linearlizer import Linearlizer
import tensorflow as tf
import os
import numpy as np


class Embedder:
    def __init__(self, mel_bins, hidden_size, out_dim, weight_dir):
        self.sess = sess = tf.Session()
        linearlizer = Linearlizer(mel_bins, hidden_size, out_dim)
        self.mel_binned_spec_plc = tf.placeholder(tf.float32, [None, mel_bins])
        linearlizer.load(sess, weight_dir)
        wordvec = linearlizer.word_vector(self.mel_binned_spec_plc)
        self.average_wordvec = tf.reduce_mean(wordvec, axis=0)

    def embed(self, mel_binned_spectrogram):
        embed = self.sess.run(self.average_wordvec,feed_dict={
            self.mel_binned_spec_plc:mel_binned_spectrogram
        })
        return embed
