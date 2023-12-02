# Standard imports
from datetime import datetime

# Third party imports
import pandas as pd

# Local imports
from .config import (
    CITATION_MSG, CONTACT_MSG, STATE_CODE_TO_NAME,
    DISCONNECTION_COUNT_DATA_PATH, DISCONNECTION_UTILITY_DATA_PATH
)

disconnection_count_data = pd.read_csv(DISCONNECTION_COUNT_DATA_PATH)  # not sure it is ever used for download?
disconnection_utility_data = pd.read_csv(DISCONNECTION_UTILITY_DATA_PATH)

index_to_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_all_data():
    """
    Get hard_fix_feb_7.csv as Excel file
    """
    writer = pd.ExcelWriter("download_buffer.xlsx", engine="xlsxwriter")

    n_cols = len(disconnection_utility_data.columns)
    last_col = index_to_letter[n_cols-1]

    disconnection_utility_data.to_excel(
        writer,
        sheet_name="Utility Disconnections",
        startrow=3,
        startcol=0,
        index=False
    )

    workbook = writer.book
    worksheet = writer.sheets["Utility Disconnections"]

    worksheet.set_header("&C&[Picture]", {"image_center": "./assets/iu_logo.png"})
    merge_format = workbook.add_format(
        {
            "bold": 1,
            "align": "center",
            "valign": "vcenter",
        }
    )
    worksheet.merge_range(f"A1:{last_col}1", CITATION_MSG, merge_format)
    worksheet.merge_range(f"A2:{last_col}2", CONTACT_MSG, merge_format)
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    worksheet.merge_range(f"A3:{last_col}3", f"Date and Time of Download: {now}", merge_format)

    worksheet.set_column(f'A:{last_col}', 20)
    writer.close()
    return writer


def get_selected_data(state):
    """
    Get hard_fix_feb_7.csv as Excel file
    """
    state = STATE_CODE_TO_NAME[state]
    state_data = disconnection_utility_data[disconnection_utility_data["State"] == state]

    writer = pd.ExcelWriter("download_buffer.xlsx", engine="xlsxwriter")

    n_cols = len(state_data.columns)
    last_col = index_to_letter[n_cols-1]

    state_data.to_excel(
        writer,
        sheet_name=state,
        startrow=3,
        startcol=0,
        index=False
    )

    workbook = writer.book
    worksheet = writer.sheets[state]

    worksheet.set_header("&C&[Picture]", {"image_center": "./assets/iu_logo.png"})
    merge_format = workbook.add_format(
        {
            "bold": 1,
            "align": "center",
            "valign": "vcenter",
        }
    )
    worksheet.merge_range(f"A1:{last_col}1", CITATION_MSG, merge_format)
    worksheet.merge_range(f"A2:{last_col}2", CONTACT_MSG, merge_format)
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
    worksheet.merge_range(f"A3:{last_col}3", f"Date and Time of Download: {now}", merge_format)

    worksheet.set_column(f'A:{last_col}', 20)

    writer.close()
    return writer
