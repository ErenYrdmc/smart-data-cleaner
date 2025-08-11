import pandas as pd

def analyze_missing_data(df: pd.DataFrame) -> pd.DataFrame:

    total_missing = df.isnull().sum()
    percent_missing = (total_missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': total_missing,
        'Missing %': percent_missing
    })

    missing_df = missing_df[missing_df['Missing Count'] > 0]
    return missing_df.sort_values(by= 'Missing %', ascending = False)

def fill_missing_data(df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:

    for col in df.columns:
        if df[col].isnull().any():
            if df[col].dtype in ['int64', 'float64']:
                if strategy == 'mean':
                    df[col].fillna(df[col].mean(), inplace= True)
                elif strategy == 'median':
                    df[col] = df[col].fillna(df[col].median())

            else:
                df[col] = df[col].fillna(df[col].mode()[0])
    return df




