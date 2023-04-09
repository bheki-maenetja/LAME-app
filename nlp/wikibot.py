# Third-Party Imports
import spacy
import nltk
from nltk.stem import WordNetLemmatizer
# nltk.download("wordnet")
import wikipediaapi
import requests as r
from bs4 import BeautifulSoup

# Standard Library Imports
import os
import sys
from math import inf
from string import punctuation

# Local Imports
from nlp.info_extraction import DocSearcher

# WikiBot Class
class WikiBot:
    def __init__(self):
        self._main_corpus = dict()
        self._doc_searcher = DocSearcher()
        self._nlp = spacy.load("en_core_web_sm")
    
    def search(self, query, method):
        # Get searchable entities from query
        search_ents = self._searchable_entities(query)

        # Build corpus of relevant wikipedia articles
        wiki_corpus = self._build_wiki_corpus(search_ents)

        # Run doc searcher on new corpus of articles
        self._doc_searcher.load_files(wiki_corpus)
        result = self._doc_searcher.search(query, method)
        self._doc_searcher.clear_files()

        # Update the main corpus of wikipedia articles
        self._main_corpus.update(wiki_corpus)

        # Update and return search result
        result += "\n\nRelated articles\n• " + "\n• ".join([k[2] for k in wiki_corpus.keys()])
        return result

    def _get_named_entities(self, query):
        # Intialise nlp model
        nlp = self._nlp
    
        # Get entities from queries
        doc = nlp(query)
        entities = { ent.text for ent in doc.ents }
        return entities
    
    def _word_tokenize(self, text, lower_case=False):
        banned = list(punctuation) + nltk.corpus.stopwords.words("english")
        
        if lower_case:
            return [
            w.lower() for w in nltk.word_tokenize(text) 
            if w.lower() not in banned
        ]
        
        return [
            w for w in nltk.word_tokenize(text) 
            if w.lower() not in banned
        ]
    
    def _get_improper_nouns(self, query):
        lemma = WordNetLemmatizer()
        pos_tags = nltk.pos_tag(self._word_tokenize(query))
        return {
            lemma.lemmatize(tag[0]).lower() 
            for tag in pos_tags 
            if tag[-1] in ("NN", "NNS")
        }
    
    def _searchable_entities(self, query):
        improper_nouns = self._get_improper_nouns(query)
        named_entities = self._get_named_entities(query)
        return improper_nouns.union(named_entities)
    
    def _article_id(self, term):
        base_url = "https://en.wikipedia.org/wiki/"
        res = r.get(base_url + term)

        if res.status_code == 200:
            doc_text = res.text
            soup = BeautifulSoup(doc_text, "html.parser")
            return soup.find(id="t-wikibase").a.attrs['href'].split("/")[-1]
        
        return None

    def _build_wiki_corpus(self, search_ents):
        wiki = wikipediaapi.Wikipedia('en')
        ids = [k[0] for k in self._main_corpus.keys()]
        new_corpus = dict()
        
        for ent in search_ents:
            page = wiki.page(ent)
            if page.exists():
                doc_id = self._article_id(ent)
                key = (doc_id, page.title, page.fullurl)
                if doc_id not in ids:
                    new_corpus[key] = page.text
                    ids.append(doc_id)
                else:
                    print(f"{ent} is already in corpus.")
                    new_corpus[key] = self._main_corpus[key]
        
        return new_corpus