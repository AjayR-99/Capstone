import requests
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
    

def preprocess_stock(file_path):
    """
    Load a stock or index CSV, parse dates, sort, drop bad rows,
    and compute log adjusted returns.
    """
    df = pd.read_csv(file_path)

    # Parse date column
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])  # drop invalid dates
    df = df.sort_values('Date').drop_duplicates(subset=['Date'], keep='last')

    # Ensure Adjusted price exists
    if 'Adjusted' not in df.columns:
        raise ValueError(f"'Adjusted' column missing in {file_path}")

    # Compute log adjusted returns
    df['Log_Adj_Return'] = np.log(df['Adjusted'] / df['Adjusted'].shift(1))
    df = df.dropna(subset=['Log_Adj_Return'])

    df.set_index('Date', inplace=True)
    return df