import statsmodels.api as sm
from sklearn.metrics import roc_auc_score

import logging
logging.basicConfig(level=logging.INFO)

from scipy.stats import ks_2samp

class PDModel:
    def __init__(self):
        self.model=None
        self.features=None

    def fit(self, X,y):
        logging.info(f'Training data shape : {X.shape}')
        logging.info("Training PD logistic regression model")

        if X.isnull().sum().sum()>0:
            raise ValueError ('Missing values in training data')

        if not all([str(dtype).startswith(('float','int'))for dtype in X.dtypes]):
            raise ValueError('Non-numeric features detected')
            
        X=sm.add_constant(X, has_constant='add')

        try:
            self.model=sm.Logit(y, X).fit(disp=False)
        except Exception as e:
            logging.error(f'model training failed : {e}')
            raise

        if not self.model.mle_retvals['converged']:
            raise ValueError("Model did not converge")
        
        self.features=X.columns.tolist()

    def predict_proba(self, X):
        logging.info("Generating predictions")
        X=X.copy()
        feature_cols=[col for col in self.features if col !='const']

        missing_cols=set(feature_cols)-set(X.columns)
        if missing_cols:
            raise ValueError(f'Missing columns in input: {missing_cols}')
        
        X=X.reindex(columns=feature_cols, fill_value=0)      
        X=sm.add_constant(X, has_constant='add')        
            
        #X=X[self.features]
        logging.info(f'scoring data shape : {X.shape}')
        return self.model.predict(X)

    def get_coefficients(self):
        return self.model.params

    def evaluate_auc(self, y_true, y_pred):
        return roc_auc_score(y_true, y_pred)

    def evaluate_ks(self, y_true, y_pred):
        return ks_2samp(y_pred[y_true==1],y_pred[y_true==0]).statistic

    def summary(self):
        return self.model.summary()
        