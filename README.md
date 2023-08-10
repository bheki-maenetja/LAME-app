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
<img src="/assets/docsPage.png" width="100%" />
<img src="/assets/docsPage-2.png" width="100%" />
</kbd>
<hr>
<figcaption>Users can create, upload and edit documents</figcaption>
<kbd>
<img src="/assets/docsPage.gif" width="100%" />
</kbd>

### Information Extraction
<figcaption>Users can use natural language queries to extract information from documents</figcaption>
<kbd>
<img src="/assets/infoExtract.png" width="100%" />
</kbd>

### Text Summarisation
<figcaption>Users can create text summaries of single or multiple documents</figcaption>
<kbd>
<img src="/assets/textSum.png" width="100%" />
</kbd>

### Semantic Visualisation
<figcaption>Users can visualise the semantic similarities between documents</figcaption>
<kbd>
<img src="/assets/semVis.png" width="100%" />
</kbd>

### WikiBot
<figcaption>Users can interact with a chatbot tool that uses Wikipedia articles to answer natural language queries</figcaption>
<kbd>
<img src="/assets/wikibot.gif" width="100%" />
</kbd>

## Development
This project is a fullstack web application. The backend consists of a PostgreSQL database hosted on a Django server. The frontend was built using Dash and styled with regular CSS as well as the Bootstrap CSS framework. The backend is quite basic, with only one Django app and model for documents created/uploaded by the user. The backend is hosted on a different service (Heroku) to the frontend (which is hosted on Railway) and thus needs to be accessed via HTTP requests.

### User Interface
- Whilst the application logic (including the NLP functionality) was written in “standard” python, the user interface was developed with a python library called Dash.
- Dash allows for the seamless integration of application logic with the user interface. The is done through special functions known as “callbacks”. Callbacks are a way of retrieving the values of UI components, such as the text inside of a form or the numerical value of a slider. These functions are automatically called whenever an input UI component's property changes, in order to update some property in another UI component (the output).
- LAME uses Cascading Style Sheets (CSS) to style and properly lay out the system’s various UI components. Dash has a built-in integration that allows it to work with CSS files. The styling of the UI also makes use of [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/) – a library of CSS styles and custom UI components from the popular Bootstrap CSS framework.

### Text Processing
- All of the NLP techniques for information extraction and text summarisation require some degree of pre-processing for their inputs. Specifically, these techniques make use of tokenisation; the process of breaking down a piece of text into smaller units called tokens.
- In LAME, tokenisation is implemented with the help of [Natural Language Toolkit (NLTK)](https://www.nltk.org/). NLTK is a popular open-source library for natural language processing. It provides a wide range of tools and functions for various NLP tasks, including tokenisation. With NLTK, tokenization can be performed using the `word_tokenize()` and `sent_tokenize()` functions; these functions break down text into word and sentence tokens respectively.
```
# Tokenisation and chunking functions used in LAME

def tokenize(doc, remove_stopwords=True):
    banned = list(punctuation)
    
    if remove_stopwords:
        banned += nltk.corpus.stopwords.words("english")
    
    return [
        w.lower() for w in nltk.word_tokenize(doc)
        if w.lower() not in banned
    ]

def _chunk_text(self, text, chunk_len):
        chunks = []
        current_chunk = ""
        sents = nltk.sent_tokenize(text)

        for sent in sents:
            if len(nltk.word_tokenize(current_chunk + f" {sent}")) >= chunk_len:
                chunks.append(current_chunk)
                current_chunk = ""
            else:
                current_chunk += f" {sent}"

        chunks.append(current_chunk)

        return chunks
```

### Information Extraction
- LAME uses two statistical NLP methods for information extraction: term frequency - inverse document frequency (TF-IDF) and cosine similarity. LAME also uses two information extraction methods from the neural approach to NLP: Bidirectional Encoder Representations from Transformers (BERT) and OpenAI’s Generative Pre-trained Transformer 3 (GPT-3).
- LAME’s implementation of TF-IDF is a [loose adaptation](https://cs50.harvard.edu/ai/2020/projects/6/questions/) of a TF-IDF exercise in one of Harvard University’s free online AI courses. LAME’s implementation of cosine similarity is very similar to its implementation of TF-IDF. But instead of ranking documents and sentences by term frequencies and inverse document frequencies, the method encodes documents, sentences, and the query into a high-dimensional vector and measures the similarity between vectors.
- LAME makes use of BERT through the Hugging Face API. Each time a user makes a query, LAME sends a request to the API with the relevant query, context and other model parameters. BERT then runs on the text using Hugging Face’s own GPU powered servers. LAME makes use of GPT-3 through OpenAI’s Completions API. Similar to BERT, LAME makes a request to OpenAI’s servers whenever a user makes a query.
```
def _run_model_bert(self, query, context):
    # Get API url and headers
    api_url = "https://api-inference.huggingface.co/models/bert-large-uncased-whole-word-masking-finetuned-squad"
    headers = {
        "Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"
    }

    payload = {
        "inputs": {
         	"question": query,
            "context": context
        }
    }

    data = json.dumps(payload)
    res = req.request("POST", api_url, headers=headers, data=data)
    content = json.loads(res.content.decode("utf-8"))
    answer = content.get("answer", None)
    if not answer:
        return f"Error:  {content.get('error', 'Something is wrong')}"
    return answer

def _run_model_openai(self, query, text):
	openai.api_key = os.getenv("OPENAI_API_KEY")

    res = openai.Completion.create(
        model="text-davinci-003", 
        prompt=f"Context: {query} Query: {text}\n\nUsing only the context given, answer the query.", 
        temperature=0,
        max_tokens=500,
    )
        
    return res.choices[0].text
```

### Text Summarisation
- LAME uses five statistical NLP methods for text summarisation: simple extractive summarisation, LexRank, TextRank, latent semantic analysis (LSA) and Luhn’s algorithm. LAME uses two techniques from the neural approach to NLP: Bidirectional and Auto-Regressive Transformers (BART) and OpenAI’s Generative Pre-trained Transformer 3 (GPT-3); these technques allow for abstractive text summarisation.
- LAME uses the implementations of LexRank, TextRank, LSA and Luhn's algorithm provided by [Sumy](https://miso-belica.github.io/sumy/) – a python module that provides a raft of extractive text summarisation techniques for the automatic summarisation of documents as well as HTML pages.
- LAME’s implementation of BART is almost identical to its implementation of BERT for information extraction. A request is made to the Hugging Face API. The model – provided with the input text and relevant parameters – is run on Hugging Face’s servers with the results returned to LAME.
- Similar to LAME’s use of GPT-3 for information extraction, LAME’s use of the LLM for text summarisation is also done through OpenAI’s Completions API.
```
# LAME's implementatiuon of LexRank, TextRank, LSA and Luhn's algorithm for text summarisation

def _algo_summary(self, text, method, summary_size=0.5):
    # Get sentence and summary lengths
    sent_length = len(nltk.sent_tokenize(text))
    summary_len = max(int(summary_size * sent_length), 1)

    # Initialise summariser
    if method == "lexR":
        summariser = LexRankSummarizer()
    elif method == "texR":
        summariser = TextRankSummarizer()
    elif method == "lsa":
        summariser = LsaSummarizer()
    elif method == "luhn":
        summariser = LuhnSummarizer()

    # Initialise parser
    parser = PlaintextParser(text, Tokenizer("english"))

    # Create summary
    summary_sents = summariser(parser.document, summary_len)

    return " ".join(str(s) for s in summary_sents)
```

### Visualising Semantic Similarity
- LAME creates visualisations of semantic similarity by performing clustering on a given corpus of documents using a combination of TF-IDF and the k-means clustering algorithm. 
- Documents are first pre-processed through the use of tokenisation. Feature extraction is then performed, by representing documents as TF-IDF vectors using the TfIdfVectoriser class from scikit-learn. 
- The k-means algorithm is then applied to the feature matrix using scikit-learn’s KMeans class. Users can choose the number of clusters into which they want to organise their documents.
- After the document clusters have been found, the function applies principal component analysis (PCA) to the feature matrix to reduce its dimensionality to two or three dimensions. PCA is performed using the PCA class from scikit-learn. 
- The reduced feature matrix is then used to identify the top themes for each cluster. These themes, along with the clusters, are then rendered in a two- or three-dimensional interactive plot.
```
# Clustering documents

def doc_clustering(corpus, num_clusters=2):
    # Get original documents
    docs = list(corpus.items())
    
    # Preprocess documents
    processed_docs = [
        ' '.join(word_tokenize(doc[1])) 
        for doc in docs
    ]
    
    # Extract features from documents
    vectoriser = TfidfVectorizer()
    X = vectoriser.fit_transform(processed_docs)
    
    # Cluster documents
    kmeans = KMeans(n_clusters=num_clusters, init="random", max_iter=2000)
    kmeans.fit(X)
    
    # Principal components
    num_comps = 3 if num_clusters > 2 else 2

    pca = PCA(n_components=num_comps)
    prin_comps = pca.fit_transform(X.toarray())
    
    # Identify Themes
    cluster_data = {
        "name": [],
        "themes": []
    }
    
    for i in range(num_clusters):
        centroid = kmeans.cluster_centers_[i]
        top_words_idx = centroid.argsort()[::-1][:5]
        top_words = [
            vectoriser.get_feature_names_out()[idx] 
            for idx in top_words_idx
        ]
        cluster_data["name"].append(i)
        cluster_data["themes"].append(", ".join(top_words))
    
    centroid_comps = pca.fit_transform(kmeans.cluster_centers_)
    
    cluster_data["x_coord"] = centroid_comps[:, 0]
    cluster_data["y_coord"] = centroid_comps[:, 1]
    if num_comps > 2: cluster_data["z_coord"] = centroid_comps[:, 2]
    
    doc_data = {
        "doc_name": [doc[0] for doc in docs],
        "x_coord": prin_comps[:, 0],
        "y_coord": prin_comps[:, 1],
        "cluster": kmeans.labels_
    }
    if num_comps > 2:
        doc_data.update({"z_coord": prin_comps[:, 2]})
    
    return pd.DataFrame.from_dict(cluster_data), pd.DataFrame.from_dict(doc_data)
```

### WikiBot
- The WikiBot works in much the same way as the Information Extraction section with the key difference being that user queries are answered by performing information extraction – using the exact same NLP techniques as the Information Extraction section – on Wikipedia articles instead of locally created/uploaded documents.
- In order to find the relevant Wikipedia articles on which to perform information extraction, the WikiBot carefully gleans any important terms or named entities that may be present in the user’s query. This is done through a combination of tokenisation, lemmatisation and named-entity recognition (NER).
- Once the WikiBot has identified all the important terms or named entities in the user’s query, it then searches Wikipedia for articles related to those terms. This is done through Wikipedia’s own API that allows for the quick search and retrieval of Wikipedia articles. When the relevant articles have been retrieved and assembled, the WikiBot then performs information extraction using the selected NLP method.
```
# Search function for the WikiBot

def search(self, query, method):
    # Get searchable entities from query
    search_ents = self._searchable_entities(query)

    # Build corpus of relevant wikipedia articles
    wiki_corpus = self._build_wiki_corpus(search_ents)
    if wiki_corpus == {}: return "Results not found...Sorry", []

    # Run doc searcher on new corpus of articles
    self._doc_searcher.load_files(wiki_corpus)
    result = self._doc_searcher.search(query, method)
    self._doc_searcher.clear_files()

    # Update the main corpus of wikipedia articles
    self._main_corpus.update(wiki_corpus)

    # Update and return search result
    articles = [k[2] for k in wiki_corpus.keys()]
    return result, articles
```

## Reflection
### Challenges
- Whilst there were no serious obstacles during the development of LAME, getting to grips with the multitude of libraries, packages and APIs necessary for its NLP functionality was quite tedious at times and definitely slowed down the development process.

### Room for Improvement
- **Better hardware:** a limiting factor of LAME’s NLP functionality is the hardware resources on which it is hosted. Some of the statistical NLP techniques used by LAME are computationally expensive, needing to make thousands of calculations in order to deliver a result; this only becomes apparent for large documents. LAME is hosted across a CPU-based machinery on Heroku and Railway. Given that these services do not provide GPU-accelerated hardware, the only possible resolutions for this issue are to find algorithmic efficiencies in the system’s code base or to move the entire system to a new hosting service.
- **A more powerful document editor:** LAME's document editing capabilities fall well short of commercial word processors such as Microsoft Word and Google Docs. LAME’s document editor is more akin to a basic text editor, with users being unable to apply stylistic changes such as changing font colour/size/weight or underlining/highlighting text. This limits LAME’s utility as an out-and-out word processor and places more of an emphasis on its NLP capabilities.

## Future Features
- **User accounts:** given that LAME was originally devised as merely a practical implementation of certain NLP techniques and a demonstration of how those techniques can be integrated into a word processor application, it currently does not feature any authentication mechanism or user accounts; meaning all documents on LAME are accessible to all users of LAME. Obviously, to make the system viable for serious personal and commercial use, LAME will need to have some sort of authentication layer coupled with the provision of user accounts that can associate individual users with only the documents that they create and/or upload to the system. This will require a redesign of the system’s backend.
- **Language translation:** another possible future addition to the next iteration of LAME is an expansion of its NLP capabilities; specifically, the addition of language translation features. Currently, LAME uses NLP techniques for the tasks of information extraction and text summarisation. And, it can only do so effectively for English language documents. However, many of the NLP techniques used by LAME – particularly those from the neural approach – can be applied to the task of language translation. The addition of language translation capabilities to LAME would enhance the system’s utility in two significant ways. Firstly, it would allow users to perform information extraction and text summarisation on documents written in languages other than English. Secondly, users would be able to take existing documents and translate them between different languages.
- **Additional word processing features:** as mentioned in the "Room for Improvement" section, LAME’s document editor lacks many of the helpful formatting tools common in modern word processor applications. Therefore, any future version of the system will certainly include a greater breadth of text formatting features that allow users to apply a variety of stylistic changes to the document text. This will also include mechanisms for structuring text such as bullet point (or numbered) lists and headers & footers.