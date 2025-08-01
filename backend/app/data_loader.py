# backend/app/data_loader.py
import pandas as pd
from typing import List
from .config import logger

def load_and_clean_trades(file_paths: List[str]) -> pd.DataFrame:
    """
    Loads trade data from multiple CSV files, cleans it, and consolidates it.
    
    Args:
        file_paths: A list of string paths to the CSV files.

    Returns:
        A single pandas DataFrame containing all cleaned trade data.
    """
    all_trades = []
    
    if not file_paths or not file_paths[0]:
        logger.error("No trade files found. Check your .env configuration.")
        return pd.DataFrame()

    for file_path in file_paths:
        try:
            logger.info(f"Processing file: {file_path}")
            # Read the CSV, skipping the header row and filtering for actual data rows
            df = pd.read_csv(file_path, on_bad_lines='skip')
            
            # 1. Filter for rows that contain actual trade data
            df = df[df['DataDiscriminator'] == 'Data'].copy()

            # 2. Clean and convert data types
            # Convert 'Quantity' from string (e.g., "2,500") to numeric
            df['Quantity'] = df['Quantity'].astype(str).str.replace(',', '', regex=False)
            df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

            # Convert 'Date/Time' to datetime objects
            df['Date/Time'] = pd.to_datetime(df['Date/Time'], errors='coerce')
            
            # Drop rows where essential data could not be parsed
            df.dropna(subset=['Quantity', 'Date/Time', 'Symbol'], inplace=True)
            
            all_trades.append(df)
            logger.info(f"Successfully loaded and cleaned {len(df)} trades from {file_path}")

        except FileNotFoundError:
            logger.error(f"File not found: {file_path}. Skipping.")
        except Exception as e:
            logger.error(f"An error occurred while processing {file_path}: {e}")

    if not all_trades:
        logger.warning("No trade data was loaded.")
        return pd.DataFrame()

    # Concatenate all dataframes into one
    master_df = pd.concat(all_trades, ignore_index=True)
    
    # Sort by date to ensure chronological order
    master_df.sort_values(by='Date/Time', inplace=True)
    
    logger.info(f"Consolidated a total of {len(master_df)} trades from all files.")
    return master_df