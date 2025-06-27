import spacy
import pycountry
import pandas as pd
import re
import numpy as np
from langdetect import detect, lang_detect_exception
import warnings
warnings.filterwarnings("ignore")


def calculate_pii_score(text, lang_code):

    if lang_code == 'EN':
        nlp = spacy.load('en_core_web_lg')
    elif lang_code == 'FR':
        nlp = spacy.load('fr_core_news_lg')
    elif lang_code == 'DE':
        nlp = spacy.load('de_core_news_lg')
    elif lang_code == 'IT':
        nlp = spacy.load('it_core_news_lg')
    elif lang_code == 'JA':
        nlp = spacy.load('ja_core_news_sm')
    elif lang_code == 'CA':
        nlp = spacy.load('ca_core_news_sm')
    elif lang_code == 'NL':
        nlp = spacy.load('nl_core_news_sm')
    elif lang_code == 'PT':
        nlp = spacy.load('pt_core_news_sm')
    elif lang_code == 'RO':
        nlp = spacy.load('ro_core_news_sm')
    elif lang_code == 'ES':
        nlp = spacy.load('es_core_news_sm')   
    else:
        nlp = spacy.load('en_core_web_lg')
    nlp_model = nlp
    doc = nlp_model(text)
    pii_entities = [ent for ent in doc.ents if ent.label_ in ['PERSON', 'NORP', 'ORG', 'GPE', 'DATE', 'EMAIL', 'PHONE', 'ADDRESS']]
    scores = len(pii_entities)
    return scores, pii_entities

def pii_scorer_call(data):
    sl = []
    pii_l = []
    for index, row in data.iterrows():
        text = row['Text']
        country_code = row['LangCode']
        score, pii_entities_list = calculate_pii_score(text, country_code)
        sl.append(score)
        pii_l.append(pii_entities_list)
    data['PII_Score'] = sl
    data['PII_Entities'] = pii_l
    data['PII_Entities'] = data['PII_Entities'].apply(lambda x: np.nan if x == [] else x)
    return data
