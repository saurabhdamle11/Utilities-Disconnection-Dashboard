# Standard imports
from datetime import datetime

# Third party imports
import pandas as pd

# Local imports
from .config import (
    COLD_PROTECTIONS_PATH, HEAT_PROTECTIONS_PATH, INDIVIDUAL_PROTECTIONS_PATH, PROCEDURAL_REQUIREMENTS_PATH,
    CITATION_MSG, CONTACT_MSG
)


cold_protection = pd.read_csv(COLD_PROTECTIONS_PATH)
heat_protection = pd.read_csv(HEAT_PROTECTIONS_PATH)
individual_protection = pd.read_csv(INDIVIDUAL_PROTECTIONS_PATH)
procedural_requirement = pd.read_csv(PROCEDURAL_REQUIREMENTS_PATH)

data = {
    # The keys must match the dropdown options (id=)
    "Cold-based Protections": cold_protection,
    "Heat-based Protections": heat_protection,
    "Protection for Individuals": individual_protection,
    "Procedual Requirements": procedural_requirement
}


index_to_letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_all_data():
    """
    Each protection type is written in its own worksheet.
    Each worksheet has all corresponding policies
    """
    writer = pd.ExcelWriter("download_buffer.xlsx", engine="xlsxwriter")
    for key in data:
        n_cols = len(data[key].columns)
        last_col = index_to_letter[n_cols-1]

        data[key].to_excel(
            writer,
            sheet_name=key,
            startrow=3,
            startcol=0,
            index=False
        )

        workbook = writer.book
        worksheet = writer.sheets[key]

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


def get_selected_data(protection):
    """
    Only one worksheet for the selected protection type, with all of its policies.
    """
    writer = pd.ExcelWriter("download_buffer.xlsx", engine="xlsxwriter")

    n_cols = len(data[protection].columns)
    last_col = index_to_letter[n_cols-1]

    data[protection].to_excel(
        writer,
        sheet_name=protection,
        startrow=3,
        startcol=0,
        index=False
    )

    workbook = writer.book
    worksheet = writer.sheets[protection]

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
