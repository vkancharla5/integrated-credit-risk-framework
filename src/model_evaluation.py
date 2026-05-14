import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve, confusion_matrix

class ModelEvaluation:
    def __init__(self):
        pass

    def auc(self, y_true,y_pred):
        return roc_auc_score(y_true, y_pred)

    def gini(self, y_true, y_pred):
        auc=roc_auc_score(y_true, y_pred)
        return 2*auc-1

    def roc_curve_data(self, y_true, y_pred):
        fpr, tpr, thresholds=roc_curve(y_true, y_pred)
        return fpr, tpr, thresholds

    def confusion_matrix(self, y_true, y_pred, threshold=0.5):
        y_class=(y_pred>=threshold).astype(int)
        return confusion_matrix(y_true, y_class)

    def ks_table(self, y_true, y_pred):
        df=pd.DataFrame({'y_true':y_true, 'y_pred':y_pred})
        df=df.sort_values(by='y_pred', ascending=False)
        df['cum_bad']=df['y_true'].cumsum()/df['y_true'].sum()
        df['cum_good']=((1-df['y_true']).cumsum())/(1-df['y_true']).sum()
        df['diff']=abs(df['cum_bad']-df['cum_good'])        
        return df

    
    def ks(self,y_true, y_pred):
        df=self.ks_table(y_true, y_pred)
        return df['diff'].max()

    def individual_pd(self, y_pred):
        return pd.DataFrame({'PD':y_pred})
        
        
        
        