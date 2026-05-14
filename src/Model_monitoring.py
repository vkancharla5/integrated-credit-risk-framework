import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

class ModelMonitor:

    def __init__(self, dev_df, oot_df, feature_cols):
        self.dev_df=dev_df
        self.oot_df=oot_df
        self.feature_cols=feature_cols

        #governance
        self.version='v1.0'
        self.monitoring_date=pd.Timestamp.today()

        
    def calculate_psi(self,expected, actual, bins=10):

    # CASE 1: DISCRETE / LOW UNIQUE
        if expected.dtype == 'object' or expected.nunique() < bins:

            all_vals = sorted(set(expected.unique()).union(set(actual.unique())))

            expected_dist = expected.value_counts(normalize=True).reindex(all_vals, fill_value=0)
            actual_dist   = actual.value_counts(normalize=True).reindex(all_vals, fill_value=0)

            psi_df = pd.DataFrame({
                'expected': expected_dist,
                'actual': actual_dist
            })

        else:
        # CASE 2: CONTINUOUS
            expected_bins = pd.qcut(expected, q=bins, duplicates='drop')
            actual_bins = pd.cut(actual, bins=expected_bins.cat.categories)

            expected_dist = expected_bins.value_counts(normalize=True).sort_index()
            actual_dist   = actual_bins.value_counts(normalize=True).sort_index()

            psi_df = pd.DataFrame({
                'expected': expected_dist,
                'actual': actual_dist
            }).fillna(0)

        # Avoid zeros
        psi_df['expected'] = psi_df['expected'].replace(0, 1e-6)
        psi_df['actual']   = psi_df['actual'].replace(0, 1e-6)

        # PSI formula
        psi_df['psi'] = ((psi_df['expected'] - psi_df['actual']) * 
                        np.log(psi_df['expected'] / psi_df['actual']))

        return psi_df, psi_df['psi'].sum()


      
    def score_stability(self):
            logging.info('calculating score PI')
            _, score_psi=self.calculate_psi(self.dev_df['pd'],self.oot_df['pd'])
            return score_psi

    def feature_stability(self):
            logging.info('Calculating feature PSI')
            
            feature_psi={}
            for col in self.feature_cols:
                _, psi_val=self.calculate_psi(self.dev_df[col], self.oot_df[col])
                feature_psi[col]=psi_val

            df=pd.DataFrame.from_dict(feature_psi, orient='index', columns=['PSI'])
            df['alert']=df['PSI'].apply(self.psi_alert_label)
            df['action']=df['PSI'].apply(self.monitoring_action)
            return df.sort_values(by='PSI',ascending=False)

    def psi_alert_label(self,psi):
        if psi <0.1:
            return 'Stable'
        elif psi <0.25:
            return 'Moderate shift'
        else:
            return 'Significant Drift'


    def monitoring_action(self,psi):
        if psi<0.1:
            return 'No action'
        elif psi <0.25:
            return 'Monitor'
        else:
            return 'Investigate'

    def run_monitoring(self):
        score_psi=self.score_stability()
        feature_psi_df=self.feature_stability()

        return {
            'score_psi':score_psi,
            'feature_psi':feature_psi_df,
            'version':self.version,
            'monitoring_date':self.monitoring_date}






