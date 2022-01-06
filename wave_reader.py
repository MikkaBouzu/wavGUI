import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from scipy.io import wavfile
from scipy.fft import rfft, rfftfreq


def read_wav(path):
    samplerate, data = wavfile.read(path)
    return samplerate, data


def time_graph(data):
    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100, tight_layout=True)
    fig.add_subplot(111).plot(data)
    return fig


def spectrum(data, samplerate):
    fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100, tight_layout=True)
    ax = fig.add_subplot(111,
                         xscale='log',
                         xlim=(10, 10e4),
                         xlabel='frequency in Hz',
                         ylabel='relative amplitude in dB')

    p_0 = 2e-5
    samples_total = data.shape[0]

    xf = rfftfreq(samples_total, 1/samplerate)
    yf = rfft(data)
    yf = 20 * np.log10(yf/p_0)

    #TODO: welches von en beiden ist "richtig"?
    ax.plot(xf, np.abs(yf), linewidth=0.5)
    # ax.plot(np.abs(yf), linewidth=0.5)

    return fig


if __name__ == "__main__":
    samplerate, data = read_wav("C:/Users/Sarah/Downloads/example.wav")
    fig = time_graph(data)
    fig.savefig("fig1.png")

    spec = spectrum(data, samplerate)
    spec.savefig("fig2.png")
