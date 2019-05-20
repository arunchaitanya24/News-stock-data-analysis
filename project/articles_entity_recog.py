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
def filterData(tups):
    org_ent_data = list(filter(lambda tup: "ORG" in tup, tups))
    entities = []
    for ent in org_ent_data:
        entities.append(ent[0])
    return entities


# # Importing Csv to check data attributes
# df = pd.read_csv('sample.csv')
# # Display first 5 rows of your data
# df.head()

# Fetches articles from `.csv` and returns an `order dictionary list`
def get_articles():
    with open('Articles.csv', newline='') as csvfile:
        articlesData = csv.DictReader(csvfile)
        articlesList = []
        for article in articlesData:
            articlesList.append(article)
    return articlesList


def getEntityIdentifiedArticles():
    # Get articles list
    articles = get_articles()

    # An array of entity recognised articles.
    entityNamedArticles = []
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
        org_flt_data = filterData(label_ner_data)

        # Checks if array of entity is empty
        if org_flt_data:
            article["ents"] = ",".join(org_flt_data)
            entityNamedArticles.append(article)

    return entityNamedArticles


# Main

entityListed_Articles = getEntityIdentifiedArticles()
# Get Keys to est header to csv
keys = entityListed_Articles[0].keys()
# Create a new csv with entity list
with open('Articles_ent.csv', 'w+') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(entityListed_Articles)

