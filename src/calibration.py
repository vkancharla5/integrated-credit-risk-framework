import pandas as pd
import statsmodels.api as sm
import pickle

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

class PDcalibrator:
    def __init__(self):
        self.model=None

    def fit(self, y_pred, y_true):
        df=pd.DataFrame({'pd_pred': y_pred, 'target':y_true})

        X=sm.add_constant(y_pred)
        self.model=sm.Logit(df['target'],X).fit(disp=False)

    def predict(self, y_pred):
        X=sm.add_constant(y_pred)
        return self.model.predict(X)

    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self.model, f)

    def load(self, path):
        with open(path, 'rb') as f:
            self.model=pickle.load(f)

    
    