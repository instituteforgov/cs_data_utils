import re


def normalise_column_names(col_name: str) -> str:
    """Normalise a column name to snake_case, removing special characters.

    Args:
        col_name: The original column name.

    Returns:
        The normalised column name in snake_case.
    """
    return re.sub(r"\s+", "_", re.sub(r"[^\w\s]", "", col_name.lower())).strip("_")
