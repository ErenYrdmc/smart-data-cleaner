import pandas as pd

def normalize_categories(df: pd.DataFrame) -> pd.DataFrame:
    normalized_df = df.copy()

    for col in normalized_df.select_dtypes(include=['object']).columns:
        normalized_df[col] = normalized_df[col].astype(str).str.strip().str.lower().str.title()

    return normalized_df
