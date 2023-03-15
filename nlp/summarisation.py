# Third-Party Imports
import nltk
import requests as req
import openai
from dotenv import load_dotenv
load_dotenv()

from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.luhn import LuhnSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer

# Standard Imports
import os
import json
from string import punctuation

# Local Imports

# Document Summariser Class
class DocSummariser():
    def __init__(self):
        self._corpus = dict()
    
    def get_corpus(self):
        return self._corpus

    def load_files(self, corpus):
        self._corpus = corpus
    
    def clear_files(self):
        self._corpus = dict()
    
    def _word_tokenize(self, text):
        banned = list(punctuation) + nltk.corpus.stopwords.words("english")
        return [
            w for w in nltk.word_tokenize(text) 
            if w not in banned
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
    
    def summarise(self, method, fnames, summary_size):
        # Build input text
        text = " ".join(self._corpus[name] for name in fnames)
        
        # Choose method and return summary
        if method == "se":
            return self._SE_summary(text, summary_size)
        elif method in ("lexR", "texR", "lsa", "luhn"):
            return self._algo_summary(text, method, summary_size)
        elif method == "bart":
            text_chunks = self._chunk_text(text, 400)
            return " ".join(
                self._BART_summary(chunk, summary_size)
                for chunk in text_chunks
            )
        elif method == "openai":
            text_chunks = self._chunk_text(text, 500)
            return " ".join(
                self._openai_summary(chunk, summary_size)
                for chunk in text_chunks
            )
    
    def _SE_summary(self, text, summary_size=0.5):
        # Create word and sentence tokens
        words = self._word_tokenize(text)
        word_set = set(words) # set of all unique words in word tokens
        sents = nltk.sent_tokenize(text)

        # Initialise frequency table for word tokens
        w_freq_table = {w: words.count(w) for w in word_set}

        # Score sentences based on frequency of their words
        sent_scores = {
            sent: sum(
                w_freq_table.get(w, 0) 
                for w in self._word_tokenize(sent)
            )
            for sent in sents
        }

        # Build summary
        multiplier = 2 * (1 - summary_size)

        avg = sum(sent_scores.values()) / len(sent_scores)
        summary = " ".join(sent for sent in sents if sent_scores[sent] >= avg * multiplier)
        return summary
    
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
    
    def _BART_summary(self, text, summary_size=0.5):
        # Get lengths of original text and summary
        word_len = len(nltk.word_tokenize(text))
        summary_len = int((summary_size * word_len) + 0.5)

        # Get API url and headers
        api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
        headers = {
            "Authorization": f"Bearer {os.getenv('HUGGING_FACE_API_KEY')}"
        }

        payload = {
            "inputs": text,
            "parameters": {
                "do_sample": False,
#                 "max_length": max(round(summary_len + 50, -2), 2),
                "max_length": min(round(summary_len + 50, -2), word_len),
                "min_length": max(summary_len - 10, 1)
            }
        }

        data = json.dumps(payload)
        res = req.request("POST", api_url, headers=headers, data=data)
        text = json.loads(res.content.decode("utf-8"))[0]["summary_text"]
        
        return text
    
    def _openai_summary(self, text, summary_size=0.5):
        word_len = len(nltk.word_tokenize(text))
        summary_len = int((summary_size * word_len) + 0.5)

        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt=f"Summarize the following text in no more than {summary_len} words:\n\n{text}\n\nSummary:"

        res = openai.Completion.create(
            model="text-davinci-003", 
            prompt=prompt, 
            temperature=0,
            max_tokens=round(summary_len + 50, -2),
        )

        summary = res.choices[0].text
        return summary