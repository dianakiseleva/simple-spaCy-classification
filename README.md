# simple-spaCy-classification
## Model description
#### The model is designed to parse scientific articles and to search for associations between food intake and intestinal bacteria modulation, as well as the direction of such modulation (i.e. increase or decrease). This is a two-step text classificator for imbalanced classes. The texts are classified by key topics and potential connections are predicted.  The data for the classificator is collected using dictionnary-based approach with spaCy English medium size model.
## Reqirements
#### Clone repo and install requirements.txt in a Python>=3.6.0 environment
#### `pip install -r requirements.txt`
## Files description
#### The project contains:
#### 1) four main Python scripts. The `matching_procedure.py` aplies spaCy model for matching bateria and food lists, as well as collects all necessary information from a span. In order to filter potential within a stipulated span and form a list of texts for classificator we run `matches_with_connections.py`. The collection of article abstracts for clustarization and full texts for classification is performed by running `collection_of_abstracts.py`, `collection_of_full_texts.py`   
#### 2) Jupyter notebook for visualisation. 
#### 3) Dictionnaries that are used by spaCy to perform matching (food and bacteria lists, included and excluded objects of study, positive and negative verbs to assign the direction of bacteria modulation after certain food intake).
#### 4) Additional files for model performance as the randomly collected text corpora from PMC Open Access Subset and a training dataset. The texts that were collected are available for texts mining under Creative Commons or similar licenses. 
## Run model
#### Type the following command in your CLI. The scripts will run in the correct order.
#### `bash run_scripts.sh`
#### When all files are generated, run the Jupyter notebook for data visualization and classification.
