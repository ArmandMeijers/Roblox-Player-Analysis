"""
Author: Armand Meijers
Date: 08/10/2026
Description: Functions for cleaning and handling raw CSV data.
"""

#imnports
import pandas as pd
from pathlib import Path

#HELPER FUNCTIONS
def csv_loading_helper(data_path: str) -> pd.DataFrame | None:
    """
    A helper function to safely load a CSV file and convert it into a pandas dataframe

    Args:
        data_path (str): Filepath of the csv file you want to turn into a dataframe

    Returns:
        pd.DataFrame | None: Returns the cleaned DataFrame  and if a error occures returns None
    """    
    
    #Error check to ensure inputed file has the correct format and extention
    path = Path(data_path)
    
    if not path.is_file():
        print(f"[ERROR]: File not found: {path}")
        return None
    
    if path.suffix.lower() != ".csv":
        print("[ERROR]: FILE IS NOT .CSV")
        return None

    #Reads in your path and converts csv fiel to a pd DataFrame
    df = pd.read_csv(data_path)
    
    #returns loaded dataframe that passed safety check
    return df

def data_cleaning_dated(data_path: str) -> pd.DataFrame | None:
    """
    Cleans a dated csv file that falls under the generic format

    Args:
        data_path (str): file path of the dated raw CSV file

    Returns:
        pd.DataFrame | None: a pandas DataFrame containing your cleaned datafrme
    """    
    
    #help loads csv file safely and converts to pd Dataframe
    df = csv_loading_helper(data_path)
    if df is None:
        return None

    #Standardise column names to lowercase and replace spaces with underscores
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
    )

    #removes duplicate rows
    df = df.drop_duplicates()
    
    #Cleaning function for dated csv files (checks if it has a date column)
    if "date" not in df.columns:
        print(f"[ERROR]: Missing date column: {data_path}")
        return None

    #Reformats dates into a more readable format and sorts them
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], utc=True)
        df = df.sort_values("date")
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    #Cleans retention column only when the column exists
    if "day_7_retention" in df.columns:
        df["day_7_retention"] = pd.to_numeric(
            df["day_7_retention"],
            errors="raise"
        ).fillna(0)

    #removes all rows, with the entry "Benchmark (Top 10,000 experience)" from breakdown column
    if "breakdown" in df.columns:
        df = df.loc[
            df["breakdown"] != "Benchmark (Top 10,000 experience)"
        ]
    
    #fills all numeric columns that have "NaN" or "None" with 0 (where appropriate)
    numeric_columns = df.select_dtypes(include="number").columns
    df[numeric_columns] = df[numeric_columns].fillna(0)

    #returns cleaned pd dataframe
    return df


def data_cleaning_misc(data_path: str) -> pd.DataFrame| None:
    """
    Cleans a unique csv files that doesnt fall under a common format

    Args:
        data_path (str): filepath of the misc csv file you want to clean

    Returns:
        pd.DataFrame | None: a pandas DataFrame containing your cleaned datafrme
    """ 
    
    #help loads csv file safely and converts to pd Dataframe
    df = csv_loading_helper(data_path)
    if df is None:
        return None
    
    #Standardise column names to lowercase and replace spaces with underscores
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", "_", regex=True)
    )
    
    #removes duplicate rows
    df = df.drop_duplicates()
    
    #fills all numeric columns that have "NaN" or "None" with 0 (where appropriate)
    numeric_columns = df.select_dtypes(include="number").columns
    df[numeric_columns] = df[numeric_columns].fillna(0)
    
    #removes breakdown column if it exisits for misc 
    if "breakdown" in df.columns:
        df = df.drop(columns=["breakdown"])
    
    #returns cleaned pandas dataframe
    return df