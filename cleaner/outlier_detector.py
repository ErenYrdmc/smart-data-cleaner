import pandas as pd

def detect_outliers_iqr(df: pd.DataFrame, threshold: float = 1.5) -> dict:
    outliers = {}
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - threshold * IQR
        upper_bound = Q3 + threshold * IQR

        outlier_idx = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()

        if outlier_idx:
            outliers[col] = outlier_idx

    return outliers