import joblib
import json
import numpy as np
import pandas as pd
import pickle




with open("PMC_005_bigtext_9k.txt", encoding="latin-1") as f:
    TEXT = f.read()


TEXT=TEXT.split('["PMC')
TEXT = [x.replace('\\n',' ') for x in TEXT]
#TEXT = [x.replace('\\u',' ') for x in TEXT]
start = [x.find('==== Refs') for x in TEXT]


for i in range(1,len(TEXT)):
    TEXT[i]=TEXT[i][0: start[i]:]

TEXT = TEXT[1:]

with open("list_of_pmc9k.txt", "rb") as fp:
    b = pickle.load(fp)

tablef = []
for i in range(0, len(b)):
    start = [x.find(str(b[i])+'.txt') for x in TEXT]
    indices = [i for i, x in enumerate(start) if not x == -1]
    tablef.append(indices)

tablef = [int(str(x).replace(']','').replace('[','')) for x in tablef]


TEXT = [TEXT[i] for i in tablef]


table = []
text in range(0,len(TEXT)):
    table.append([TEXT[text], TEXT[text][0:7]])



table1 = pd.DataFrame(table, columns = ['Full_text', 'PMC'])
table1.to_csv('005_dir_9k_texts.csv')