import spacy
import pycountry
import pandas as pd
import re
import numpy as np
from langdetect import detect, lang_detect_exception
import warnings
warnings.filterwarnings("ignore")


def address_flag(data):
    for text in data['Text']:
        for lang_code in data['LangCode']:
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
            doc = nlp(text)
            city_state = []
            location_entities = [ent for ent in doc.ents if ent.label_ == "GPE" or ent.label_ == "LOC"]
            city_state.append(location_entities)
            if len(city_state) == 0:
                city_state.append(np.nan)
            else:
                city_state.append(location_entities if location_entities else np.nan)  
    data['SpacyLocationEntities'] = [city_state]
    
    def detect_address(text, language_code):
        regex_locn_list = []
        
        if language_code == "EN":
            regex_pattern = r"\b\d{2}(?:,\s?\d{1,4})?\s+\w+\b"
        elif language_code == "FR":
            regex_pattern = r"\b\d{1,5}\s[A-Za-zéèàêûïëüôæœç\s]+\b,\s\d{5}\s[A-Za-zéèàêûïëüôæœç\s'-]+\b"
        elif language_code == "DE":
            regex_pattern = r"\b\d{1,5}\s[A-Za-zäöüÄÖÜß\s]+\b,\s\d{5}\s[A-Za-zäöüÄÖÜß\s]+\b"
        elif language_code == "IT":
            regex_pattern = r"\b\d{1,5}\s[A-Za-z\s]+\b,\s\d{5}\s[A-Za-z\s]+\b"
        elif language_code == "NL":
            regex_pattern = r"\b\d{1,5}\s[A-Za-z\s]+\b,\s\d{4}\s[A-Za-z\s]+\b"
        elif language_code == "PT":
            regex_pattern = r"\b\d{2}(?:,\s?\d{1,4})?\s+\w+\b"
        elif language_code == "CA":
            regex_pattern =  r"\b\d{2}(?:,\s?\d{1,4})?\s+\w+\b"
        else:
            return False

        address_match = re.findall(regex_pattern, text)
        regex_locn_list.append(address_match if address_match else np.nan)

        return regex_locn_list
    
    for index, row in data.iterrows():
        text = row['Text']
        lang_code = row['LangCode']
    
    data['RegexLocationEntities'] = detect_address(text, lang_code)
    
    if pd.isnull(data['RegexLocationEntities'].values) and pd.isnull(data['SpacyLocationEntities'].values):
        result = "NoAddressFound"
    else:
        result = 1

    data['AddressFlag'] = "AddressFound"
    
    return data