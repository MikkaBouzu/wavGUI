import os
import soundfile as sf
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
import matplotlib

matplotlib.use("TkAgg")

data, samplerate = sf.read('C:/Users/Sarah/Downloads/example.wav')

fig = matplotlib.figure.Figure(figsize=(8, 4), dpi=100)
fig.add_subplot(111).plot(data)


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


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

# Add the plot to the window
# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    # Folder name was filled in, make a list of files in the folder
    if event == "-FOLDER-":
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".wav"))
        ]
        window["-FILE LIST-"].update(fnames)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            filename = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            window["-TIME_GRAPH-"].update(draw_figure(window["-TIME_GRAPH-"].TKCanvas, fig))

        except:
            pass

window.close()




