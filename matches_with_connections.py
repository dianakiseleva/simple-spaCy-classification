import pandas as pd


# loading dictionaries
with open("food_refactored.txt", encoding="utf8") as f:
    FOOD = f.read()
FOOD=FOOD.split('\n')


with open("bac_refactored.txt", encoding="utf8") as f:
    BACTERIA = f.read()
BACTERIA=BACTERIA.split('\n')

with open("negative_verbs.txt", encoding="utf8") as f:
    NV = f.read()
NV=NV.split('\n')


with open("positive_verbs.txt", encoding="utf8") as f:
    PV = f.read()
PV=PV.split('\n')


with open("include_object.txt", encoding="utf8") as f:
    INCLUDE = f.read()
INCLUDE=INCLUDE.split('\n')


with open("exclude_object.txt", encoding="utf8") as f:
    EXCLUDE = f.read()
EXCLUDE=EXCLUDE.split('\n')


# defining functions


#Function to mark potential connections
def process_match(data):
    
    match = data[0].lower()
    food = data[1]
    bacteria = data[2]
    
    is_food = match in FOOD
    is_bacteria = match in BACTERIA
    
    if ((len(food) + int(is_food))>=1) & ((len(bacteria) + int(is_bacteria))>=1):
        return 1
    else:
        return 0


#Function to mark the tone of an association
def process_verbs(data):
    verb = data[0]
    connection = data[1]
    is_positive = len(set(verb) & set(PV)) > 0
    is_negative = len(set(verb) & set(NV)) > 0
    if connection==1:
        if (is_positive==True) & (is_negative==True):
            return 'manual_check'
        elif is_positive==True:
            return 'positive'
        elif is_negative==True:
            return 'negative'
        else:
            return 'manual_check'
    elif connection==0:
        return 'no_connection'



#Function to mark the object of study
def object_type(data):
    
    incl_ob = data[0]
    excl_ob = data[1]
    
    is_excluded = len(set(excl_ob) & set(EXCLUDE)) > 0
    is_included = len(set(incl_ob) & set(INCLUDE)) > 0
    
    if (is_excluded==True) & (is_included==True):
        return 'manual_check'
    elif is_included==True:
        return 'included_object_type'
    elif is_excluded==True:
        return 'excluded_object_type'
    else:
        return 'manual_check'


# applying functions



results_bac_9k = pd.read_csv('results_bigtext_005dir_9kplus.csv', index_col=0)



results_bac_9k['Verbs_in_span']=results_bac_9k['Verbs_in_span'].apply(eval)
results_bac_9k['Food_in_span']=results_bac_9k['Food_in_span'].apply(eval)
results_bac_9k['Bac_in_span']=results_bac_9k['Bac_in_span'].apply(eval)


results_bac_9k['Connection'] = results_bac_9k[['Match', 'Food_in_span', 'Bac_in_span']].apply(process_match, axis=1)


results_bac_9k['Tone']=results_bac_9k[['Verbs_in_span','Connection']].apply(process_verbs, axis=1)


df1 = results_bac_9k[results_bac_9k.Connection==1]['PMC'].value_counts().rename_axis('unique_values').reset_index(name='counts')


list_of_pmc = df1.unique_values.to_list()


import pickle
with open("list_of_pmc9k.txt", "wb") as fp:   #Pickling
    pickle.dump(list_of_pmc, fp)


abstract_9k= pd.read_csv('abstracts_9k.csv', index_col=0)



abstract_9k['Excluded_object_in_abstract']=abstract_9k['Excluded_object_in_abstract'].apply(eval)
abstract_9k['Included_object_in_abstract']=abstract_9k['Included_object_in_abstract'].apply(eval)



abstract_9k['PMC'] = abstract_9k['PMC'].astype('int64')


results_bac_9k = results_bac_9k.merge(abstract_9k,how='inner',on='PMC')



results_bac_9k['Object_of_study']=results_bac_9k[['Included_object_in_abstract','Excluded_object_in_abstract']].apply(object_type, axis=1)


results_bac_9k[results_bac_9k['Connection']==1].to_csv('all_potential_matches.csv')


