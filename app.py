# Third-Party Imports
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from PyPDF2 import PdfReader
import docx2txt

# Standard Imports


# Local Imports
from utils import file_handling as fh

# Global Variables
app = Dash(__name__)
app.title = "Lexical Analyser Manipulator and Extractor (LAME)"

server = app.server

UPLOAD_TEXT = "Drag and drop, or click to upload files to storage"

docs = fh.get_documents() # load documents from cloudinary

# UI Layout
## Main App Layout (headings, file saver and file selector)
app.layout = html.Div(id="main-container", children=[
    html.H1("Welcome to LAME!!!"),
    dcc.Upload(
        id="upload-data",
        multiple=True,
        children=dcc.Loading(
            color="white",
            children=[
                html.Div(UPLOAD_TEXT)
            ]
        )
    ),
    dcc.Tabs(id="main-tabs", value="docs", children=[
        dcc.Tab(
            className="main-tab",
            selected_className="main-tab-selected",
            label="My Documents", 
            value="docs"
        ),
        dcc.Tab(
            className="main-tab",
            selected_className="main-tab-selected",
            label="Information Extraction", 
            value="info-extraction"
        ),
        dcc.Tab(
            className="main-tab",
            selected_className="main-tab-selected",
            label="Summarisation", 
            value="summarisation"
        ),
        dcc.Tab(
            className="main-tab",
            selected_className="main-tab-selected",
            label="Clustering", 
            value="clustering"
        ),
        dcc.Tab(
            className="main-tab",
            selected_className="main-tab-selected",
            label="WikiBot", 
            value="wikibot"
        ),
    ]),
    html.Div(id="section-container"),
    html.Div(id='dummy', style={"display": "hidden"}),
    html.Div(id='dummy2', style={"display": "hidden"}),
    html.Div(id='dummy3', style={"display": "hidden"}),
    html.Div(id='dummy4', style={"display": "hidden"}),
    html.Div(id='dummy5', style={"display": "hidden"}),
])

## Major Components
### Document Table
def section_selector(s_name):
    if s_name == "docs":
        return get_doc_section()
    elif s_name == "info-extraction":
        return get_info_extraction_section()
    elif s_name == "summarisation":
        return get_summary_section()
    elif s_name == "clustering":
        return get_clustering_section()
    elif s_name == "wikibot":
        return get_wiki_bot_section()

def get_doc_section():
    return html.Div(
        id="doc-section",
        children=[
            dbc.Table.from_dataframe(
                docs[["title", "created_at", "url"]],
                id="doc-table"
            )
        ]
    )

### Info Extraction Section
def get_info_extraction_section():
    return html.Div(
        id="info-extraction-section",
        children=[
            html.H3("Information Extraction")
        ]
    )

### Summary Section
def get_summary_section():
    return html.Div(
        id="summary-section",
        children=[
            html.H3("Summarisation")
        ]
    )

### Clustering Section
def get_clustering_section():
    return html.Div(
        id="clustering-section",
        children=[
            html.H3("Document Clustering")
        ]
    )

### WikiBot Section
def get_wiki_bot_section():
    return html.Div(
        id="wiki-bot-section",
        children=[
            html.H3("The WikiBot")
        ]
    )

# Callback functions
"""
Callback Basics
---------------
Callbacks are a way of retrieving the values of UI components; e.g. the text
inside a form or the numerical value of a slider. Callbacks functions are 
automatically called whenever an input UI component's property changes, in 
order to update some property in another UI component (the output).
Syntax guide
------------
@app.callback(...) <-- function decorator containing all of the input and
                       output UI components.
Input(component-id, property) <-- this selects a given UI component by its ID
                                  and reads the value of the chosen property
                                  into the function. This is used as a trigger
                                  for your callback function run; when the value
                                  of 'property' in this UI component changes the
                                  function will be called.
State(component-id, property) <-- this works just like Input(component-id, property).
                                  the only difference is that this will not trigger
                                  your callback function. This is useful when you just
                                  want to get the value of a UI component property
                                  without changing the value of the property.
Output(component-id, property) <-- this selects a given UI component by its ID
                                   and changes the value of the selected property
                                   to whatever value was output by the callback
                                   function.
IMPORTANT: the order in which you specify input and output UI components is
           crucial. Always specify the output components before the input
           components. And always make sure that there is atleast 1 output
           component and at least 1 input component in the style Input(id, prop).
           If you don't do this, your callback function will not work.
In order to fully understand what each callback function does you can look at 
the ids of the UI components specified in @app.callback() and then find those 
components in the part of the code where those UI components are created.
For more info on how callback functions work you can visit the following links:
    * https://dash.plotly.com/basic-callbacks
    * https://dash.plotly.com/sharing-data-between-callbacks
    * https://dash.plotly.com/advanced-callbacks
"""

@app.callback(
    Output("dummy", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")]
)
def upload_handler(f_names, f_contents):
    if not f_names or not f_contents:
        return None

    fh.save_files(f_names, f_contents)

@app.callback(
    Output("section-container", "children"),
    Input("main-tabs", "value"),
)
def main_tabs_handler(value):
    return section_selector(value)

# Running server
if __name__ == "__main__":
    app.run_server(debug=True)