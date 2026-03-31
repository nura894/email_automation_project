import pandas as pd
import re

def is_valid_email(email):
    if pd.isna(email):
        return False
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", str(email)))


def clean_csv_from_df(df):
    print(f"Original rows: {len(df)}")

    df.columns = df.columns.str.strip().str.lower()
 
    required_cols = ['name', 'email', 'company']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df['name'] = df['name'].astype(str).str.strip()
    df['email'] = df['email'].astype(str).str.strip().str.lower()
    df['company'] = df['company'].astype(str).str.strip()
    
    df = df.dropna(subset=required_cols)
    df = df[df['email'].apply(is_valid_email)]
    df = df.drop_duplicates(subset=['email'], keep='first')

    print(f"Clean rows: {len(df)}")

    return df