'''
Author: Armand Meijers
Date: 08/10/2026
Description: Constructs pipeline of all module functions to clean and format data 
'''

from pathlib import Path
import data_transformation as dt
import pandas as pd

def main_pipeline() -> None:
    
    #raw data folder paths
    raw_folder_dated = Path("data/raw/dated")
    raw_folder_misc = Path("data/raw/misc")
    
    #processed clean data folder path
    cleaned_folder_path = Path("data/processed/cleaned")

    #loops through all files in dated folder
    for file_path in raw_folder_dated.glob("*.csv"):
        #cleans each file
        df = dt.data_cleaning_dated(str(file_path))

        #skips file if error returned
        if df is None:
            continue

        #saves cleaned files to cleaned folder
        output_path = cleaned_folder_path / f"{file_path.stem}_cleaned.csv"
        df.to_csv(output_path, index=False)

    #loops through all files in MISC folder
    for file_path in raw_folder_misc.glob("*.csv"):
        df = dt.data_cleaning_misc(str(file_path))

        #skips file if error returned
        if df is None:
            continue

        #saves cleaned files to cleaned folder
        output_path = cleaned_folder_path / f"{file_path.stem}_cleaned.csv"
        df.to_csv(output_path, index=False)