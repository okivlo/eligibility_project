"""Function to save a pandas DataFrame as an excel file."""

from io import BytesIO

import pandas as pd


def save_and_format_df_as_excel(updated_researchers_dataframe: pd.DataFrame) -> BytesIO:
    """Function to save the updated hr dataframe as an Excel file with the correct formatting.

    Args:
        updated_researchers_dataframe (pd.DataFrame): The updated researchers dataframe.

    Returns:
        BytesIO: The Excel file in the requested format.
    """
    excel_buffer = BytesIO()

    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        # Write the DataFrame to Excel starting from the second row.
        updated_researchers_dataframe.to_excel(
            writer, startrow=1, index=False, sheet_name="Sheet1"
        )

        # Get the xlsxwriter workbook and worksheet objects.
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]

        # Define cell formats.
        header_format = workbook.add_format(
            {
                "bold": True,
                "text_wrap": True,
                "valign": "top",
                "fg_color": "#D7E4BC",
                "border": 1,
            }
        )
        workbook.add_format({"text_wrap": True, "valign": "top", "border": 1})
        alternating_color = workbook.add_format({"fg_color": "#F2F2F2"})

        # Apply formatting to headers (starting from the second row.)
        for col_num, value in enumerate(updated_researchers_dataframe.columns.values):
            worksheet.write(1, col_num, value, header_format)

        # Apply alternating row color.
        for row_num in range(
            2, len(updated_researchers_dataframe) + 2
        ):  # Start from the second row
            if row_num % 2 == 0:
                worksheet.set_row(row_num, None, alternating_color)

        # Enable sorting by clicking on column headers.
        worksheet.autofilter(
            1,
            0,
            len(updated_researchers_dataframe) + 1,
            len(updated_researchers_dataframe.columns) - 1,
        )

        # Adjust column width based on the length of the text.
        for i, col in enumerate(updated_researchers_dataframe.columns):
            column_len = max(
                updated_researchers_dataframe[col].astype(str).map(len).max(), len(col)
            )
            worksheet.set_column(i, i, column_len)

    excel_data = excel_buffer.getvalue()

    return excel_data
