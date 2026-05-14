import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression, LinearRegression
import pickle

class LGDModel:

    def __init__(self):
        self.stage1 = LogisticRegression(max_iter=1000)
        self.stage2 = LinearRegression()

    def prepare_targets(self, df):
        df = df.copy()

        # Recovery Rate
        df['recovery_rate'] = df['recoveries'] / df['funded_amnt']
        df['recovery_rate'] = np.clip(df['recovery_rate'], 0, 1)

        # Binary target
        df['recovery_rate_0_1'] = np.where(df['recovery_rate'] == 0, 0, 1)

        return df

    def train(self, X, df_targets):

        # Stage 1 (classification)
        y_stage1 = df_targets['recovery_rate_0_1']
        self.stage1.fit(X, y_stage1)

        # Stage 2 (regression)
        df_stage2 = df_targets[df_targets['recovery_rate_0_1'] == 1]
        X_stage2 = X.loc[df_stage2.index]
        y_stage2 = df_stage2['recovery_rate']

        self.stage2.fit(X_stage2, y_stage2)

    def predict(self, X):

        stage1_pred = self.stage1.predict_proba(X)[:, 1]
        stage2_pred = self.stage2.predict(X)

        lgd = stage1_pred * stage2_pred
        lgd = np.clip(lgd, 0, 1)

        return lgd

    def save(self, path_stage1, path_stage2):
        pickle.dump(self.stage1, open(path_stage1, 'wb'))
        pickle.dump(self.stage2, open(path_stage2, 'wb'))

    def load(self, path_stage1, path_stage2):
        self.stage1 = pickle.load(open(path_stage1, 'rb'))
        self.stage2 = pickle.load(open(path_stage2, 'rb'))