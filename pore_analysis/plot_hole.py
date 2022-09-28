## IMPORT LIBRARIES
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from colour import Color
from os import listdir
from os.path import isfile, join
from natsort import natsorted, ns, natsort_keygen

# load files to be plotted
files_list = []
for arg in sys.argv[1:]:
 files_list.append(arg) 

natsort_key1 = natsort_keygen(key=lambda y: y.lower())
files_list.sort(key=natsort_key1)

# parse tsv files
proc_files = []
for file_name in files_list:
    print(file_name)
    file = pd.read_csv(file_name, sep="\t", header=None, names=['columnA'])
    file['coors']= file['columnA'].str.slice(stop=14)
    file['columnA'] = file['columnA'].str[14:]
    file['pore_rad']= file['columnA'].str.slice(stop=12)
    del file['columnA']
    proc_files.append(file)

appended_data = pd.concat(proc_files, axis=1)

# rename columns
cols = []
count = 1
for column in appended_data.columns:
    if column == 'coors':
        cols.append(f'coors_{count}')
        count+=1
        continue
    cols.append(column)
appended_data.columns = cols

cols = []
count = 1
for column in appended_data.columns:
    if column == 'pore_rad':
        cols.append(f'pore_rad_{count}')
        count+=1
        continue
    cols.append(column)
appended_data.columns = cols

appended_data = appended_data.apply(pd.to_numeric)

num_plots = len(appended_data.columns)//2+1

N = 69

start_color = "#150ecc" # dark red
end_color = "#cc0e0e" # dark blue

# list of "N" colors between "start_color" and "end_color"
colorscale = [x.hex for x in list(Color(start_color).range_to(Color(end_color), N))]
#colorscale = ['#e30e0e','#f06767','#e8a0a0','#8c91ed','#4049ed','#0713f0']

fig = go.Figure()

for i in range(1,num_plots):
    fig.add_trace(
        go.Scatter(x=appended_data['pore_rad_'+ str(i)], y=appended_data['coors_'+ str(i)],
                  line=dict(color=colorscale[i], width=2))
    )


fig.update_layout(plot_bgcolor = "white")
fig.update_layout(height=1000, width=900, title_text="Pore analysis")
fig.update_layout(
yaxis = dict(
tickfont = dict(size=18)))
fig.update_layout(
xaxis = dict(
tickfont = dict(size=18)))
fig.update_yaxes(title_text=" Channel coordinates Å ")
fig.update_xaxes(title_text=" Pore radius Å ")
fig['layout']['yaxis']['autorange'] = "reversed"
fig.show()    

