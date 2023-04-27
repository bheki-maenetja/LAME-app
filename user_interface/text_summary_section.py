# Third-Party Imports
from dash import html, dcc
import dash_bootstrap_components as dbc

def get_summary_section(docs):
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
                                multi=True,
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