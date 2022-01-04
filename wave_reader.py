import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import soundfile as sf
from scipy.fft import fft

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

    p_0 = 2e-5
    y = fft(data)
    y = 20 * np.log10(y/p_0)
    d = len(y) / 2  # you only need half of the fft list (real signal symmetry)
    plt.plot(abs(y[:int(d)-1]))

    plt.xscale('log')
    plt.show()