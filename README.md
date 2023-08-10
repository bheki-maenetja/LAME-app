# Lexical Analyser Manipulator and Extractor (LAME)
Lexical Analyser Manipulator and Extractor (LAME) is a web-based word processing application that allows users to perform information extraction and text summarisation on documents. It also features a chatbot tool that uses Wikipedia articles to answer natural language queries.

## Getting Started
### Installation
- Clone this repository by running the terminal command `git clone git@github.com:bheki-maenetja/LAME-app.git`.
- In the root folder run the terminal command `pipenv shell`. Ensure that you have Python 3.9 installed on your device.
- In the root folder run the terminal command `pipenv install` to install all necessary packages and modules for the backend.
- Create an `.env` file to store your own keys for the OpenAI and HuggingFace APIs; assign these keys to `OPENAI_API_KEY` and `HUGGING_FACE_API_KEY` respectively.
- In the same `.env` file add the backend url `https://lame-backend-7c4f83e7614c.herokuapp.com` and assign it to `BACKEND_URL`.
- To view the site locally run the terminal command `python app.py` and navigate to localhost:8050 in your web browser.

### Deployment
- You can view the deployed version of the site [here](https://web-production-f2c0.up.railway.app/).

## Technologies Used
- Python 3.9
- Plotly/Dash
- Django
- PostgreSQL
- CSS (incl. Bootstrap)
- Third-party APIs
  * [OpenAI](https://openai.com/blog/openai-api/)
  * [Hugging Face](https://huggingface.co/)

## Overview
Lexical Analyser Manipulator and Extractor (LAME) is a project that seeks to explore natural language processing (NLP) techniques as applied to the tasks of information extraction and text summarisation. The project explored methods from the symbolic, statistical and neural approaches to NLP and tied together some of their most prevalent techniques in a practical implementation that provides real-world utility to users. The system — a web-based word processing application — allows users to perform information extraction and text summarisation on documents. It also features a chatbot tool that uses Wikipedia articles to answer natural language queries.

### Documents
<figcaption>The Documents Page</figcation>
<kbd>
<img src="/assets/docsPage.png" width="45%" />
</kbd>
<kbd>
<img src="/assets/docsPage-2.png" width="45%" />
</kbd>

### Information Extraction
### Text Summarisation
### Semantic Visualisation
### WikiBot