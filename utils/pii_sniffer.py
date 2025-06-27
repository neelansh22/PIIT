import pandas as pd
import utils.pii_data_processing as pii_dp
import utils.pii_score as pii_score
import utils.pii_address_flag as pii_address
import utils.pii_phn_org_name as pii_phn_org
import utils.pii_redact as pii_redact
import utils.pii_main_flag as pii_main_flag
import warnings
warnings.filterwarnings("ignore")


class pii_sniffer:
    def __init__(self, test_string): #multilingual
        
        #self.multilingual = multilingual
        
        self.data = pd.DataFrame({'Text': [test_string]})
    

    def data_processing(self):
        self.data = pii_dp.data_processing(self.data['Text'].iloc[0])
    
    def address_flag(self):
        self.data = pii_address.address_flag(self.data)
    
    def pii_scorer_call(self):
        #self.data = pii_score.pii_scorer_call(self.data['Text'].iloc[0])
        self.data = pii_score.pii_scorer_call(self.data)
    
    def rpi_caller(self):
        self.data = pii_redact.rpi_caller(self.data)
    
    def extract_phone_numbers(self):
        self.data = pii_phn_org.extract_phone_numbers(self.data)
    
    def extract_organization_names(self):
        self.data = pii_phn_org.extract_organization_names(self.data)
    
    def detect_pii_flag(self):
        self.data = pii_main_flag.detect_pii_flag(self.data)

