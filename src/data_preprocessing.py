#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np

import logging
logging.basicConfig(level=logging.INFO)

from src.data_validation import validate_input
from src.config import BAD_STATUS, TARGET_COL
import re


# In[6]:


class LoanDataPreprocessor:
        
    def __init__(self):
        self.version= 'v1.0'
        logging.info(f"Preprocessing version: {self.version}")
        pass

   #load data
    def load_data(self, filepath):
        df=pd.read_csv(filepath, low_memory=False)
        return df

    

    #clean employement length
    def clean_emp_length(self,df):
        logging.info("Cleaning employment length")
        df['emp_length_int']=df['emp_length'].str.replace('+ years','', regex=False)
        df['emp_length_int']=df['emp_length_int'].str.replace('< 1 year',str(0), regex=False)
        df['emp_length_int']=df['emp_length_int'].str.replace('n/a', str(0), regex=False)
        df['emp_length_int']=df['emp_length_int'].str.replace(' years','', regex=False)
        df['emp_length_int']=df['emp_length_int'].str.replace(' year','', regex=False)
        df['emp_length_int']=pd.to_numeric(df['emp_length_int'], errors='coerce')
        df['emp_length_int']=df['emp_length_int'].fillna(0)
        return df

    #clean loan term
    def clean_term_int(self,df):
        logging.info("Cleaning term")
        df['term_int']=df['term'].str.replace(' months','', regex=False)
        df['term_int']=pd.to_numeric(df['term_int'])
        return df

    
    #clean earliest_cr_line
    def convert_dates(self, df):
        logging.info("dates conversion")
        df['earliest_cr_line_date']=pd.to_datetime(df['earliest_cr_line'],format='%b-%y',errors='coerce')
        mask=df['earliest_cr_line_date'].dt.year>pd.Timestamp.today().year
        df.loc[mask,'earliest_cr_line_date']-=pd.DateOffset(years=100)

        df['issue_d']=pd.to_datetime(df['issue_d'],format='%b-%y',errors='coerce')
        missing_mask=df['earliest_cr_line_date'].isnull()
        if missing_mask.any():
            
            logging.warning(f'{missing_mask.sum()} missing earliest_cr_line_date fill with issue_d')
            df.loc[missing_mask, 'earliest_cr_line_date']=df.loc[missing_mask, 'issue_d']
        return df

    #create credit age 
    def create_credit_age(self, df):
        logging.info("credit age creation")
        df['credit_age_months']=((df['issue_d']- df['earliest_cr_line_date']).dt.days //30)        
        invalid_rows=df['issue_d']<df['earliest_cr_line_date']
        if invalid_rows.any():
            logging.warning(f'{invalid_rows.sum()} records have invalid credit dates')
            df['invalid_credit_age_flag']=invalid_row.astype(int)
            df.loc[invalid_rows,'credit_age_months']=0        
        return df

    #Handling missing values

    def handle_missing_values(self,df):
        logging.info("missing values handling")
        missing_value_rules={
            'total_rev_hi_lim':'funded_amnt',
            'annual_inc':'mean'
        }

        for col,rule in missing_value_rules.items():
            if rule=='mean':
                df[col]=df[col].fillna(df[col].mean())
            else:
                df[col]=df[col].fillna(df[rule])

        for col in df.columns:
            if df[col].dtype=='datetime64[ns]':
                continue
            df[col]=df[col].fillna(0)
        return df

        
    def cap_outliers(self, df, col):
        if df[col].nunique()>2:
            return df
            
        logging.info(f"Outlier capping applied on : {col}")
        upper = df[col].quantile(0.99)
        lower = df[col].quantile(0.01)
        
        df[col] = np.where(df[col] > upper, upper, df[col])
        df[col] = np.where(df[col] < lower, lower, df[col])
        return df
       
    def create_target_variable(self,df):
        logging.info("target variable creation")
        df['loan_status_clean'] = df['loan_status'].str.strip()

        pattern = '|'.join(map(re.escape, BAD_STATUS))
        
        df[TARGET_COL] = np.where(
        df['loan_status_clean'].str.contains(pattern,case=False,regex=True),1,0)   
        return df 
      

    #final pipeline    
    def preprocess(self, filepath):  
        try:
            df=self.load_data(filepath)
        except Exception as e:
            logging.error(f'Error loading data : {e}')
            raise

        if df.shape[0]==0:
            raise ValueError('Dataset is empty')

        required_cols = ['emp_length','term','loan_status','earliest_cr_line','issue_d']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")  
            
        validate_input(df)
        df=self.clean_emp_length(df)
        df=self.clean_term_int(df)
        df=self.convert_dates(df)
        df=self.create_credit_age(df)        
        df=self.handle_missing_values(df)
        df=self.create_target_variable(df)

        exclude_cols=['id', 'member_id',TARGET_COL]
        numeric_cols=df.select_dtypes(include=np.number).columns
        numeric_cols=[col for col in numeric_cols if col not in exclude_cols and df[col].nunique()>10]       
        logging.info(f"Applying outlier capping on {len(numeric_cols)} columns")       
        for col in numeric_cols:
            df=self.cap_outliers(df, col)            
        
        logging.info(f'final dataset shape: {df.shape}')
        #feature metadata maintained in artifacts/feature_metadata.csv
        
        return df

    def validate_target(self,df, target_col='good_bad'):
        print("\n===== TARGET VALIDATION =====")

        # Show configured bad statuses
        print("\nConfigured BAD_STATUS values:")
        for status in BAD_STATUS:
            print(f" - {status}")

        total_bad = df[target_col].sum()
        comp = df[df[target_col] == 1]['loan_status'].value_counts()
        print("\nComponent Breakdown:\n", comp)
        print("\nTotal Bad Count:", total_bad)
        print("Sum of Components:", comp.sum())

        if total_bad == comp.sum():
            print("\n✅ VALIDATION PASSED")
        else:
            print("\n❌ VALIDATION FAILED")
        
             

        

        
        
    
    
    

    
    



    

    
        

