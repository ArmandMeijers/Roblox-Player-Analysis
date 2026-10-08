"""
Author: Armand Meijers
Date: 08/10/2026
Description: Functions for cleaning raw Roblox CSV data.
"""

import csv
from pathlib import Path

import pandas as pd

# These columns describe records; all other supported columns are numerical.
TEXT_COLUMNS = {"Breakdown", "Source", "Series", "Revenue Source"}


def _load_csv(data_path: str | Path) -> pd.DataFrame:
    """Read an export, including files with metadata above the table."""
    path = Path(data_path)
    metadata_date = None

    with path.open(encoding="utf-8-sig", newline="") as file:
        for row_number, row in enumerate(csv.reader(file)):
            if not row:
                continue
            row = [cell.strip() for cell in row]
            if row[0] == "Date" and len(row) == 2:
                metadata_date = row[1]
            if row[0] in TEXT_COLUMNS:
                header_row = row_number
                break
        else:
            raise ValueError(f"No supported Roblox CSV header found in {path.name}")

    df = pd.read_csv(path, skiprows=header_row, encoding="utf-8-sig")
    df.columns = df.columns.str.strip()
    if metadata_date is not None and "Date" not in df.columns:
        df["Date"] = metadata_date
    return df


def data_cleaning(data_path: str | Path) -> pd.DataFrame:
    """Return a cleaned table without modifying the original CSV.

    Dates become YYYY-MM-DD strings. Missing numerical values become zero
    by project convention, including unavailable retention measurements.
    Invalid dates or non-numerical metric text raise an error for review.
    Labels, genuine zeros, breakdowns, and duplicate rows are preserved.
    """
    df = _load_csv(data_path)

    for column in df.columns:
        if column in TEXT_COLUMNS:
            df[column] = df[column].astype("string").str.strip()
        elif column == "Date":
            dates = pd.to_datetime(df[column], utc=True, errors="raise")
            if dates.isna().any():
                raise ValueError(f"Missing dates in {Path(data_path).name}")
            df[column] = dates.dt.strftime("%Y-%m-%d")
        else:
            df[column] = pd.to_numeric(df[column], errors="raise").fillna(0)

    if "Date" in df.columns:
        df = df.sort_values("Date", kind="stable")

    return df.reset_index(drop=True)
