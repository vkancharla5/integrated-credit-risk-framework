import numpy as np
from sklearn.linear_model import LinearRegression
import pickle


class EADModel:

    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, df):

        df = df.copy()

        # CCF calculation
        df['CCF'] = (df['funded_amnt'] - df['total_rec_prncp']) / df['funded_amnt']
        df['CCF'] = np.clip(df['CCF'], 0, 1)

        y = df['CCF']
        self.model.fit(X, y)

    def predict(self, X, funded_amount):

        ccf_pred = self.model.predict(X)
        ccf_pred = np.clip(ccf_pred, 0, 1)

        ead = ccf_pred * funded_amount
        return ead

    def save(self, path):
        pickle.dump(self.model, open(path, 'wb'))

    def load(self, path):
        self.model = pickle.load(open(path, 'rb'))