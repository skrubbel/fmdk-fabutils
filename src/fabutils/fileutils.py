from logging import Logger
from typing import Any
import pandas as pd
import pyarrow as pa


def excel_sheet_to_pyarrow_table(
    abfss_path: str, sheet_name: str, logger: Logger = None, **kwargs: Any
) -> pa.Table:
    """
    Read a specific sheet from an Excel file.

    Args:
        abfss_path: ABFSS path to the Excel file (.xlsx format)
        sheet_name: Name of the sheet to read
        logger: Logger object
        **Kwargs: Keyword arguments (Passed on to pandas.read_excel())

    Returns:
        PyArrow Table containing the sheet data

    Example:
        >>> config_table = read_config_sheet(
        ...     "abfss://container@storage.dfs.core.windows.net/config/solution_config.xlsx",
        ...     "workspaces"
        ... )
    """
    try:
        # Read Excel sheet using pandas
        df = pd.read_excel(
            abfss_path,
            sheet_name=sheet_name,
            engine="openpyxl",  # Required for .xlsx files
        )

        # Convert to PyArrow Table
        arrow_table = pa.Table.from_pandas(df)

        if logger:
            logger.info(f"✓ Successfully read sheet '{sheet_name}' with {len(df)} rows")
            logger.info(f"  Columns: {', '.join(df.columns)}")

        return arrow_table

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {abfss_path}")
    except ValueError as e:
        raise ValueError(f"Sheet '{sheet_name}' not found in workbook: {e}")
    except Exception as e:
        raise Exception(f"Error reading Excel file: {str(e)}")
