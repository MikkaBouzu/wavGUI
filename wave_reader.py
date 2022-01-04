import os
import numpy as np
import matplotlib
from matplotlib import pyplot
import soundfile as sf


def read_wav(path):
    data, samplerate = sf.read(path)
    return data, samplerate


def time_graph(data):
    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
    fig.add_subplot(111).plot(data)
    return fig


if __name__ == "__main__":
    data, samplerate = read_wav("C:/Users/Sarah/Downloads/example.wav")
    fig = time_graph(data)
    fig.savefig("fig1.png")
    fig = time_graph(data)
    fig.savefig("fig2.png")
