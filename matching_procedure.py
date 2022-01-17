import joblib
import json
import numpy as np
import pandas as pd
import spacy

nlp = spacy.load("en_core_web_md", disable="ner")
nlp.max_length = 1500000


from spacy.matcher import PhraseMatcher


with open("PMC_005_bigtext_9k.txt", encoding="latin-1") as f:
    TEXT = f.read()


TEXT=TEXT.split('["PMC')
TEXT = [x.replace('\\n',' ') for x in TEXT]
TEXT = [x.replace('\\u',' ') for x in TEXT]
start = [x.find('==== Refs') for x in TEXT]
start1 = [x.find('//t') for x in TEXT]
end1 = [x.rfind('//t') for x in TEXT]

for i in range(1,len(TEXT)):
    TEXT[i]=TEXT[i][0:start[i]:]

for i in range(1,len(TEXT)):
    TEXT[i]=TEXT[i][0: start1[i]:] + TEXT[i][end1[i]::]

TEXT = TEXT[1:]
docs = nlp.pipe(TEXT, batch_size=100)


with open("food_refactored.txt", encoding="utf8") as f:
    FOOD = f.read()
FOOD=FOOD.split('\n')


with open("bac_refactored.txt", encoding="utf8") as f:
    BACTERIA = f.read()
BACTERIA=BACTERIA.split('\n')


from spacy.tokens import Token
is_FOOD = lambda token: token.text.lower() in FOOD
Token.set_extension("is_food", getter=is_FOOD)

with open("exclude_object.txt", encoding="utf8") as f:
    EXCL = f.read()
EXCL=EXCL.split('\n')

with open("include_object.txt", encoding="utf8") as f:
    INCL = f.read()
INCL= INCL.split('\n')


is_BACTERIA = lambda token: token.text.lower() in BACTERIA
Token.set_extension("is_bacteria", getter=is_BACTERIA)


is_EXCL = lambda token: token.text in EXCL
Token.set_extension("is_excluded", getter=is_EXCL)

is_INCL = lambda token: token.text in INCL
Token.set_extension("is_included", getter=is_INCL)

table = []
for doc in list(docs):
    matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

    patterns = list(nlp.pipe(BACTERIA))
    matcher.add("BACTERIA", None, *patterns)
    #patterns1 = list(nlp.pipe(FOOD))
    #matcher.add("FOOD", None, *patterns1)
    matches = matcher(doc)


    for token in matches:
        word = doc[token[1]]
        span = doc[token[1]-54:token[1]+54]
        span1 = doc[token[1]-27:token[1]+27]
        new_text = doc.text
   
        table.append([word.text, token[1], word.head.text,
                [child for child in word.children],
                [token.lemma_ for token in span1 if token.pos_ == "VERB"],
                [token.lemma_ for token in span if token._.is_food],
                [token.lemma_ for token in span if token._.is_bacteria],
                [token.lemma_ for token in span if token._.is_excluded],
                [token.lemma_ for token in span if token._.is_included],
                new_text[0:7]])


table1 = pd.DataFrame(table, columns = ['Match', 'Place_in_doc','Token_head','Token_children', 'Verbs_in_span', 'Food_in_span','Bac_in_span','Excluded_object_in_span','Included_object_in_span', 'PMC'])
table1.to_csv('results_bigtext_005dir_9kplus.csv')