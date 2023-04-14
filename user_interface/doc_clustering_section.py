# Third-Party Imports
from dash import html, dcc
import dash_bootstrap_components as dbc

# Standard Imports
# Local Imports
import nlp.doc_clustering as dc

def get_clustering_section(docs):
    if docs is None or len(docs) < 2:
        text = "Please upload 2 or more documents to get started with semantic visualisation."
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
                        children="Create Visualisation",
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
