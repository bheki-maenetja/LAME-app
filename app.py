# Third-Party Imports
from dash import Dash, html, dcc, dash_table

# Standard Imports
# Local Imports

# Global Variables
app = Dash(__name__)
app.title = "Lexical Analyser Manipulator and Extractor (LAME)"

server = app.server

upload_text = "Drag and drop, or click to upload files to storage"

# UI Layout
## Main App Layout (headings, file saver and file selector)
app.layout = html.Div(id="main-container", children=[
    html.H1("Welcome to LAME!!!"),
    dcc.Upload(
        id="upload-data",
        multiple=True,
        children=dcc.Loading(
            children=[
                html.Div(upload_text)
            ]
        )
    ),
    dcc.Tabs(id="main-tabs", value="1", children=[
        dcc.Tab(label="My Documents", value="1"),
        dcc.Tab(label="Information Extraction", value="2"),
        dcc.Tab(label="Summarisation", value="3"),
        dcc.Tab(label="Clustering", value="4"),
        dcc.Tab(label="WikiBot", value="5"),
    ])
])

# Running server
if __name__ == "__main__":
    app.run_server(debug=True)