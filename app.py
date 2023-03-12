# Third-Party Imports
from dash import Dash, html, dcc, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# Standard Imports


# Local Imports
from utils import file_handling as fh

# Global Variables
app = Dash(name=__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Lexical Analyser Manipulator and Extractor (LAME)"

server = app.server

UPLOAD_TEXT = "Drag and drop, or click to upload files to storage"

docs = fh.get_documents() # load documents from cloudinary
current_doc = None

# UI Layout
## Main App Layout (headings, file saver and file selector)
app.layout = html.Div(id="main-container", children=[
    dcc.ConfirmDialog(
        id='confirm-save',
        message='Your file(s) were saved successfully.\nPress OK to continue'
    ),
    dcc.ConfirmDialog(
        id='confirm-save-error',
        message='Error: Your file(s) could not be saved.'
    ),
    dcc.ConfirmDialog(
        id="confirm-new-doc",
        message="Error: Your new file was saved successfully.\nPress OK to continue"
    ),
    dcc.ConfirmDialog(
        id="confirm-new-doc-error",
        message=""
    ),
    dcc.ConfirmDialog(
        id='confirm-doc-delete',
        message='Your file was deleted successfully.\nPress OK to continue',
        displayed=False,
    ),
    dcc.ConfirmDialog(
        id='confirm-doc-delete-error',
        message='Error: Your file could not be deleted.'
    ),
    html.H1(id="main-heading", children="Lexical Analyser Manipulator and Extractor"),
    dcc.Upload(
        id="upload-data",
        multiple=True,
        children=dcc.Loading(
            color="#003049",
            children=[
                html.Div(
                    id="upload-text",
                    children=UPLOAD_TEXT,
                )
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
    html.Div(id='reload-handler-0', style={"display": "hidden"}),
    html.Div(id='reload-handler-1', style={"display": "hidden"}),
    html.Div(id='reload-handler-2', style={"display": "hidden"}),
    html.Div(id='reload-handler-3', style={"display": "hidden"}),
    html.Div(id='reload-handler-4', style={"display": "hidden"}),
    html.Div(id='reload-handler-5', style={"display": "hidden"}),
])

## Major Components
### Section Selector
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

### Documents Section
new_doc_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    id="new-doc-modal-header",
                    children=dbc.ModalTitle(
                        id="new-doc-modal-heading",
                        children="New Document",
                    ),
                ),
                dbc.ModalBody(
                    id="new-doc-modal-body",
                    children=[
                        html.H3("Name"),
                        dbc.Input(
                            id="new-doc-name",
                            placeholder="Name of new document",
                            value="",
                            persistence=False,
                        ),
                        html.Br(),
                        html.H3("Content"),
                        dbc.Textarea(
                            id="new-doc-content",
                            placeholder="Content of new document",
                            draggable=False,
                            value="",
                            persistence=False,
                        )
                    ]
                ),
                dbc.ModalFooter(
                    id="new-doc-modal-footer",
                    children=[
                        dbc.Button(
                            id="new-doc-modal-btn",
                            children="Create New Document",
                        )
                    ]
                ),
            ],
            id="new-doc-modal",
            keyboard=False,
            backdrop="static",
            fullscreen=True,
        ),
    ],
)

def get_doc_section():
    if docs is None:
        text = "No documents to display. Upload documents to get started."
        return html.H2(
            children=text,
            className="no-docs-heading"
        )

    docs_copy = docs.copy(deep=True).to_dict('records')

    return html.Div(
        id="doc-section",
        children=[
            new_doc_modal,
            html.Div(
                id="doc-btn-container",
                children=[
                    html.Button(
                        id="new-doc-btn",
                        className="doc-btn", 
                        children="New Document",
                        disabled=False,
                    ),
                    html.Button(
                        id="download-doc-btn",
                        className="doc-btn-disabled", 
                        children="Download Raw Text",
                        disabled=True,
                    ),
                    dcc.Download(id="download-doc"),
                    html.Button(
                        id="delete-doc-btn",
                        className="doc-btn-disabled", 
                        children="Delete Document",
                        disabled=True,
                    ),
                ]
            ),
            dbc.Accordion(
                id="doc-accord",
                children=[
                    dbc.AccordionItem(
                        id=doc["public_id"],
                        item_id=doc["public_id"],
                        title=doc["title"],
                        class_name="doc-accord-item",
                        children=[
                            html.Div(
                                className="doc-accord-item-content",
                                children=[
                                    html.P(f"URL: {doc['url']}"),
                                    html.P("Raw text:"),
                                    html.P(
                                        children=doc["content"],
                                        className="doc-content",
                                    )
                                ]
                            )
                        ],
                    )
                    for doc in docs_copy
                ],
                start_collapsed=True
            )
        ]
    )

### Info Extraction Section
def get_info_extraction_section():
    if docs is None:
        text = "Please upload documents to get started with information extraction."
        return html.H2(
            children=text,
            className="no-docs-heading"
        )

    docs_copy = docs.copy(deep=True)

    doc_list = docs_copy["title"]
    return html.Div(
        id="info-extract-section",
        children=[
            html.Div(
                id="info-extract-params",
                children=[
                    html.Div(children=[html.H3("Select Documents"),
                    dcc.Dropdown(
                        id="info-extract-doc-select",
                        options=doc_list,
                        multi=True,
                        placeholder="Select documents..."
                    )]),
                    html.Div(children=[html.H3("Select Extraction Method"),
                    dcc.Dropdown(
                        id="info-extract-method-select",
                        options=[
                            {"label": "TF-IDF", "value": "tf-idf"}, 
                            {"label": "Cosine Similarity", "value": "cosine_sim"},
                            {"label": "BERT", "value": "bert"},
                            {"label": "OpenAI", "value": "openai"}
                        ],
                        value="tf-idf",
                        multi=False,
                        clearable=False,
                    )]),
                    html.Div(children=[html.H3("Search Query"),
                    dbc.Input(
                        id="info-extract-query",
                        placeholder="Enter your search query",
                        value="",
                        persistence=False,
                    )]),
                    html.Button(
                        id="info-extract-btn",
                        children="Extract Information",
                        className="nlp-btn-disabled",
                        disabled=True,
                    )
                ]
            ),
            html.Div(
                id="info-extract-output",
                children=[
                    dcc.Loading([
                        dbc.Textarea(
                            id="info-extract-output-content",
                            value="",
                            draggable=False,
                            readOnly=True,
                            placeholder="The results of your query will appear here"
                        )
                    ])
                ]
            )
        ]
    )

### Summary Section
def get_summary_section():
    if docs is None:
        text = "Please upload documents to get started with text summmarisation."
        return html.H2(
            children=text,
            className="no-docs-heading"
        )

    return html.Div(
        id="summary-section",
        children=[
            html.H3("Summarisation")
        ]
    )

### Clustering Section
def get_clustering_section():
    if docs is None:
        text = "Please upload documents to get started with document clustering."
        return html.H2(
            children=text,
            className="no-docs-heading"
        )

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
## Page Refresh Callback
@app.callback(
    Output("section-container", "children"),
    inputs=dict(
        children=(
            Input("reload-handler-0", "children"), 
            Input("reload-handler-1", "children"), 
            Input("reload-handler-2", "children"),
            Input("reload-handler-3", "children"),
            Input("reload-handler-4", "children"),
            Input("reload-handler-5", "children"),      
        ),
        tab_value=State("main-tabs", "value"),
    )
)
def refresh_page(tab_value, children):
    return section_selector(tab_value)

## Docs Page Callbacks
@app.callback(
    Output("reload-handler-0", "children"),
    Output("confirm-save", "displayed"),
    Output("confirm-save-error", "displayed"),
    Output("upload-text", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")]
)
def upload_handler(f_names, f_contents):
    global docs

    is_success = True

    if not f_names or not f_contents:
        return None, False, False, UPLOAD_TEXT

    res = fh.save_files(f_names, f_contents)

    is_success = res
    
    docs = fh.get_documents()
    return None, is_success, not is_success, UPLOAD_TEXT


@app.callback(
    Output("reload-handler-1", "children"),
    Input("main-tabs", "value"),
)
def main_tabs_handler(value): return None

@app.callback(
    Output("new-doc-btn", "className"),
    Output("new-doc-btn", "disabled"),
    Output("download-doc-btn", "className"),
    Output("download-doc-btn", "disabled"),
    Output("delete-doc-btn", "className"),
    Output("delete-doc-btn", "disabled"),
    Input("doc-accord", "active_item"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def accordion_handler(item_id):
    global current_doc
    if item_id is not None:
        current_doc = docs[docs["public_id"] == item_id].to_dict('records')[0]
        return "doc-btn-disabled", True, "doc-btn", False, "doc-btn", False
    elif item_id is None:
        current_doc = None
        return "doc-btn", False, "doc-btn-disabled", True, "doc-btn-disabled", True

@app.callback(
    Output("new-doc-modal", "is_open"),
    Input("new-doc-btn", "n_clicks"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def new_doc_handler(n_clicks):
    if n_clicks is not None:
        return True

@app.callback(
    Output("reload-handler-2", "children"),
    Output("confirm-new-doc", "displayed"),
    Output("confirm-new-doc-error", "displayed"),
    Output("confirm-new-doc-error", "message"),
    State("new-doc-name", "value"),
    State("new-doc-content", "value"),
    Input("new-doc-modal-btn", "n_clicks"),
)
def create_doc_handler(doc_name, doc_content, n_clicks):
    global docs

    if n_clicks is not None:
        err_messages = [
            "Please enter a name for your new file.",
            "Please enter some content for your new file.",
            "Error: Your document could not be created. Please try again.",
        ]

        if doc_name.strip() == "" and doc_content.strip() == "":
            return no_update, False, True, "\n".join(err_messages[:-1])
        elif doc_name.strip() == "":
            return no_update, False, True, err_messages[0]
        elif doc_content.strip() == "":
            return no_update, False, True, err_messages[1]
        
        res = fh.create_new_file(doc_name, doc_content)
        if not res:
            return no_update, False, True, err_messages[2]
        
        docs = fh.get_documents()
        return None, True, False, "",
    return no_update, False, False, ""

@app.callback(
    Output("download-doc", "data"),
    Input("download-doc-btn", "n_clicks"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def doc_download_handler(n_clicks):
    if n_clicks is not None and n_clicks > 0 and current_doc is not None:
            doc_title = current_doc["title"]
            doc_content = current_doc["content"]
            return dict(content=doc_content, filename=f"{doc_title}.txt")

@app.callback(
    Output("reload-handler-3", "children"),
    Output("confirm-doc-delete", "displayed"),
    Output("confirm-doc-delete-error", "displayed"),
    Input("delete-doc-btn", "n_clicks"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def doc_delete_handler(n_clicks):
    global docs

    if n_clicks is not None and n_clicks > 0 and current_doc is not None:
        is_success = True
        doc_id = current_doc["public_id"]
        res = fh.delete_document(doc_id)
        is_success = res
        docs = fh.get_documents()
        return None, is_success, not is_success
    return None, False, False

## Info Extraction Page Callbacks
@app.callback(
    Output("info-extract-btn", "disabled"),
    Output("info-extract-btn", "className"),
    Input("info-extract-doc-select", "value"),
    Input("info-extract-query", "value"),
)
def info_extract_params_handler(documents, query):
    if documents is not None and query != "":
        if query.strip() != "" and len(documents) > 0:
            return False, "nlp-btn"
    return True, "nlp-btn-disabled"

@app.callback(
    Output("dummy", "children"),
    State("info-extract-doc-select", "value"),
    State("info-extract-method-select", "value"),
    State("info-extract-query", "value"),
    Input("info-extract-btn", "n_clicks"),
)
def info_extract_handler(select_docs, method, query, n_clicks):
    if n_clicks is not None:
        print(select_docs, method, query)

# Running server
if __name__ == "__main__":
    app.run_server(debug=True)