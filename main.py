# Sarah Gritzka 2022

import os
import PySimpleGUI as sg
from matplotlib import use
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from wave_handler import read_wav, time_graph, spectrum, a_weighing

# use matplotlib's TkAgg backend
use("TkAgg")


def draw_figure(canvas, figure):
    """
    this function draws figures to the GUI
    :param canvas: Tkinter Canvas Object
    :param figure:
    :return: FigureCanvasTkAgg object
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def delete_figure_agg(figure_agg):
    """
    this function deletes plots that have been drawn to the GUI
    :param figure_agg:
    :return: None
    """
    figure_agg.get_tk_widget().forget()
    plt.close('all')


#####################
#   Define Layout   #
#####################

file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-"
        )
    ],
]

wave_column = [
    [sg.Text("Time Graph", font=('Helvetica', 16))],
    [sg.Canvas(key="-TIME_GRAPH-")],
    [sg.Text("Spectrogram", font=('Helvetica', 16))],
    [sg.Canvas(key="-SPECTRUM-")],
    [sg.Checkbox("A-weighing", default=False, key="-A_WEIGHING-"), sg.Text("    "), sg.Button("Redraw", key="-REDRAW-")]
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(wave_column),
    ]
]

# Create the form and show it without the plots
window = sg.Window(
    "WAV-File Viewer",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
)

#####################
#   Event Loop   #
#####################
time_figure_agg = None
spectrum_figure_agg = None
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # ** IMPORTANT ** Clean up previous drawings before drawing again
    if time_figure_agg:
        delete_figure_agg(time_figure_agg)
    if spectrum_figure_agg:
        delete_figure_agg(spectrum_figure_agg)

    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        # filter names that are files and end with .wav
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".wav"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            # get full file name and read the file
            filename = os.path.join(values["-FOLDER-"],
                                    values["-FILE LIST-"][0])
            samplerate, data = read_wav(filename)
            # draw wave graph
            time_fig = time_graph(data, samplerate)
            time_figure_agg = draw_figure(window['-TIME_GRAPH-'].TKCanvas, time_fig)
            # draw spectrum
            xf, yf, spectrum_fig = spectrum(data, samplerate)
            spectrum_figure_agg = draw_figure(window['-SPECTRUM-'].TKCanvas, spectrum_fig)
        except:
            pass

    elif event == "-REDRAW-": # redraw plots with or without a-weighing
        try:
            time_figure_agg = draw_figure(window['-TIME_GRAPH-'].TKCanvas, time_fig)
            if values["-A_WEIGHING-"] == True:
                a_weighted_fig = a_weighing(xf, yf)
                spectrum_figure_agg = draw_figure(window['-SPECTRUM-'].TKCanvas, a_weighted_fig)
            else:
                spectrum_figure_agg = draw_figure(window['-SPECTRUM-'].TKCanvas, spectrum_fig)
        except:
            pass


window.close()
