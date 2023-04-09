#!/bin/bash
gunicorn app:server --timeout 60 --keep-alive 5
python -m spacy download en_core_web_lg
python -m spacy download en_core_web_sm