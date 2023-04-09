# Third-Party Imports
from dash import Dash, html, dcc, no_update
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

import plotly.graph_objects as go

# Standard Imports


# Local Imports
from utils import file_handling as fh
from nlp.info_extraction import DocSearcher, tokenize
from nlp.summarisation import DocSummariser
import nlp.doc_clustering as dc
from nlp.wikibot import WikiBot

# Global Variables
app = Dash(
    name=__name__, 
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP, 
        dbc.icons.FONT_AWESOME,
    ]
)
app.title = "Lexical Analyser Manipulator and Extractor (LAME)"

server = app.server

UPLOAD_TEXT = "Drag and drop, or click to upload files to storage"
WIKIBOT_TAGLINE = """
Ask me anything and I'll search Wikipedia's 6m+ articles to find the answer
"""

docs = fh.get_documents() # load documents from cloudinary
current_doc = None

info_extractor = DocSearcher()
doc_summariser = DocSummariser()
wikibot = WikiBot()

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
        message="Your file was saved successfully.\nPress OK to continue"
    ),
    dcc.ConfirmDialog(
        id="confirm-new-doc-error",
        message="Error: Your file(s) could not be saved."
    ),
    dcc.ConfirmDialog(
        id="confirm-edit-doc",
        message="Your file was saved successfully.\nPress OK to continue"
    ),
    dcc.ConfirmDialog(
        id="confirm-edit-doc-error",
        message="Error: Your file could not be saved."
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
            label="Question Answering", 
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

edit_doc_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader(
                    id="edit-doc-modal-header",
                    children=dbc.ModalTitle(
                        id="edit-doc-modal-heading",
                        children="New Document",
                    ),
                ),
                dbc.ModalBody(
                    id="edit-doc-modal-body",
                    children=[
                        html.H3("Name"),
                        dbc.Input(
                            id="edit-doc-name",
                            placeholder="Name of document",
                            value="",
                            persistence=False,
                        ),
                        html.Br(),
                        html.H3("Content"),
                        dbc.Textarea(
                            id="edit-doc-content",
                            placeholder="Content of document",
                            draggable=False,
                            value="",
                            persistence=False,
                        )
                    ]
                ),
                dbc.ModalFooter(
                    id="edit-doc-modal-footer",
                    children=[
                        dbc.Button(
                            id="edit-doc-modal-btn",
                            children="Save Document",
                        )
                    ]
                ),
            ],
            id="edit-doc-modal",
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
            edit_doc_modal,
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
                        id="edit-doc-btn",
                        className="doc-btn-disabled", 
                        children="Edit Document",
                        disabled=True,
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
            html.Div(
                id="doc-accord-container",
                children=[
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
                                            # html.P(f"Word count: {doc['word_count']}"),
                                            # html.P(f"Character count: {doc['char_count']}"),
                                            html.P(f"Word count: {len(tokenize(doc['content'], False))}"),
                                            html.P(f"Character count: {len(doc['content'])}"),
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
        ]
    )

### Info Extraction Section
def get_info_extraction_section():
    if docs is None:
        text = "Please upload documents to get started with question answering."
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
                    html.Div(children=[html.H3("Method"),
                    dcc.Dropdown(
                        id="info-extract-method-select",
                        options=[
                            {"label": "TF-IDF", "value": "tf-idf"}, 
                            {"label": "Cosine Similarity", "value": "cosine_sim"},
                            {"label": "BERT", "value": "bert2"},
                            {"label": "OpenAI", "value": "openai"}
                        ],
                        value="tf-idf",
                        multi=False,
                        clearable=False,
                    )]),
                    html.Div(children=[html.H3("Question"),
                    dbc.Input(
                        id="info-extract-query",
                        placeholder="Enter your question here",
                        value="",
                        persistence=False,
                    )]),
                    html.Button(
                        id="info-extract-btn",
                        children="Answer Question",
                        className="nlp-btn-disabled",
                        disabled=True,
                    )
                ]
            ),
            html.Div(
                id="info-extract-output",
                children=[
                    dcc.Loading(
                        color="#003049",
                        children=[
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

    docs_copy = docs.copy(deep=True)
    doc_list = docs_copy["title"]

    return html.Div(
        id="summary-section",
        children=[
            html.Div(
                id="summary-params",
                children=[
                    html.Div(
                        children=[
                            html.H3("Select Documents"),
                            dcc.Dropdown(
                                id="summary-doc-select",
                                options=doc_list,
                                multi=False,
                                placeholder="Select documents..."
                            )
                        ]
                    ),
                    html.Div(
                        children=[
                            html.H3("Method"),
                            dcc.Dropdown(
                                id="summary-method-select",
                                options=[
                                    {"label": "Simple Extractive", "value": "se"}, 
                                    {"label": "LexRank", "value": "lexR"},
                                    {"label": "TextRank", "value": "texR"},
                                    {"label": "Latent Semenatic Analysis", "value": "lsa"},
                                    {"label": "Luhn's Algorithm", "value": "luhn"},
                                    {"label": "BART", "value": "bart"},
                                    {"label": "OpenAI", "value": "openai"},
                                ],
                                value="se",
                                multi=False,
                                clearable=False,
                            )
                        ]
                    ),
                    html.Div(
                        children=[
                            html.H3("Summary Size (% of Original)"),
                            dcc.Slider(
                                id="summary-size-slider",
                                min=5,
                                max=100,
                                step=5,
                                value=50,
                                included=False,
                                marks=None,
                                tooltip={
                                    "placement": "bottom", 
                                    "always_visible": True
                                }
                            )
                        ]
                    ),
                    html.Button(
                        id="summary-btn",
                        children="Summarise Documents",
                        className="nlp-btn-disabled",
                        disabled=True,
                    )
                ]
            ),
            html.Div(
                id="summary-output",
                children=[
                    dcc.Loading(
                        color="#003049",
                        children=[
                            dbc.Textarea(
                                id="summary-output-content",
                                value="",
                                draggable=False,
                                readOnly=True,
                                placeholder="The summary of your document(s) will appear here."
                            )
                        ])
                    ]
                )
            ]
        )

### Clustering Section
def get_clustering_section():
    if docs is None or len(docs) < 2:
        text = "Please upload 2 or more documents to get started with document clustering."
        return html.H2(
            children=text,
            className="no-docs-heading"
        )

    docs_copy = docs.copy(deep=True)
    doc_list = docs_copy["title"]

    return html.Div(
        id="clustering-section",
        children=[
            html.Div(
                id="clustering-params",
                children=[
                    dcc.Dropdown(
                        id="clustering-doc-select",
                        options=doc_list,
                        multi=True,
                        placeholder="Select documents..."
                    ),
                    dcc.Dropdown(
                        id="clustering-num-select", 
                        options=[
                            {"label": str(i), "value": i}
                            for i in range(2, len(doc_list) + 1)
                        ],
                        multi=False,
                        placeholder="Number of clusters",
                        clearable=False,
                        value=2,
                    ),
                    html.Button(
                        id="clustering-btn",
                        children="Cluster Documents",
                        className="nlp-btn-disabled",
                        disabled=True,
                    )
                ]
            ),
            html.Div(
                id="clustering-fig-container",
                children=[
                    dcc.Loading([
                        dcc.Graph(
                            id="clustering-plot",
                            figure=dc.plot_data()
                        )
                    ])
                ]
            )
        ]
    )

### WikiBot Section
def get_wiki_bot_section():
    return html.Div(
        id="wikibot-section",
        children=[
            html.I(
                id="wikibot-icon", 
                className="bi bi-wikipedia", 
                children=[html.Span("ikiBot")],
            ),
            html.H3(id="wikibot-tagline", children=WIKIBOT_TAGLINE),
            html.Div(
                id="wikibot-params",
                children=[
                    dbc.Input(
                        id="wikibot-query",
                        placeholder="Enter your question here",
                        value="",
                        persistence=False,
                    ),
                    dbc.Select(
                        id="wikibot-method-select",
                        placeholder="Select a Search Method",
                        options=[
                            {"label": "TF-IDF", "value": "tf-idf"}, 
                            {"label": "Cosine Similarity", "value": "cosine_sim"},
                            {"label": "BERT", "value": "bert2"},
                            {"label": "OpenAI", "value": "openai"}
                        ],
                        value=None,
                        persistence=False,
                    ),
                    html.Button(
                        id="wikibot-btn",
                        children="Search",
                        className="nlp-btn-disabled",
                        disabled=True,
                    )
                ]
            ),
            html.Div(
                id="wikibot-output",
                children=[
                    dcc.Loading(
                        color="#003049",
                        children=[
                            dbc.Textarea(
                                id="wikibot-output-content",
                                value="",
                                draggable=False,
                                readOnly=True,
                                placeholder="The results of your query will appear here"
                            )
                        ]
                    )
                ]
            )
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
    Output("edit-doc-btn", "className"),
    Output("edit-doc-btn", "disabled"),
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
        return (
            "doc-btn-disabled", 
            True, 
            "doc-btn",
            False,
            "doc-btn", 
            False, 
            "doc-btn", 
            False
        )
    elif item_id is None:
        current_doc = None
        return (
            "doc-btn", 
            False,
            "doc-btn-disabled",
            True, 
            "doc-btn-disabled", 
            True, 
            "doc-btn-disabled", 
            True
        )

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
    Output("edit-doc-modal", "is_open"),
    Output("edit-doc-modal-heading", "children"),
    Output("edit-doc-name", "value"),
    Output("edit-doc-content", "value"),
    Input("edit-doc-btn", "n_clicks"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def edit_doc_handler(n_clicks):
    global current_doc
    if n_clicks is not None:
        return (
            True, 
            current_doc["title"], 
            current_doc["title"], 
            current_doc["content"]
        )

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
    Output("reload-handler-3", "children"),
    Output("confirm-edit-doc", "displayed"),
    Output("confirm-edit-doc-error", "displayed"),
    Output("confirm-edit-doc-error", "message"),
    State("edit-doc-name", "value"),
    State("edit-doc-content", "value"),
    Input("edit-doc-modal-btn", "n_clicks"),
)
def save_doc_handler(doc_name, doc_content, n_clicks):
    global docs
    global current_doc

    if n_clicks is not None and n_clicks > 0 and current_doc is not None:
        err_messages = [
            "Please enter a name for your file.",
            "Please enter some content for your file.",
            "Error: Your document could not be saved. Please try again.",
        ]

        if doc_name.strip() == "" and doc_content.strip() == "":
            return no_update, False, True, "\n".join(err_messages[:-1])
        elif doc_name.strip() == "":
            return no_update, False, True, err_messages[0]
        elif doc_content.strip() == "":
            return no_update, False, True, err_messages[1]
        
        doc_id = current_doc["public_id"]
        try:
            fh.delete_document(doc_id)
            res = fh.create_new_file(doc_name, doc_content)
            if not res:
                return no_update, False, True, err_messages[2]
            
            docs = fh.get_documents()
            return None, True, False, ""
        except Exception as e:
            print(e)
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
    Output("reload-handler-4", "children"),
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
    Output("info-extract-output-content", "value"),
    State("info-extract-doc-select", "value"),
    State("info-extract-method-select", "value"),
    State("info-extract-query", "value"),
    Input("info-extract-btn", "n_clicks"),
)
def info_extract_handler(select_docs, method, query, n_clicks):
    if n_clicks is not None:
        corpus = {
            doc_name: docs[
                docs["title"] == doc_name
            ].to_dict("records")[0]["content"]
            for doc_name in select_docs
        }
        info_extractor.load_files(corpus)
        try:
            answer = info_extractor.search(query, method)
            info_extractor.clear_files()
            return answer
        except Exception as e:
            print(e)
            return "Error: Something went wrong."
    return ""

## Summarisation Page Callbacks
@app.callback(
    Output("summary-btn", "disabled"),
    Output("summary-btn", "className"),
    Input("summary-doc-select", "value"),
)
def summary_params_handler(documents):
    if documents is not None and len(documents) > 0:
        return False, "nlp-btn"
    return True, "nlp-btn-disabled"

@app.callback(
    Output("summary-output-content", "value"),
    State("summary-doc-select", "value"),
    State("summary-method-select", "value"),
    State("summary-size-slider", "value"),
    Input("summary-btn", "n_clicks"),
)
def summary_handler(select_doc, method, summary_size, n_clicks):
    if n_clicks is not None:
        corpus = {
            select_doc: docs[
                docs["title"] == select_doc
            ].to_dict("records")[0]["content"]
        }
        try:
            doc_summariser.load_files(corpus)
            summary = doc_summariser.summarise(
                method, 
                [select_doc], 
                summary_size/100
            )
            doc_summariser.clear_files()
            return summary if summary.strip() != "" else "[SUMMARY SIZE TO SMALL]"
        except Exception as e:
            print(e)
            return "Error: Something went wrong."
    return ""

# Document Clustering Page Callbacks
@app.callback(
    Output("clustering-btn", "disabled"),
    Output("clustering-btn", "className"),
    Input("clustering-doc-select", "value"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def clustering_params(documents):
    if documents is not None and len(documents) > 1:
        return False, "nlp-btn"
    return True, "nlp-btn-disabled"

@app.callback(
    Output("clustering-plot", "figure"),
    State("clustering-doc-select", "value"),
    State("clustering-num-select", "value"),
    Input("clustering-btn", "n_clicks"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def clustering_handler(select_docs, num_clusters, n_clicks):
    if n_clicks is not None:
        corpus = {
            doc_name: docs[
                docs["title"] == doc_name
            ].to_dict("records")[0]["content"]
            for doc_name in select_docs
        }
        true_cluster_num = min(num_clusters, len(select_docs))
        try:
            cluster_data, doc_data = dc.doc_clustering(corpus, true_cluster_num)
            cluster_plot = dc.plot_clusters(
                doc_data, 
                cluster_data,
                "z_coord" in cluster_data and len(select_docs) > 3
            )
            return cluster_plot
        except Exception as e:
            print(e)
            return go.Figure()
    return go.Figure()

# WikiBot Page Callbacks
@app.callback(
    Output("wikibot-btn", "disabled"),
    Output("wikibot-btn", "className"),
    Input("wikibot-query", "value"),
    Input("wikibot-method-select", "value"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def wikibot_params(query, method):
    if query.strip() != "" and method is not None:
        return False, "nlp-btn"
    return True, "nlp-btn-disabled"

@app.callback(
    Output("wikibot-output-content", "value"),
    State("wikibot-query", "value"),
    State("wikibot-method-select", "value"),
    Input("wikibot-btn", "n_clicks"),
    suppress_callback_exceptions=True,
    prevent_initial_call=True,
)
def wikibot_handler(query, method, n_clicks):
    if n_clicks is not None:
        try:
            answer = wikibot.search(query, method)
            return answer
        except Exception as e:
            print(e)
            return f"Error — something went wrong\n{e}"
    return ""

# Running server
if __name__ == "__main__":
    app.run_server(debug=False)