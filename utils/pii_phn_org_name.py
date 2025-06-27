import spacy
import pycountry
import pandas as pd
import re
import numpy as np
from langdetect import detect, lang_detect_exception
import warnings
warnings.filterwarnings("ignore")


def extract_phone_numbers(data):
    pattern_phone = r'\b\d{7,10}\b'
    pattern_house =  r'\b([1-9][0-9]{0,3})\b' #r"\b\d{1,4}(?=\s*,)" 
    phone_numbers = []
    house_numbers = []
    for text in data['Text']:
        matches = re.findall(pattern_phone, text)
        phone_numbers.append(matches if matches else None)
        matches1 = re.findall(pattern_house, text)
        house_numbers.append(matches1 if matches1 else None)

    data['PhoneNumber'] = phone_numbers
    data['PhoneNumber'] = data['PhoneNumber'].apply(lambda x: np.nan if x == [] else x)
    data['HouseNumber'] = house_numbers
    data['HouseNumber'] = data['HouseNumber'].apply(lambda x: np.nan if x == [] else x)

    return data


def extract_organization_names(data):
    for text in data['Text']:
        for lang_code in data['LangCode']:
            nlp = spacy.load("en_core_web_lg")
            doc = nlp(text)
            organization_names = []
            spacy_org_entities = [ent for ent in doc.ents if ent.label_ == "ORG"]
            if len(spacy_org_entities) == 0:
                organization_names.append(np.nan)
            else:
                organization_names.append(spacy_org_entities if spacy_org_entities else np.nan)
    data['OrgName'] = organization_names
    return data

