'''
Author: Armand Meijers
Date: 09/10/2026
Description: Constructs pipeline of all module functions to manipulate data
'''

from pathlib import Path
import data_transformation as dt
import pandas as pd

def main_pipeline() -> None:
    
    #raw data folder paths
    raw_folder_dated = Path("data/raw/dated")
    raw_folder_misc = Path("data/raw/misc")
    
    merging_files = []
    separate_files = {
        "Robux_Sources_Revenue_2026-08-12_To_2026-10-06.csv",
        "Unique_Users_With_Plays_2026-08-13_To_2026-10-07.csv",
    }
    
    #processed clean data folder path
    cleaned_folder_path = Path("data/processed/cleaned")

    #loops through all files in dated folder
    for file_path in raw_folder_dated.glob("*.csv"):
        #cleans each file
        df = dt.data_cleaning_dated(str(file_path))

        #skips file if error returned
        if df is None:
            continue
        
        #checks if file is intended to be merged or pivoted
        if file_path.name in separate_files:
            if "revenue_source" in df.columns:
                #pivots dataframe
                df = dt.pivot_dataframe(df, "revenue_source", "revenue")
            else:
                df = dt.pivot_dataframe(df, "source", "unique_users_with_plays")

            output_path = cleaned_folder_path / f"{file_path.stem}_pivoted_cleaned.csv"
            df.to_csv(output_path, index=False)
        else:
            #appends df to list
            merging_files.append(df)
            
    #calls function to merge related csv files together into singular file
    if merging_files:
        merged_df = dt.merging_files(merging_files)

        if merged_df is not None:
            output_path = cleaned_folder_path / "daily_metrics_cleaned.csv"
            merged_df.to_csv(output_path, index=False)
    else:
        print("[WARNING]: No dated datasets available to merge")


    #loops through all files in MISC folder
    for file_path in raw_folder_misc.glob("*.csv"):
        df = dt.data_cleaning_misc(str(file_path))

        #skips file if error returned
        if df is None:
            continue

        #saves cleaned files to cleaned folder
        output_path = cleaned_folder_path / f"{file_path.stem}_cleaned.csv"
        df.to_csv(output_path, index=False)