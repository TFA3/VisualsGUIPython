import PySimpleGUI as UI
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog as fd
#Thomas Ashton 4/29/23 Created for Data Visualization K274 Create Your Own
#Select the file path that you want
filepath = fd.askopenfile(title='Select the .csv file with keywords',
                          filetypes=(('csv files', '*.csv'), ('excel files', '*.xlsx')))
value = filepath.name.find(".")
filevalue = filepath.name[value:]
#Determines if it is a .csv or a .xlsx and extracts the column names from the data.
if filevalue == ".csv":
    df = pd.read_csv(filepath)
if filevalue == ".xlsx":
    df = pd.read_excel(filepath.name)
column_Namesbase = df.columns.values
column_Names = column_Namesbase.tolist()
#Creates the User Interface and takes the column names and puts them in the listbox, also creates the combobox with the plots, I might shift it to a
#Radio button only because depending on radio button selected it can adjust how many listbox values can be selected at once, right now it is only 1
layout = [
    [UI.Listbox(column_Names, size=(20, 4), expand_y=True, enable_events=True, default_values=[1], key='-LISTBOX-'),
     UI.Combo(values=['bar', 'pie', 'hist'], default_value='bar', key='-PlotType-'),
     UI.Button("Create Graph"), ]
]
window = UI.Window('Select Column and Graph Type', layout, finalize=True)
#Creates the window and brings it to the front, along with allows the button to create the graph and keep it from closing, you can create a graph, close it
#and create another one as many times as you would like.
while True:
    window.finalize()
    window.bring_to_front()
    event, values = window.read()
    if event == UI.WINDOW_CLOSED:
        break

    if event == "Create Graph":
        Gtype = values["-PlotType-"]
        Selected = values["-LISTBOX-"]
        #Determines if it is an object, which will require a count process to be done to it for it to work properly
        if df[Selected[0]].dtype == "object":
            if Gtype == 'pie':
                plt.pie(df[Selected[0]].value_counts(), labels=df[Selected[0]].unique(), autopct='%1.1f%%')
            else:
                df[Selected[0]].value_counts().plot(kind=Gtype)
            plt.title(Selected[0])
            plt.show()
        else:
            #Creates the bins for the numerical data so that it isn't overly complex for bar and pie charts, doesn't do anything for histograms yet.
            Maxval = df[Selected[0]].max()
            Minval = df[Selected[0]].min()
            low = Maxval * 0.33
            Mid = Maxval * 0.66
            lowv = '(' + str(Minval) + ', ' + str(low) + ']'
            Midv = '(' + str(low) + ', ' + str(Mid) + ')'
            Highv = '[' + str(Mid) + ', ' + str(Maxval) + ')'
            #Bins the data
            df['binned'] = pd.qcut(df[Selected[0]], q=[0, 0.33, 0.66, 1], labels=[lowv, Midv, Highv])
            #Counts the binned data
            grouped_data = df.groupby(['binned']).size().reset_index(name='Count')
            #Figures out which graph was selected and creates it.
            if Gtype == 'pie':
                fig, ax = plt.subplots()
                ax.pie(grouped_data['Count'], labels=[lowv, Midv, Highv], autopct='%1.1f%%')
                ax.axis('equal')
            if Gtype == 'bar':
                Counts = grouped_data['Count']
                plt.bar([lowv, Midv, Highv], grouped_data['Count'])
            if Gtype == 'hist':
                plt.hist(df[Selected[0]])
            #Adds the title to the graph
            plt.title(Selected[0])
            #Shows the graph.
            plt.show()
