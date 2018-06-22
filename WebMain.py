import dash
from dash.dependencies import Input , Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

import os

import Directory , File

import webbrowser


app = dash.Dash()
first_update = True
current_path = ""
number_of_clicks = 0

app.layout = html.Div(children=[
        html.H1(
                children="Distribution of Disk Space.",
                style={
                'textAlign':'center',
                }),   
        html.H2(
                children="Current Directory : "
                ),
        html.Div(children=[
                html.Button(
                        id='go-back',
                        children="Back"),
                dcc.Input(
                        id="directory-path",
                        value=os.getcwd(),
                        type="text",
                        style={"width":"100%"}
                    ),
                html.H3(
                        children="Sub Directories"
                        ),
                dcc.Dropdown(
                        id="subdirectory-list",
                        value="Select"
                        )]
                ),
        dcc.Graph(
                    id='subdirectories-bar-graph'
                 ),
        dcc.Graph(
                   id='files-bar-graph'
                )
    ])


@app.callback(  
        Output("subdirectories-bar-graph" , "figure"),
        [Input("directory-path" , "value")])
def update_graph(directory_path):
    global current_path
    current_path = directory_path
    
    current_directory = Directory.Directory(directory_path)
    subDirectories , files = current_directory.get_list()
    
    return dict(
                data=[go.Bar(
                            x = [dr.name for dr in subDirectories[1:]], 
                            y = [dr.size()[0] for dr in subDirectories[1:]],
                            )],
                layout=go.Layout(
                            title="Sub-Directories",
                            )
                )
                    
@app.callback(
        Output("files-bar-graph" , "figure"),
        [Input("directory-path" , "value")])
def update_graph(directory_path):

    current_directory = Directory.Directory(directory_path)
    subDirectories , files = current_directory.get_list()
    
    return dict(
                data=[go.Bar(
                            x = [file.name for file in files[1:]], 
                            y = [file.size() for file in files[1:]],
                            )],
                layout=go.Layout(
                            title="Files",
                            )
                )
                
@app.callback(
        Output("subdirectory-list" , "options"),
        [Input("directory-path" , "value")])
def update_graph(directory_path):
    
    current_directory = Directory.Directory(directory_path)
    subDirectories , files = current_directory.get_list()
    
    return [{'label': dr.name, 'value': dr.path} for dr in subDirectories[1:]]
                
@app.callback(
        Output("directory-path" , "value"),
        [Input("subdirectory-list" , "value"),
         Input("go-back" , "n_clicks")])
def update_graph(directory_path , n_clicks):
    global current_path , number_of_clicks
    if number_of_clicks == n_clicks:
        return directory_path
    number_of_clicks = n_clicks
    os.chdir(current_path)
    os.chdir("..")
    print("Clicks :" , n_clicks)
    return os.getcwd()



if __name__ == '__main__':
    webbrowser.open("http://127.0.0.1:8050/")
    app.run_server()
    
    
    
    