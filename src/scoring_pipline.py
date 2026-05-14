import pickle
import pandas as pd
import numpy as np

from src.feature_engineering import apply_feature_engineering

import pickle
import pandas as pd
import numpy as np
from src.feature_engineering import apply_feature_engineering

# Load artifacts
with open("artifacts/pd_model.pkl", "rb") as f:
    pd_model = pickle.load(f)

with open("artifacts/woe_binner.pkl", "rb") as f:
    woe = pickle.load(f)

with open("artifacts/final_features.pkl", "rb") as f:
    features = pickle.load(f)

with open("artifacts/score_params.pkl", "rb") as f:
    params = pickle.load(f)

factor = params["factor"]
offset = params["offset"]


def score_data(df):

    # Step 1: Feature engineering
    df, _ = apply_feature_engineering(df, woe)

    # Step 2: Apply bins
    df = woe.apply_bins(df)

    # Step 3: WoE transform
    df = woe.transform(df)

    # Step 4: Select features
    X = df[features]

    # Step 5: Predict PD
    pd_vals = pd_model.predict_proba(X)

    # Step 6: Score
    score = offset - factor * np.log(pd_vals / (1 - pd_vals))

    return pd_vals, score

def assign_band_pd(pd):
    if pd < 0.01:
        return "Very Low Risk"
    elif pd < 0.02:
        return "Low Risk"
    elif pd < 0.03:
        return "Medium Risk"
    elif pd < 0.05:
        return "High Risk"
    else:
        return "Very High Risk"