"""
This is the driver program it runs the app and updates it accordingly.
"""

# All the dash packages used in the program.
import dash
from dash.dependencies import Input , Output     # For user interactions.
import dash_core_components as dcc               # For making graphs and other components.
import dash_html_components as html              # For html related components.
import plotly.graph_objs as go                   # For making bar graphs.


import os            # To get the current working directory and for other os funtions.

import Directory     # This package is used to store the directories' information.

import webbrowser    # To open the app in a web browser.


app = dash.Dash()           # Dash object.

current_path = os.getcwd()           # Stores the path of the current directory whose information is displayed.
number_of_clicks = 0         # Stores the number of clicks on go-back button to check if it is pressed or not.

# Layout of the app is defined here.
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
        
        
        
        

'''
This function is used to update the sub directory bar graph whenever the value in the input field changes.

Parameters - 
    (string) directory_path - Contains the path of the directory which is present in directory-path field.
Return-
    (figure) Returns a figure object which contains the bar graph for sub directories.
'''
@app.callback(  
        Output("subdirectories-bar-graph" , "figure"),
        [Input("directory-path" , "value")])
def update_directory_graph(directory_path):
    global current_path
    current_path = directory_path                       # Every time the graph is updated we update the current path.
    
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
                
                

'''
This function is used to update the files bar graph whenever the value in the input field changes.

Parameters - 
    (string) directory_path - Contains the path of the directory which is present in directory-path field.
Return-
    (figure) Returns a figure object which contains the bar graph for files.
'''
@app.callback(
        Output("files-bar-graph" , "figure"),
        [Input("directory-path" , "value")])
def update_files_graph(directory_path):

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
                
                

'''
This function is used to update the sub directory dropdown. It gets the directory path from the directory-path field
and updates the dropdown menu accordingly.

Parameters - 
    (string) directory_path - Contains the path of the directory which is present in directory-path field.
Return-
    (figure) Returns a list which contains the labels and values of each option in the sub directory.
'''
@app.callback(
        Output("subdirectory-list" , "options"),
        [Input("directory-path" , "value")])
def update_dropdown_options(directory_path):
    
    current_directory = Directory.Directory(directory_path)
    subDirectories , files = current_directory.get_list()
    
    return [{'label': dr.name, 'value': dr.path} for dr in subDirectories[1:]]
                


'''
This function is used to change the path of the current directory to either a subdirectory or the parent directory
according to where the input is from. It returns the path of the directory as 'value' field in directory-path which triggers the callback 
for update_directory_graph and update_files_graph.

Parameters - 
    (string) sub_directory_path - Contains the path of the sub directory selected from the sub directory dropdown menu.
    (int) n_clicks - Stores the number of clicks on the back button. This is used to check if the back button is pressed or not.
Return-
    (string) Path of the directory
'''
@app.callback(
        Output("directory-path" , "value"),
        [Input("subdirectory-list" , "value"),
         Input("go-back" , "n_clicks")])
def select_subdirectory_or_go_back(sub_directory_path , n_clicks):
    global current_path , number_of_clicks
    
    if number_of_clicks == n_clicks:    # Check if back button is pressed or not ( If it is pressed then n_clicks value will change)
        return sub_directory_path      # If back button is not pressed then dropdown item is selected. Return the path of subdirectory.
    
    number_of_clicks = n_clicks     
    os.chdir(current_path)              # Change the current directory to the current path.
    os.chdir("..")                      # Go back to the parent directory.
    return os.getcwd()                  # return its path.



webbrowser.open("http://127.0.0.1:8050/")
app.run_server()
    
    
    
    