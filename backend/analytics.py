import pandas as pd

def get_summary(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": int(df.duplicated().sum())
    }

def total(df, column):
    return df[column].sum()

def average(df, column):
    return df[column].mean()

def maximum(df, column):
    return df[column].max()

def minimum(df, column):
    return df[column].min()