# Third-Party Imports
import torch
import nltk
from sentence_transformers import SentenceTransformer, util

import requests as req
import openai

from dotenv import load_dotenv
load_dotenv()

# Standard Imports
import os
import json
from string import punctuation
from math import log1p, inf

# Local Imports

# Tokenization
def tokenize(doc, remove_stopwords=True):
    banned = list(punctuation)
    
    if remove_stopwords:
        banned += nltk.corpus.stopwords.words("english")
    
    return [
        w.lower() for w in nltk.word_tokenize(doc)
        if w.lower() not in banned
    ]

# Document Searcher Class
class DocSearcher():
    def __init__(self):
        self._corpus = dict()
        self._file_matches = 2
        self._sentence_matches = 5
        self._sent_transformer = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2"
        )
    
    def view_corpus(self):
        return self._corpus

    def load_files(self, corpus):
        self._corpus = corpus
    
    def clear_files(self):
        self._corpus = dict()

    def search(self, query, s_method="tf-idf"):
        fnames = self._corpus.keys()

        if s_method == "tf-idf":
            joint_context, ranked_sents = self._context_and_sents_idf(query, fnames)
            output_text = self._build_output_text(ranked_sents, inf)
            answer = " ".join(nltk.sent_tokenize(output_text)[:self._sentence_matches])
            return answer
        
        joint_context, ranked_sents = self._context_and_sents_cosine(query, fnames)
                
        if s_method == "cosine_sim":
            output_text = self._build_output_text(ranked_sents, inf)
            answer = " ".join(nltk.sent_tokenize(output_text)[:self._sentence_matches])
        elif s_method == "bert":
            output_text = self._build_output_text(ranked_sents, 2048)
            answer = self._run_model_bert(query, output_text)
        elif s_method == "openai":
            output_text = self._build_output_text(ranked_sents, 2500)
            answer = self._run_model_openai(query, output_text)
        
        return answer.strip()
    
    def _build_output_text(self, ranked_sents, max_length=512):
        output_text = ''

        for sent in ranked_sents:
            new_sent = sent[0]
            if len(nltk.word_tokenize(f'{output_text} {new_sent}')) <= max_length:
                output_text += f' {new_sent}'
            else:
                break

        return output_text
    
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

    def _context_and_sents_idf(self, query, fnames):
        idfs = self._compute_idfs(fnames)
        top_files = self._top_files_idf(query, idfs)

        joint_context = "\n".join(self._corpus[name] for name in top_files)

        ranked_sents = self._sent_rank_idf(query, joint_context, idfs)

        return joint_context, ranked_sents
    
    def _context_and_sents_cosine(self, query, fnames):
        top_files = self._top_files_cosine(query, fnames)
        joint_context = "\n".join(self._corpus[name] for name in top_files)

        ranked_sents = self._sent_rank_cosine(query, joint_context)

        return joint_context, ranked_sents

    def _cosine_similarity(self, text_1, text_2, model):
        embedding_1 = model.encode(text_1, convert_to_tensor=True)
        embedding_2 = model.encode(text_2, convert_to_tensor=True)
    
        return float(util.pytorch_cos_sim(embedding_1, embedding_2))
    
    def _compute_idfs(self, fnames):
        file_idfs = dict()
        unique_words = set()
        num_docs = len(fnames)

        for name in fnames:
            for sent in nltk.sent_tokenize(self._corpus[name]):
                unique_words = set().union(
                    unique_words, 
                    set(self._word_tokenize(sent))
                )
                
        for word in unique_words:
            num_apps = sum(1 for name in fnames if word in self._corpus[name])
            if num_apps > 0:
                file_idfs[word] = log1p(num_docs / num_apps)
        
        return file_idfs

    def _top_files_idf(self, query, idfs):
        tf_idfs = { fname: 0 for fname in self._corpus }

        query = self._word_tokenize(query)

        for w in query:
            for fname in self._corpus:
                tf_idfs[fname] += self._corpus[fname].count(w) * idfs.get(w, 0)
        
        ranked_files = sorted(
            tf_idfs.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return [file[0] for file in ranked_files][:self._file_matches]
    
    def _top_files_cosine(self, query, fnames):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

        ranked_files = sorted([
            (name, self._cosine_similarity(query, self._corpus[name], model))
            for name in fnames
        ], key=lambda x: x[1], reverse=True)

        return [file[0] for file in ranked_files][:self._file_matches]
    
    def _word_tokenize(self, words):
        banned = list(punctuation) + nltk.corpus.stopwords.words("english")

        return [
            w.lower() for w in nltk.word_tokenize(words)
            if w.lower() not in banned
        ]
    
    def _sent_rank_idf(self, query, context, idfs):
        query_set = set(self._word_tokenize(query))
        sent_scores = { sent: [0,0] for sent in nltk.sent_tokenize(context)}

        for sent in sent_scores:
            sent_set = set(self._word_tokenize(sent))
            common_words = query_set.intersection(sent_set)
            sent_scores[sent][0] += sum(idfs.get(w, 0) for w in common_words)
            sent_scores[sent][1] += len(common_words)
        
        ranked_sents = sorted(
            sent_scores.items(),
            key=lambda x: (x[1][0], x[1][1]),
            reverse=True
        )

        return [(sent, score[0]) for sent, score in ranked_sents]

    def _sent_rank_cosine(self, query, context):
        model = self._sent_transformer
        sent_scores = {
            sent: self._cosine_similarity(query, sent, model)
            for sent in nltk.sent_tokenize(context)
        }
    
        ranked_sents = sorted(
            sent_scores.items(),
            key = lambda x: x[1],
            reverse=True
        )
    
        return ranked_sents