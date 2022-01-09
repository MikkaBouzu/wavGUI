import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
from wave_reader import read_wav, time_graph, spectrum

matplotlib.use("TkAgg")


def draw_figure(canvas, figure):
    """

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

    :param figure_agg:
    :return: None
    """
    figure_agg.get_tk_widget().forget()
    plt.close('all')


# Define the window layout
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
    [sg.Text("Time Graph")],
    [sg.Canvas(key="-TIME_GRAPH-")],
    [sg.Text("Spectrogram")],
    [sg.Canvas(key="-SPECTRUM-")],
]

# ----- Full layout -----
layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(wave_column),
    ]
]

# Create the form and show it without the plot
window = sg.Window(
    "WAV-File Viewer",
    layout,
    location=(0, 0),
    finalize=True,
    element_justification="center",
)


time_figure_agg = None
spectrum_figure_agg = None
# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if time_figure_agg: # if this already exists, delete it
        # ** IMPORTANT ** Clean up previous drawing before drawing again
        delete_figure_agg(time_figure_agg)
    if spectrum_figure_agg: # if this already exists, delete it
        # ** IMPORTANT ** Clean up previous drawing before drawing again
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
            filename = os.path.join(values["-FOLDER-"],
                                    values["-FILE LIST-"][0])
            samplerate, data = read_wav(filename)
            time_fig = time_graph(data, samplerate)
            time_figure_agg = draw_figure(window['-TIME_GRAPH-'].TKCanvas, time_fig)

            spectrum_fig = spectrum(data, samplerate)
            spectrum_figure_agg = draw_figure(window['-SPECTRUM-'].TKCanvas, spectrum_fig)

        except:
            pass

window.close()
