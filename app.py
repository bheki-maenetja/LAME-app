# Third-Party Imports
from dash import Dash, html, dcc, dash_table

# Standard Imports
# Local Imports

# Global Variables
app = Dash(__name__)
app.title = "Lexical Analyser Manipulator and Extractor (LAME)"

server = app.server

# UI Layout
## Main App Layout (headings, file saver and file selector)
app.layout = html.Div(children=[
    html.H1("Welcome to LAME!!!")
])

# Running server
if __name__ == "__main__":
    app.run_server(debug=True)