import os
import numpy as np
import matplotlib
import soundfile as sf


def read_wav(path):
    data, samplerate = sf.read(path)
    return data, samplerate

def time_graph(data):
    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
    fig.cla()
    fig.add_subplot(111).plot(data)
    return fig
