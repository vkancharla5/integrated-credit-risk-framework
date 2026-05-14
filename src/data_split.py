#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sklearn.model_selection import train_test_split


# In[2]:


def split_data(df, target='good_bad',test_size=0.2, random_state=42):
    
    train_df, test_df= train_test_split(df, test_size=test_size, random_state=random_state, stratify=df[target])
    return train_df, test_df


# In[ ]:




