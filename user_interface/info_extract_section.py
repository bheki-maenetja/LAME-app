# Third-Party Imports
from dash import html, dcc
import dash_bootstrap_components as dbc

# Standard Imports
# Local Imports

def get_info_extraction_section(docs):
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
                    html.Div(children=[html.H3("Query"),
                    dbc.Input(
                        id="info-extract-query",
                        placeholder="Enter your query here",
                        value="",
                        persistence=False,
                    )]),
                    html.Button(
                        id="info-extract-btn",
                        children="Extract Info",
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