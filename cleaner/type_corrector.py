import pandas as pd

def correct_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    corrected_df = df.copy()

    for col in corrected_df.columns:

        try:
            corrected_df[col] = pd.to_numeric(corrected_df[col])
            continue
        except:
            pass

        if 'date' in col.lower():
            try:
                corrected_df[col] = pd.to_datetime(corrected_df[col], format="%Y-%m-%d", errors="coerce")
            except:
                pass
        else:

            corrected_df[col] = corrected_df[col].astype(str)

    return corrected_df
