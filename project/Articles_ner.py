# Imports

import os
import csv
import spacy
import pandas as pd
import en_core_web_sm
from spacy import displacy
from collections import Counter


# Performing name entity recognisation (NER) using spacy
def performNER(data):
    nlp = en_core_web_sm.load()
    doc = nlp(data)
    labelData = [(X.text, X.label_) for X in doc.ents]
    return labelData


# Filtering out organisation from entites
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

# Fetchs articles from `.csv` and returns an `order dictonary list`
def getArticles():
    with open('Articles.csv', newline='') as csvfile:
        articlesData = csv.DictReader(csvfile)
        articlesList = []
        for article in articlesData:
            articlesList.append(article)
    return articlesList


def getEntityIdentifiedArticles():
    # Get articles list
    articles = getArticles()

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
        labledNERData = performNER(summary)

        # Filter Organization labled data
        org_flt_data = filterData(labledNERData)

        # Checks if array of entites is empty
        if org_flt_data:
            article["ents"] = ",".join(org_flt_data)
            entityNamedArticles.append(article)

    return entityNamedArticles


# Main

entityListed_Articles = getEntityIdentifiedArticles()
# Get Keys to est hearder to csv
keys = entityListed_Articles[0].keys()
# Create a new csv with entity list
with open('Articles_ent.csv', 'w+') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(entityListed_Articles)

