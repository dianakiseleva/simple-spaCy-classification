import joblib
import json
import numpy as np

import pandas as pd
import spacy
nlp = spacy.load("en_core_web_md", disable="ner")
nlp.max_length = 1500000



with open("PMC_005_bigtext_9k.txt", encoding="latin-1") as f:
    TEXT = f.read()


TEXT=TEXT.split('["PMC')
TEXT = [x.replace('\\n',' ') for x in TEXT]
TEXT = [x.replace('.txt',' ') for x in TEXT]
start = [x.find('article distributed under the terms') for x in TEXT]
end = [x.find('==== Body') for x in TEXT]

for i in range(1,len(TEXT)):
    TEXT[i]=TEXT[i][start[i]:end[i]:]

TEXT=TEXT[1:]
docs = nlp.pipe(TEXT, batch_size=100)

from spacy.tokens import Token

with open("exclude_object.txt", encoding="utf8") as f:
    EXCL = f.read()
EXCL=EXCL.split('\n')

with open("include_object.txt", encoding="utf8") as f:
    INCL = f.read()
INCL= INCL.split('\n')


is_EXCL = lambda token: token.text in EXCL
Token.set_extension("is_excluded", getter=is_EXCL)

is_INCL = lambda token: token.text in INCL
Token.set_extension("is_included", getter=is_INCL)

table = []
for doc in list(docs):
    new_text = doc.text
    table.append([new_text,
            [token.lemma_ for token in doc if token._.is_excluded],
            [token.lemma_ for token in doc if token._.is_included],
            new_text[0:7]])


table1 = pd.DataFrame(table, columns = ['Abstract','Excluded_object_in_abstract','Included_object_in_abstract', 'PMC'])
table1.to_csv('abstracts_9k.csv')