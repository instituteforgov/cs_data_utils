import re

from IPython.display import display
import pandas as pd


def normalise_column_names(col_name: str) -> str:
    """Normalise a column name to snake_case, removing special characters.

    Args:
        col_name: The original column name.

    Returns:
        The normalised column name in snake_case.
    """
    return re.sub(r"\s+", "_", re.sub(r"[^\w\s]", "", col_name.lower())).strip("_")


def compare_dataframes(
    df_excel: pd.DataFrame,
    df_sql: pd.DataFrame,
    key_cols: list[str],
) -> None:
    """Compare two DataFrames (one from Excel, one from SQL) and report differences.

    Prints a summary of column differences, row counts, and value mismatches.
    The 'Value' column is compared numerically with a tolerance of 1e-9; all
    other shared non-key columns are compared by equality.

    Args:
        df_excel: DataFrame read from an Excel working file.
        df_sql: DataFrame read from a SQL query.
        key_cols: Columns used as the merge key to match rows between sources.

    Raises:
        AssertionError: If row counts before or after merging do not match.
    """
    df_excel_cols = set(df_excel.columns)
    df_sql_cols = set(df_sql.columns)
    cols_in_both = [col for col in df_excel.columns if col in df_sql_cols]
    cols_excel_only = [col for col in df_excel.columns if col not in df_sql_cols]
    cols_sql_only = [col for col in df_sql.columns if col not in df_excel_cols]
    print(f"Columns in both sources: {cols_in_both}")
    print(f"Columns only in Excel: {cols_excel_only}")
    print(f"Columns only in SQL: {cols_sql_only}")

    assert len(df_sql) == len(df_excel), (
        f"Row count mismatch before merge: SQL has {len(df_sql)} rows, Excel has {len(df_excel)} rows."
    )

    df_merged = df_sql.merge(df_excel, on=key_cols, how="outer", suffixes=("_sql", "_excel"), indicator=True)
    rows_in_both = df_merged[df_merged["_merge"] == "both"]
    rows_excel_only = df_merged[df_merged["_merge"] == "right_only"]
    rows_sql_only = df_merged[df_merged["_merge"] == "left_only"]
    print(f"Rows in both sources: {len(rows_in_both)}")
    print(f"Rows only in Excel: {len(rows_excel_only)}")
    print(f"Rows only in SQL: {len(rows_sql_only)}")

    assert len(df_merged) == len(df_sql), (
        f"Merged row count ({len(df_merged)}) differs from source row count ({len(df_sql)}). "
        f"{len(rows_excel_only)} Excel-only and {len(rows_sql_only)} SQL-only rows."
    )

    value_cols = [col for col in df_excel.columns if col in cols_in_both and col not in key_cols]

    mismatch_masks = {}
    for col in value_cols:
        sql_col = f"{col}_sql"
        excel_col = f"{col}_excel"
        if sql_col in rows_in_both.columns and excel_col in rows_in_both.columns:
            if col == "Value":
                sql_series = pd.to_numeric(rows_in_both[sql_col], errors="coerce")
                excel_series = pd.to_numeric(rows_in_both[excel_col], errors="coerce")
                match_mask = (
                    (sql_series - excel_series).abs().lt(1e-9)
                    | (sql_series.isna() & excel_series.isna())
                )
            else:
                sql_series = rows_in_both[sql_col]
                excel_series = rows_in_both[excel_col]
                match_mask = (
                    (sql_series == excel_series)
                    | (rows_in_both[sql_col].isna() & rows_in_both[excel_col].isna())
                )
            if (~match_mask).any():
                mismatch_masks[col] = ~match_mask

    if mismatch_masks:
        display({col: int(mask.sum()) for col, mask in mismatch_masks.items()})
        for col, mask in mismatch_masks.items():
            sql_col = f"{col}_sql"
            excel_col = f"{col}_excel"
            if col == "Value":
                preview = rows_in_both.loc[mask, key_cols + [sql_col, excel_col]].reset_index(drop=True)
            else:
                preview = (
                    rows_in_both.loc[mask, key_cols + [sql_col, excel_col]]
                    .drop_duplicates()
                    .reset_index(drop=True)
                )
            print(f"Mismatches in '{col}':")
            display(preview)
    else:
        print("No value mismatches in matched rows")
