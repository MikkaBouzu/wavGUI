# Sarah Gritzka 2022

import numpy as np
from matplotlib.figure import Figure
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


def time_graph(data, samplerate):
    """
    this function creates a wave plot of the sound file
    :param data: np.array
    :param samplerate: int
    :return: matplotlib.figure.Figure object
    """
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111,
                         xlabel='Time in s',
                         ylabel='Amplitude')

    # rescale x axis to seconds
    samples_total = data.shape[0]
    x_scale = [x/samplerate for x in range(samples_total)]

    ax.plot(x_scale, data, linewidth=0.5)

    # some plot beautification
    fig.tight_layout()
    ax.grid(True, which='both')
    return fig


def spectrum(data, samplerate):
    """
    this function calculates an FFT over the whole sound file and returns a plot. It also returns the x and y data for
    that plot, so they can be reused later and only have to be calculated once.
    :param data: np.array
    :param samplerate: int
    :return:xf: np.array
            yf: np.array
            fig: matplotlib.figure.Figure object
    """
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111,
                         xscale='log',
                         xlabel='frequency in Hz',
                         ylabel='relative amplitude in dB')
    p_0 = 2e-5
    samples_total = data.shape[0]

    xf = rfftfreq(samples_total, 1/samplerate)
    yf = rfft(data)
    yf = 20 * np.log10(yf/p_0) # convert to dB scale

    ax.plot(xf, np.abs(yf), linewidth=0.5)

    # some plot beautification
    fig.tight_layout()
    ax.set_xlim(left=10)
    ax.grid(True, which='both')
    return xf, yf, fig


def a_weighing(xf, yf):
    """
    This function calculates A-weighing according to https://de.wikipedia.org/wiki/Frequenzbewertung and returns a plot
    :param xf: 
    :param yf: 
    :return: matplotlib.figure.Figure object
    """
    fig = Figure(figsize=(8, 4), dpi=100)
    ax = fig.add_subplot(111,
                         xscale='log',
                         xlabel='frequency in Hz',
                         ylabel='relative amplitude in dB')
    # perform A-weighing according to https://de.wikipedia.org/wiki/Frequenzbewertung
    k_A = 7.39705e9
    a_weighted = k_A * yf**4/((yf + 129.4)**2
                              * (yf + 676.7)
                              * (yf + 4636)
                              * (yf + 76655)**2)
    ax.plot(xf, abs(a_weighted), linewidth=0.5)

    # some plot beautification
    fig.tight_layout()
    ax.set_xlim(left=10)
    ax.grid(True, which='both')
    return fig


# if you execute this helper code you will save the graphs displayed in the GUI to your disk
if __name__ == "__main__":
    samplerate, data = read_wav("C:/Users/Sarah/Downloads/example.wav")
    fig = time_graph(data, samplerate)
    fig.savefig("fig1.png")

    xf, yf, spec = spectrum(data, samplerate)
    spec.savefig("fig2.png")

    a_bewertung = a_weighing(xf, yf)
    a_bewertung.savefig("fig3.png")
