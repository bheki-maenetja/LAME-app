# Third-Party Imports
from dash import html, dcc
import dash_bootstrap_components as dbc

# Standard Imports
# Local Imports

wikibot_user_message = html.Div(
    id="wikibot-message",
    className="user",
    children=[
        html.Div(
            id="wikibot-message-content",
            className="user",
            children="This is a user message. Lorem ipsum bla bla bla...",
        )
    ]
)

wikibot_bot_message = html.Div(
    id="wikibot-message",
    className="bot",
    children=[
        html.Div(
            id="wikibot-message-content",
            className="bot",
            children="This is a bot message. Lorem ipsum bla bla bla...",
        )
    ]
)

def get_wiki_bot_section(tagline):
    return html.Div(
        id="wikibot-section",
        children=[
            html.I(
                id="wikibot-icon", 
                className="bi bi-wikipedia", 
                children=[html.Span("ikiBot")],
            ),
            html.H3(id="wikibot-tagline", children=tagline),
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
                            {"label": "BERT", "value": "bert"},
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

def get_wiki_bot_section_2(tagline):
    return html.Div(
        id="wikibot-section",
        children=[
            html.Div(
                id="wikibot-params",
                children=[
                    # html.H3(id="wikibot-tagline", children=tagline),
                    dbc.Select(
                        id="wikibot-method-select",
                        placeholder="Select a Search Method",
                        options=[
                            {"label": "TF-IDF", "value": "tf-idf"}, 
                            {"label": "Cosine Similarity", "value": "cosine_sim"},
                            {"label": "BERT", "value": "bert"},
                            {"label": "OpenAI", "value": "openai"}
                        ],
                        value=None,
                        persistence=False,
                    ),
                ],
                style={"flexDirection":"column"}
            ),
            html.Div(
                id="wikibot-message-space",
                children=[
                    html.Div([], style={"flexGrow":"1"}),
                    wikibot_bot_message,
                    wikibot_user_message,
                    wikibot_bot_message,
                ]
            ),
            html.Div(
                id="wikibot-params",
                children=[
                    dbc.Input(
                        id="wikibot-query",
                        placeholder="Enter your question here",
                        value="",
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
        ]
    )