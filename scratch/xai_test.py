import joblib
import pandas as pd
fi_df = joblib.load("model/rf_feature_importances.joblib")
print(fi_df.head(20))
