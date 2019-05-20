# Imports

import csv
import spacy
import pandas as pd
import en_core_web_sm
from spacy import displacy
from collections import Counter


# Performing name entity recognition (NER)
def perform_ner(data):
    nlp = en_core_web_sm.load()
    doc = nlp(data)
    label_data = [(X.text, X.label_) for X in doc.ents]
    return label_data


# Filtering out organisation from entities
def filter_entities_data(tups):
    org_ent_data = list(filter(lambda tup: "ORG" in tup, tups))
    entities = []
    for ent in org_ent_data:
        entities.append(ent[0])
    return entities


# Fetches articles from `.csv` and returns an `order dictionary list`
def get_articles():
    with open('sample.csv', newline='') as csvfile:
        articles_data = csv.DictReader(csvfile)
        articles_list = []
        for article in articles_data:
            articles_list.append(article)
    return articles_list


def perform_ner_articles():
    # Get articles list
    articles = get_articles()

    # An array of entity recognised articles.
    entity_articles = []
    i = 0
    # Looping articles for NER
    for article in articles:
        i = i + 1
        print(i)
        # Get summary from article
        summary = article["summary"]

        # Perform NER
        label_ner_data = perform_ner(summary)

        # Filter Organization labeled data
        org_flt_data = filter_entities_data(label_ner_data)

        # Checks if array of entity is empty
        if org_flt_data:
            article["ents"] = ",".join(org_flt_data)
            entity_articles.append(article)

    return entity_articles


# Main

entity_named_articles = perform_ner_articles()
# Get Keys to est header to csv
keys = entity_named_articles[0].keys()
# Create a new csv with entity list
with open('sample_articles_ent.csv', 'w+') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(entity_named_articles)
    print('Success')

