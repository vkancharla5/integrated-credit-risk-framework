#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class WoeBinner:
    def __init__(self):
        self.woe_tables={}
        self.woe_maps={}
        self.iv_values={}

        #store bin definitions for continuous variables
        self.bin_rules={}        

    def woe_discrete(self, df, discrete_variable_name, good_bad_variable):

        
        #combine feature and target
        temp=pd.concat([df[discrete_variable_name], good_bad_variable],axis=1)
        temp.columns=[discrete_variable_name, 'target']
        #target_name=good_bad_variable.name if good_bad_variable.name else 'good_bad_variable'
        #temp.columns=[discrete_variable_name, target_name]

        #group by feature
        grouped=temp.groupby(discrete_variable_name,observed=True)['target'].agg(['count','sum'])

        #rename columns
        grouped=grouped.rename(columns={'count':'n_obs', 'sum':'n_bad'})

        #calculate goods
        grouped['n_good']=grouped['n_obs']-grouped['n_bad']

        #total goods and bads
        total_good=grouped['n_good'].sum()
        total_bad=grouped['n_bad'].sum()

        #smootihg to avoid division by zero
        grouped['prop_n_good']=(grouped['n_good']+0.5)/total_good
        grouped['prop_n_bad']=(grouped['n_bad']+0.5)/total_bad

        #calculate WoE
        grouped['WoE']=np.log(grouped['prop_n_good']/grouped['prop_n_bad'])

        #replace infinite values if any
        grouped['WoE']=grouped['WoE'].replace([np.inf, -np.inf],0)

        #IV contribution
        grouped['IV']=(grouped['prop_n_good']-grouped['prop_n_bad'])*grouped['WoE']

        #Total IV
        iv=grouped['IV'].sum()

        #sort by WoE
        #grouped=grouped.sort_values('WoE').reset_index()
        grouped=grouped.reset_index()

        return grouped, iv

    def woe_continuous(self, df, continuous_variable, good_bad_variable, bins=10):
        temp=pd.concat([df[continuous_variable], good_bad_variable], axis=1)
        target_name=good_bad_variable.name if good_bad_variable.name else 'good_bad_variable'
        temp.columns=[continuous_variable, 'target']

        #create bins
        temp[continuous_variable+'_bin'], bin_edges=pd.qcut(temp[continuous_variable], q=bins, duplicates='drop', retbins=True)

        self.bin_rules[continuous_variable]=bin_edges
        
        #grouped by feature
        grouped=temp.groupby(continuous_variable+'_bin',observed=True)['target'].agg(['count', 'sum'])

         #rename columns
        grouped=grouped.rename(columns={'count':'n_obs','sum':'n_bad'})        

        #calculate goods
        grouped['n_good']=grouped['n_obs']-grouped['n_bad']        

        #total goods and bads
        total_good=grouped['n_good'].sum()
        total_bad=grouped['n_bad'].sum()        

        #smootihg to avoid division by zero
        grouped['prop_n_good']=(grouped['n_good']+0.5)/total_good
        grouped['prop_n_bad']=(grouped['n_bad']+0.5)/total_bad        

        #calculate WoE
        grouped['WoE']=np.log(grouped['prop_n_good']/grouped['prop_n_bad'])        

        #replace infinite values if any
        grouped['WoE']=grouped['WoE'].replace([np.inf, -np.inf],0)
        grouped['WoE']=grouped['WoE'].fillna(0)

        #IV contribution
        grouped['IV']=(grouped['prop_n_good']-grouped['prop_n_bad'])*grouped['WoE']
        iv=grouped['IV'].sum()

        grouped=grouped.reset_index()

        #store resultes
        self.woe_tables[continuous_variable]=grouped
        self.iv_values[continuous_variable]=iv

        self.woe_maps[continuous_variable+'_bin']=dict(zip(grouped[continuous_variable+'_bin'].astype(str), grouped['WoE']))

        return grouped, iv

    def set_bin_rules(self, variable, bins):

        '''
        Save the edges for a variable
        example : [0,8,11,15,100]
        '''
        self.bin_rules[variable]=bins

    def apply_bins(self, df):
        df_binned=df.copy()

        for variable, bins in self.bin_rules.items():
            df_binned[variable+'_bin']=pd.cut(df_binned[variable], bins=bins)
        return df_binned 
        
        

    def fit(self, X, y, discrete_vars=None, continuous_vars=None):
        self.woe_tables={}
        self.woe_maps={}
        self.iv_values={}

        if discrete_vars:
            for var in discrete_vars:
                woe_table, iv=self.woe_discrete(X, var, y)

                self.woe_tables[var]=woe_table
                self.iv_values[var]=iv
                self.woe_maps[var]=dict(zip(woe_table[var].astype(str),woe_table['WoE']))

        if continuous_vars:
            for var in continuous_vars:
                
                woe_table, iv=self.woe_continuous(X, var, y)
                self.woe_tables[var]=woe_table
                self.iv_values[var]=iv

                self.woe_maps[var+'_bin']=dict(
                    zip(woe_table[var+'_bin'].astype(str),woe_table['WoE']))

    def transform(self, X):
        X_woe=X.copy()
        for var, mapping in self.woe_maps.items():
            if var in X_woe.columns:                
                X_woe[var+'_woe']=X_woe[var].astype(str).map(mapping).fillna(0)
                       
        return X_woe
        
    def fit_transform(self, X, y, discrete_vars=None, continuous_vars=None)  :
        self.fit(X,y, discrete_vars, continuous_vars)
        return self.transform(X)    

    
    def plot_woe(self, feature, rotation_of_X_tick_lables=0):
        import matplotlib.pyplot as plt
        import numpy as np
        
        df_woe=self.woe_tables[feature]
        X=np.array(df_woe[feature].astype(str))
        y=df_woe['WoE']

        plt.figure(figsize=(18,6))
        plt.plot(X,y, marker='o', linestyle='--', color='black')

        plt.xlabel(feature)
        plt.ylabel('Weight of Evidence')
        plt.title(f'Weight of Evidence by {feature}')
        plt.xticks(rotation=rotation_of_X_tick_lables)
        plt.grid(True)
        plt.show()

    def iv_summary(self):
        iv_df=pd.DataFrame(list(self.iv_values.items()), columns=['Variable', 'IV'])
        return iv_df.sort_values('IV', ascending=False)


# ![image.png](attachment:63d01fa0-c6fa-44d1-b064-9d3ae7c92e11.png)

# ![image.png](attachment:d27d8272-d831-44c4-b760-80b0764571c9.png)

# In[ ]:




