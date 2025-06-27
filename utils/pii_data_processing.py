import spacy
import pycountry
import pandas as pd
import re
import numpy as np
from langdetect import detect, lang_detect_exception
import warnings
warnings.filterwarnings("ignore")

def data_processing(text):
    data = pd.DataFrame({'Text': [text]})
    for text in data['Text']:    
        try:
            lang = detect(text)
        except lang_detect_exception.LangDetectException:
            lang = 'EN'  # Replace unknown or NaN language with 'EN' (English)
        data['LangCode'] = lang
        data['LangCode'] = data['LangCode'].str.upper()
        
    return data

