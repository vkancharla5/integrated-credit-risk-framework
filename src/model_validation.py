import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score

def backtesting(df, y_true, y_pred, n_bins=10):
    df=df.copy()

    df['pd']=y_pred
    df['actual']=y_true

    df['decile']=pd.qcut(df['pd'], q=n_bins, duplicates='drop')

    summary=df.groupby('decile').agg(
    avg_pd=('pd', 'mean'),
    actual_rate=('actual', 'mean'),
    count=('actual','count')).reset_index()
    return summary
'''
def challenger_model(X_train, y_train, X_test, y_test):
        model=RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        preds=model.predict_proba(X_test)[:,1]
        auc=roc_auc_score(y_test, preds)
        return model, preds, auc
        '''

MODEL_REGISTRY={
    'rf':RandomForestClassifier(n_estimators=100, random_state=42),
    
    'xgb':XGBClassifier(
    use_label_encoder=False,
    eval_metric='logloss',
    random_state=42),
    
    'lgb':LGBMClassifier(n_estimators=100,random_state=42)}

def challenger_model(model_name, X_train, y_train, X_test, y_test):
    if model_name not in MODEL_REGISTRY:
        raise ValueError(f'Model {model_name} not supoorted')

    model=MODEL_REGISTRY[model_name]
    model.fit(X_train, y_train)
    preds=model.predict_proba(X_test)[:,1]
    auc=roc_auc_score(y_test, preds)

    return model, preds, auc

def sensitivity_analysis(model, X, feature, num_points=10):
    
    X=X.copy()
    features=X.columns
    
    values=np.linspace(X[feature].min(), X[feature].max(), num_points)    
    avg_pd=[]
    
    for val in values:
        X_temp=X.copy()
        X_temp[feature]=val   

        X_temp=X_temp[features]
        
        
        preds=model.predict_proba(X_temp)
        avg_pd.append(preds.mean())

    return values, avg_pd


def stress_simulation(df,model,calibrator,selected_woe_vars):

    stress_df = df.copy()
    stress_df['annual_inc_bin_woe'] *= 0.8
    stress_df['dti_bin_woe'] *= 1.2
    stress_df['inq_last_6mths_bin_woe'] *= 1.3

    
    X_stress = stress_df[selected_woe_vars]
    raw_pd = model.predict_proba(X_stress)
    calibrated_pd = calibrator.predict(raw_pd)

    return raw_pd, calibrated_pd


    
    

    
    
