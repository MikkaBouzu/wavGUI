# Sarah Gritzka 2022

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq


def read_wav(path):
    """
    this function reads a WAV-file and outputs the samplerate and data
    :param path: os.path str
    :return: tuple: int, np.array
    """
    samplerate, data = wavfile.read(path)
    return samplerate, data


def time_graph(data):
    """
    this function creates a plot
    :param data: np.array
    :return: matplotlib.figure.Figure object
    """
    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(data, linewidth=0.5)

    # some beautification
    fig.tight_layout()
    ax.grid(True)
    return fig


def spectrum(data, samplerate):
    """

    :param data: np.array
    :param samplerate: int
    :return: matplotlib.figure.Figure object
    """
    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111,
                         xscale='log',
                         # xlim=(10, 10e4),
                         xlabel='frequency in Hz',
                         ylabel='relative amplitude in dB')

    p_0 = 2e-5
    samples_total = data.shape[0]

    xf = rfftfreq(samples_total, 1/samplerate)
    yf = rfft(data)
    yf = 20 * np.log10(yf/p_0) # convert to dB scale

    # TODO: welches von den beiden ist "richtig"?
    ax.plot(xf, np.abs(yf), linewidth=0.5)
    # ax.plot(np.abs(yf), linewidth=0.5)

    # some beautification
    fig.tight_layout()
    ax.grid(True)
    return fig


# if you execute this helper code you will save the graphs displayed in th GUI to your disk
if __name__ == "__main__":
    samplerate, data = read_wav("C:/Users/Sarah/Downloads/example.wav")
    fig = time_graph(data)
    fig.savefig("fig1.png")

    spec = spectrum(data, samplerate)
    spec.savefig("fig2.png")
