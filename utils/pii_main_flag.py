import spacy
import pandas as pd
import re
import numpy as np
from langdetect import detect, lang_detect_exception
import warnings
warnings.filterwarnings("ignore")

def detect_pii_flag(data):
    # Load the appropriate Spacy language model based on the language code
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
            
    person_list = []
    spacy_person_entities = [ent for ent in doc.ents if ent.label_ in ['PERSON','DATE', 'EMAIL', 'PHONE', 'ADDRESS']]
    if len(spacy_person_entities) == 0:
        person_list.append(np.nan)
    else:
        person_list.append(spacy_person_entities if spacy_person_entities else np.nan)
    
    regex_list = []
    regex_pattern = r"(?:Ms\.|Miss|Mrs\.|Mr\.|c/o\.|Mister|Doctor|Doc\.|Dr\.|M\.|Monsieur|Madame|Mademoiselle|Herr|Hr\.|Sir|Frau| Fr\.|Meneer|Mevrouw| Mevr\.|Signore|Sig\.|Signora|Sig\.ra|Sig\.na|Senyor|Sr\.|Sernyora|Sra\.|Senyoreta|Srta\.|Señor|Señora|Señorita|Srta\.)\s+[A-Z][a-z]+\b"
    regex_match = re.findall(regex_pattern, text)
    regex_list.append(regex_match if regex_match else np.nan)
    
    data['SpacyEntities'] = person_list
    data['RegexMatches'] = regex_list

    if pd.isnull(data['SpacyEntities'].values) and pd.isnull(data['RegexMatches'].values):
        result = 0
    else:
        result = 1

    data['PII_Flag'] = result
    return data

