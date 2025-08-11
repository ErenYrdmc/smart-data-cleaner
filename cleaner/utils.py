import pandas as pd
import io

def convert_df_to_csv(df: pd.DataFrame) -> bytes:

    return df.to_csv(index=False).encode('utf-8')
