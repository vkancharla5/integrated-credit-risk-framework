import logging
logging.basicConfig(level=logging.INFO)

from src.config import purpose_grp_dict
from src.config import addr_state_grp_dict
from src.config import home_ownership_grp_dict

feature_engineering_version='v1.0'


    
def apply_feature_engineering(df, woe):
    logging.info("Starting feature engineering")

    required_cols = ['home_ownership','purpose','addr_state']
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in feature engineering: {missing}")

    
    logging.info("Applying categorical grouping")
       
    df = df.copy()

    # Grouping
    df['home_ownership_grp'] =df['home_ownership'].replace(home_ownership_grp_dict).fillna('other')
    df['purpose_grp'] = df['purpose'].replace(purpose_grp_dict).fillna('other')
    df['addr_state_grp'] = df['addr_state'].map(addr_state_grp_dict).fillna('other')

    #  Missing flags
    if 'mths_since_last_delinq' in df.columns:
        df['mths_since_last_delinq_missing'] = df['mths_since_last_delinq'].isnull().astype(int)

    if 'mths_since_last_record' in df.columns:    
        df['mths_since_last_record_missing'] = df['mths_since_last_record'].isnull().astype(int)
    '''    
    # Apply bins
    logging.info("Applying WoE binning")
    if woe is None:
        raise ValueError('WoE object not provided')
    df = woe.apply_bins(df)
    '''

    #  Drop unwanted
    #df = df.drop(columns=['total_acc_bin'], errors='ignore')
    #Feature definitions maintained in artifacts/feature_metadata.csv
    feature_cols=df.columns.tolist()
    logging.info(f"Feature engineering completed. Shape: {df.shape}")
    logging.info(f"Feature engineering version: {feature_engineering_version}")
    return df, feature_cols

 