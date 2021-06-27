import os
import tempfile
from ..spectrify import load_data, spectrify_audios
import numpy as np

def test_spectrify():
    out_bins = 80
    samplerate = 44100
    frame_len = 0.1
    input_fnames = [os.path.dirname(__file__)+"/test.mp3"]
    with tempfile.NamedTemporaryFile(suffix=".npy") as file:
        # output_fnames = [file.name]

        spec_datas = [load_data(filename,samplerate) for filename in input_fnames]

        spec_outs = spectrify_audios(
            spec_datas,
            out_bins,
            samplerate,
            frame_len,
        )
        assert len(spec_outs) == 1
        assert spec_outs[0].shape == (int(30/frame_len), out_bins)
        # np.save("test.npy",spec_outs[0])
