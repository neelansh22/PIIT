import spacy
import pycountry
import pandas as pd
import re
import numpy as np
from langdetect import detect, lang_detect_exception
import warnings
warnings.filterwarnings("ignore")


# Redacting Natual Human names as discovered in the text block
def redact_personal_info(text, lang_code):
    name_list = []
    # Process the text with spaCy
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
    model = nlp
    doc = model(text)
    # Iterate over the entities in the document
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            # Extracting all names out of the text block
            name_list.append(ent.text)
            # Replace the person name with asterisks
            text = text.replace(ent.text, "****")
    
    # Replace the name in the email ID with asterisks
    email_parts = text.split("@")
    if len(email_parts) == 2:
        name_parts = email_parts[0].split(".")
        if len(name_parts) > 1:
            name_parts[-1] = "****"
            email_parts[0] = ".".join(name_parts)
            text = "@".join(email_parts)
    return text, name_list

# Rolling the redaction logic over a given dataset
def rpi_caller(data):
    rl = []
    nl = []
    eml = []
    for index, r in data.iterrows(): #for i in data['Text']:
        text = r['Text']
        country_code = r['LangCode']
        redacted_text, n = redact_personal_info(text, country_code) #, name_list, email_list
        rl.append(redacted_text)
        nl.append(n)
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        emails = re.findall(pattern, text)
        eml.append(emails)
    data['Redacted_Text'] = rl
    data['Name'] = nl
    data['Name'] = data['Name'].apply(lambda x: np.nan if x == [] else x)
    data['Emails'] = eml
    data['Emails'] = data['Emails'].apply(lambda x: np.nan if x == [] else x)
    return data
