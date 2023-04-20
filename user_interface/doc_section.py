# Third-Party Imports
from dash import html, dcc
import dash_bootstrap_components as dbc

# Standard Imports
from datetime import datetime

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

def get_doc_section(docs):
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
                                            html.P(f"Date of creation: {parse_time_string(doc['created_at'])}"),
                                            html.P(f"Word count: {doc['word_count']}"),
                                            html.P(f"Character count: {doc['char_count']}"),
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

# Utility functions
def parse_time_string(t_string):
    parsed_time = datetime.strptime(t_string, "%Y-%m-%dT%H:%M:%SZ")
    return parsed_time.strftime("%Y-%m-%d at %H:%M")