# import streamlit as st
# import pandas as pd
# from io import BytesIO
# from datetime import date
# import openpyxl


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Company Standard Format",
#     page_icon="💎",
#     layout="wide"
# )


# # ============================================================
# # COMPANY STANDARD COLUMNS
# # ============================================================

# COMPANY_COLUMNS = [
#     "SELECTION DONE BY",
#     "INDIA PRICE FILLED BY",
#     "USA PRICE FILLED BY",
#     "FINAL THIS FILE  BY ",
#     "DATE",
#     "STONE ID",
#     "PARTY NAME",
#     "REPORT NO.",
#     "GROWTH TYPE",
#     "SHAPE",
#     "CTS",
#     "SIZE GROUP",
#     "COLOR",
#     "CLARITY",
#     "KEY",
#     "GRID",
#     "AVAILABLE",
#     "SAME",
#     "REMARK",
#     "PER CARAT",
#     "TOTAL AMT",
#     "VDB PRICE INDIA",
#     "VDB AMOUNT INDIA",
#     "VDB PRICE USA",
#     "VDB AMOUNT USA",
#     "WITH TARIFF COST",
#     "WITH TARIFF AMOUNT",
#     "IND%",
#     "USA%",
#     "AFTER TARIFF DIFF$"
# ]


# # ============================================================
# # PARTY FIELDS WHICH USER MUST MAP
# # ============================================================

# PARTY_FIELDS = [
#     "STONE ID",
#     "REPORT NO.",
#     "GROWTH TYPE",
#     "SHAPE",
#     "CTS",
#     "COLOR",
#     "CLARITY",
#     "PER CARAT",
#     "VDB PRICE INDIA",
#     "VDB PRICE USA"
# ]


# # ============================================================
# # PARTY FIELD → COMPANY FIELD
# # ============================================================

# FIELD_TO_COMPANY_COLUMN = {

#     "STONE ID": "STONE ID",

#     "REPORT NO.": "REPORT NO.",

#     "GROWTH TYPE": "GROWTH TYPE",

#     "SHAPE": "SHAPE",

#     "CTS": "CTS",

#     "COLOR": "COLOR",

#     "CLARITY": "CLARITY",

#     "PER CARAT": "PER CARAT",

#     "VDB PRICE INDIA": "VDB PRICE INDIA",

#     "VDB PRICE USA": "VDB PRICE USA"
# }


# # ============================================================
# # SESSION STATE
# # ============================================================

# if "converted_files" not in st.session_state:
#     st.session_state.converted_files = {}


# # ============================================================
# # FUNCTIONS
# # ============================================================
# def get_size_group(cts):
#     """
#     Calculate Size Group from CTS.
#     """

#     if pd.isna(cts):
#         return ""

#     try:
#         cts = float(cts)
#     except (ValueError, TypeError):
#         return ""

#     if cts < 0.30:
#         return ""

#     if cts <= 0.50:
#         return "0.30 - 0.50"
    
#     if cts <= 0.59:
#             return "0.50 - 0.59"

#     if cts <= 0.69:
#         return "0.60 - 0.69"

#     if cts <= 0.79:
#         return "0.70 - 0.79"

#     if cts <= 0.89:
#         return "0.80 - 0.89"

#     if cts <= 0.94:
#         return "0.90 - 0.94"

#     if cts <= 0.99:
#         return "0.95 - 0.99"

#     if cts <= 1.10:
#         return "1.00 - 1.10"

#     if cts <= 1.19:
#         return "1.11 - 1.19"

#     if cts <= 1.29:
#         return "1.20 - 1.29"

#     if cts <= 1.39:
#         return "1.30 - 1.39"

#     if cts <= 1.49:
#         return "1.40 - 1.49"

#     if cts < 4.00:
#         lower = int(cts * 10) / 10
#         upper = lower + 0.09
#         return f"{lower:.2f} - {upper:.2f}"

#     if cts <= 4.10:
#         return "4.00 - 4.10"

#     if cts < 4.50:
#         return "4.11 - 4.49"

#     if cts <= 4.59:
#         return "4.50 - 4.59"

#     if cts < 5.00:
#         return "4.60 - 4.99"

#     if cts <= 5.59:
#         return "5.00 - 5.59"

#     if cts < 6.00:
#         return "5.60 - 5.99"

#     if cts < 7.00:
#         return "6.00 - 6.99"

#     # 7 CTS onwards
#     whole = int(cts)
#     decimal = cts - whole

#     if decimal <= 0.10:
#         return f"{whole:.2f} - {whole + 0.10:.2f}"

#     return f"{whole + 0.11:.2f} - {whole + 0.99:.2f}"

# def read_excel(file):
#     """
#     Read Excel file.
#     """

#     file.seek(0)

#     return pd.read_excel(
#         file,
#         engine="openpyxl"
#     )


# def normalize_column_name(value):
#     """
#     Normalize column name for comparison.
#     """

#     if value is None:
#         return ""

#     return (
#         str(value)
#         .strip()
#         .upper()
#         .replace("\n", " ")
#         .replace("_", " ")
#     )


# def validate_company_format(columns):
#     """
#     Validate Company Standard Format.
#     """

#     actual = [
#         normalize_column_name(c)
#         for c in columns
#     ]

#     required = [
#         normalize_column_name(c)
#         for c in COMPANY_COLUMNS
#     ]

#     missing = []

#     for column in required:

#         if column not in actual:
#             missing.append(column)

#     return missing


# def create_blank_output(number_of_rows):
#     """
#     Create blank DataFrame using exact Company Format columns.
#     """

#     output = pd.DataFrame(
#         "",
#         index=range(number_of_rows),
#         columns=COMPANY_COLUMNS
#     )

#     return output
# # def convert_party_file(
# #     party_df,
# #     master_df,
# #     mapping,
# #     party_name,
# #     selection_done_by,
# #     india_price_filled_by,
# #     usa_price_filled_by,
# #     final_file_by,
# #     selected_date
# # ):
# #     """
# #     Convert Party File into Company Standard Format.

# #     Flow:
# #     1. Map Party columns to Company columns
# #     2. Calculate SIZE GROUP from CTS
# #     3. Create KEY from:
# #            Shape + Size Group + Color + Clarity
# #     4. Match KEY with Master File KEY
# #     5. Bring Grid and Available from Master File
# #     6. Return final Company Standard Format
# #     """

# #     # ========================================================
# #     # CREATE EMPTY COMPANY OUTPUT
# #     # ========================================================

# #     output = pd.DataFrame(
# #         index=party_df.index
# #     )


# #     # ========================================================
# #     # MAP PARTY COLUMNS → COMPANY COLUMNS
# #     # ========================================================

# #     for party_field, party_column in mapping.items():

# #         company_column = FIELD_TO_COMPANY_COLUMN[
# #             party_field
# #         ]

# #         output[company_column] = (
# #             party_df[party_column]
# #             .reset_index(drop=True)
# #         )


# #     # ========================================================
# #     # SIZE GROUP
# #     # ========================================================

# #     if "CTS" in output.columns:

# #         output["SIZE GROUP"] = output["CTS"].apply(
# #             get_size_group
# #         )

# #     else:

# #         output["SIZE GROUP"] = ""


# #     # ========================================================
# #     # CLEAN KEY FIELDS
# #     # ========================================================

# #     for column in [
# #         "SHAPE",
# #         "SIZE GROUP",
# #         "COLOR",
# #         "CLARITY"
# #     ]:

# #         if column not in output.columns:

# #             output[column] = ""

# #         output[column] = (
# #             output[column]
# #             .fillna("")
# #             .astype(str)
# #             .str.strip()
# #         )


# #     # ========================================================
# #     # CREATE KEY
# #     #
# #     # Shape + Size Group + Color + Clarity
# #     #
# #     # IMPORTANT:
# #     # This KEY is created from COMPANY FORMAT,
# #     # NOT from Party File.
# #     # ========================================================

# #     output["KEY"] = (
# #         output["SHAPE"]
# #         + output["SIZE GROUP"]
# #         + output["COLOR"]
# #         + output["CLARITY"]
# #     )


# #     # ========================================================
# #     # PREPARE MASTER FILE
# #     # ========================================================

# #     master_lookup = master_df.copy()


# #     # Check Master KEY
# #     if "KEY" not in master_lookup.columns:

# #         raise ValueError(
# #             "Master File does not contain a 'KEY' column."
# #         )


# #     # ========================================================
# #     # CLEAN MASTER KEY
# #     # ========================================================

# #     master_lookup["KEY"] = (
# #         master_lookup["KEY"]
# #         .fillna("")
# #         .astype(str)
# #         .str.strip()
# #     )


# #     # ========================================================
# #     # KEEP ONLY REQUIRED MASTER COLUMNS
# #     # ========================================================

# #     required_master_columns = [
# #         "KEY",
# #         "Grid",
# #         "Available"
# #     ]

# #     missing_columns = [
# #         column
# #         for column in required_master_columns
# #         if column not in master_lookup.columns
# #     ]

# #     if missing_columns:

# #         raise ValueError(
# #             "Master File is missing columns: "
# #             + ", ".join(missing_columns)
# #         )


# #     master_lookup = master_lookup[
# #         required_master_columns
# #     ].copy()


# #     # ========================================================
# #     # CONVERT GRID / AVAILABLE TO NUMBERS
# #     # ========================================================

# #     master_lookup["Grid"] = pd.to_numeric(
# #         master_lookup["Grid"],
# #         errors="coerce"
# #     ).fillna(0)


# #     master_lookup["Available"] = pd.to_numeric(
# #         master_lookup["Available"],
# #         errors="coerce"
# #     ).fillna(0)


# #     # ========================================================
# #     # REMOVE DUPLICATE MASTER KEYS
# #     #
# #     # Keep the first matching Master record.
# #     # ========================================================

# #     master_lookup = master_lookup.drop_duplicates(
# #         subset=["KEY"],
# #         keep="first"
# #     )


# #     # ========================================================
# #     # MATCH COMPANY KEY WITH MASTER KEY
# #     #
# #     # Party File KEY is NOT used.
# #     #
# #     # We use the KEY created above from:
# #     # Shape + Size Group + Color + Clarity
# #     # ========================================================

# #     output = output.merge(
# #         master_lookup,
# #         on="KEY",
# #         how="left"
# #     )


# #     # ========================================================
# #     # GRID
# #     #
# #     # If KEY found → Master Grid
# #     # If KEY not found → 0
# #     # ========================================================

# #     output["Grid"] = (
# #         pd.to_numeric(
# #             output["Grid"],
# #             errors="coerce"
# #         )
# #         .fillna(0)
# #     )


# #     # ========================================================
# #     # AVAILABLE
# #     #
# #     # If KEY found → Master Available
# #     # If KEY not found → 0
# #     # ========================================================

# #     output["Available"] = (
# #         pd.to_numeric(
# #             output["Available"],
# #             errors="coerce"
# #         )
# #         .fillna(0)
# #     )


# #     # ========================================================
# #     # RETURN COMPANY COLUMN ORDER
# #     # ========================================================

# #     # Keep only columns that actually exist
# #     ordered_columns = [
# #         column
        
# #         for column in COMPANY_COLUMNS
# #         if column in output.columns
# #     ]


# #     # Add any columns not already included
# #     remaining_columns = [
# #         column
# #         for column in output.columns
# #         if column not in ordered_columns
# #     ]


# #     output = output[
# #         ordered_columns + remaining_columns
# #     ]


# #     # ========================================================
# #     # RESET INDEX
# #     # ========================================================

# #     output = output.reset_index(
# #         drop=True
# #     )


# #     return output



# def convert_party_file(
#     party_df,
#     master_df,
#     mapping,
#     party_name,
#     selection_done_by,
#     india_price_filled_by,
#     usa_price_filled_by,
#     final_file_by,
#     selected_date
# ):
#     """
#     Convert Party File into Company Standard Format.

#     Flow:
#     1. Map Party columns
#     2. Fill Company information
#     3. Create Size Group
#     4. Create KEY from Company Format
#     5. Match KEY with Master File
#     6. Get GRID and AVAILABLE
#     7. Create remaining Company columns
#     8. Return final DataFrame
#     """

#     # ========================================================
#     # CREATE OUTPUT
#     # ========================================================

#     output = pd.DataFrame(
#         index=range(len(party_df))
#     )


#     # ========================================================
#     # MAP PARTY COLUMNS
#     # ========================================================

#     for party_field, party_column in mapping.items():

#         if party_column not in party_df.columns:
#             continue

#         company_column = FIELD_TO_COMPANY_COLUMN.get(
#             party_field
#         )

#         if company_column is None:
#             continue

#         output[company_column] = (
#             party_df[party_column]
#             .reset_index(drop=True)
#         )


#     # ========================================================
#     # CREATE REQUIRED COMPANY COLUMNS
#     # ========================================================

#     required_columns = [
#         "STONE ID",
#         "REPORT NO.",
#         "GROWTH TYPE",
#         "SHAPE",
#         "CTS",
#         "COLOR",
#         "CLARITY",
#         "PER CARAT",
#         "VDB PRICE INDIA",
#         "VDB PRICE USA"
#     ]

#     for column in required_columns:

#         if column not in output.columns:

#             output[column] = ""


#     # ========================================================
#     # USER ENTERED INFORMATION
#     # ========================================================

#     output["PARTY NAME"] = party_name

#     output["SELECTION DONE BY"] = selection_done_by

#     output["INDIA PRICE FILLED BY"] = (
#         india_price_filled_by
#     )

#     output["USA PRICE FILLED BY"] = (
#         usa_price_filled_by
#     )

#     output["FINAL THIS FILE BY "] = (
#         final_file_by
#     )

#     output["DATE"] = selected_date


#     # ========================================================
#     # SIZE GROUP
#     # ========================================================

#     output["SIZE GROUP"] = output["CTS"].apply(
#         get_size_group
#     )


#     # ========================================================
#     # CLEAN KEY FIELDS
#     # ========================================================

#     for column in [
#         "SHAPE",
#         "SIZE GROUP",
#         "COLOR",
#         "CLARITY"
#     ]:

#         output[column] = (
#             output[column]
#             .fillna("")
#             .astype(str)
#             .str.strip()
#         )


#     # ========================================================
#     # CREATE KEY
#     #
#     # Shape + Size Group + Color + Clarity
#     # ========================================================

#     output["KEY"] = (
#         output["SHAPE"]
#         + output["SIZE GROUP"]
#         + output["COLOR"]
#         + output["CLARITY"]
#     )


#     # ========================================================
#     # MASTER FILE PREPARATION
#     # ========================================================

#     master_lookup = master_df.copy()


#     # --------------------------------------------------------
#     # Check Master KEY
#     # --------------------------------------------------------

#     if "KEY" not in master_lookup.columns:

#         raise ValueError(
#             "Master File does not contain a KEY column."
#         )


#     # --------------------------------------------------------
#     # Clean Master KEY
#     # --------------------------------------------------------

#     master_lookup["KEY"] = (
#         master_lookup["KEY"]
#         .fillna("")
#         .astype(str)
#         .str.strip()
#     )


#     # ========================================================
#     # CHECK MASTER GRID / AVAILABLE
#     # ========================================================

#     if "Grid" not in master_lookup.columns:

#         raise ValueError(
#             "Master File does not contain Grid column."
#         )


#     if "Available" not in master_lookup.columns:

#         raise ValueError(
#             "Master File does not contain Available column."
#         )


#     # ========================================================
#     # CREATE MASTER LOOKUP
#     # ========================================================

#     master_lookup = master_lookup[
#         [
#             "KEY",
#             "Grid",
#             "Available"
#         ]
#     ].copy()


#     # ========================================================
#     # CONVERT GRID / AVAILABLE TO NUMBER
#     # ========================================================

#     master_lookup["Grid"] = pd.to_numeric(
#         master_lookup["Grid"],
#         errors="coerce"
#     ).fillna(0)


#     master_lookup["Available"] = pd.to_numeric(
#         master_lookup["Available"],
#         errors="coerce"
#     ).fillna(0)


#     # ========================================================
#     # REMOVE DUPLICATE MASTER KEYS
#     # ========================================================

#     master_lookup = master_lookup.drop_duplicates(
#         subset=["KEY"],
#         keep="first"
#     )


#     # ========================================================
#     # MATCH PARTY COMPANY KEY WITH MASTER KEY
#     # ========================================================

#     output = output.merge(
#         master_lookup,
#         on="KEY",
#         how="left"
#     )


#     # ========================================================
#     # RENAME MASTER COLUMNS TO COMPANY FORMAT
#     # ========================================================

#     output["GRID"] = (
#         pd.to_numeric(
#             output["Grid"],
#             errors="coerce"
#         )
#         .fillna(0)
#     )


#     output["AVAILABLE"] = (
#         pd.to_numeric(
#             output["Available"],
#             errors="coerce"
#         )
#         .fillna(0)
#     )


#     # Remove temporary Master columns

#     if "Grid" in output.columns:

#         output.drop(
#             columns=["Grid"],
#             inplace=True
#         )


#     if "Available" in output.columns:

#         output.drop(
#             columns=["Available"],
#             inplace=True
#         )


#     # ========================================================
#     # SAME
#     #
#     # This will also be written as Excel formula later.
#     # ========================================================

#     output["SAME"] = ""


#     # ========================================================
#     # REMARK
#     # ========================================================

#     output["REMARK"] = ""


#     # ========================================================
#     # FORMULA COLUMNS
#     #
#     # These are intentionally blank here.
#     # create_download_excel() will write actual Excel
#     # formulas into these columns.
#     # ========================================================

#     formula_columns = [
#         "TOTAL AMT",
#         "VDB AMOUNT INDIA",
#         "VDB AMOUNT USA",
#         "WITH TARIFF COST",
#         "WITH TARIFF AMOUNT",
#         "IND%",
#         "USA%",
#         "AFTER TARIFF DIFF$"
#     ]


#     for column in formula_columns:

#         output[column] = ""


#     # ========================================================
#     # FINAL COMPANY COLUMN ORDER
#     # ========================================================

#     COMPANY_COLUMNS = [
#         "SELECTION DONE BY",
#         "PARTY NAME",
#         "DATE",

#         "STONE ID",
#         "REPORT NO.",
#         "GROWTH TYPE",

#         "SHAPE",
#         "CTS",
#         "SIZE GROUP",
#         "COLOR",
#         "CLARITY",

#         "KEY",
#         "SAME",

#         "PER CARAT",

#         "VDB PRICE INDIA",
#         "VDB AMOUNT INDIA",

#         "VDB PRICE USA",
#         "VDB AMOUNT USA",

#         "GRID",
#         "AVAILABLE",

#         "TOTAL AMT",

#         "WITH TARIFF COST",
#         "WITH TARIFF AMOUNT",

#         "IND%",
#         "USA%",

#         "AFTER TARIFF DIFF$",

#         "INDIA PRICE FILLED BY",
#         "USA PRICE FILLED BY",

#         "FINAL THIS FILE BY ",

#         "REMARK"
#     ]


#     # ========================================================
#     # MAKE SURE EVERY COMPANY COLUMN EXISTS
#     # ========================================================

#     for column in COMPANY_COLUMNS:

#         if column not in output.columns:

#             output[column] = ""


#     # ========================================================
#     # FINAL ORDER
#     # ========================================================

#     output = output[
#         COMPANY_COLUMNS
#     ]


#     # ========================================================
#     # RESET INDEX
#     # ========================================================

#     output = output.reset_index(
#         drop=True
#     )


#     return output









# # def convert_party_file(
# #     party_df,
# #     mapping,
# #     party_name,
# #     selection_done_by,
# #     india_price_filled_by,
# #     usa_price_filled_by,
# #     final_file_by,
# #     selected_date
# # ):
# #     """
# #     Convert one Party File into Company Standard Format.
# #     """

# #     row_count = len(party_df)

# #     output = create_blank_output(row_count)


# #     # ========================================================
# #     # A-E : USER ENTERED INFORMATION
# #     # ========================================================

# #     output["SELECTION DONE BY"] = selection_done_by

# #     output["INDIA PRICE FILLED BY"] = india_price_filled_by

# #     output["USA PRICE FILLED BY"] = usa_price_filled_by

# #     output["FINAL THIS FILE  BY "] = final_file_by

# #     output["DATE"] = selected_date.strftime(
# #         "%d-%m-%Y"
# #     )
    


# #     # ========================================================
# #     # G : PARTY NAME
# #     # ========================================================

# #     output["PARTY NAME"] = party_name


# #     # ========================================================
# #     # PARTY MAPPED COLUMNS
# #     # ========================================================

# #     for party_field, party_column in mapping.items():

# #         company_column = FIELD_TO_COMPANY_COLUMN[
# #             party_field
# #         ]

# #         output[company_column] = (
# #             party_df[party_column]
# #             .reset_index(drop=True)
# #         )

# #     output["SIZE GROUP"] = output["CTS"].apply(
# #         get_size_group
# #     )

    
# #     # ========================================================
# #     # RETURN EXACT COMPANY ORDER
# #     # ========================================================

# #     output = output[
# #         COMPANY_COLUMNS
# #     ]

# #     return output

# # def create_download_excel(df):
#     """
#     Create downloadable Excel file with actual Excel formulas.
#     """

#     output = BytesIO()

#     with pd.ExcelWriter(
#         output,
#         engine="xlsxwriter"
#     ) as writer:

#         # ====================================================
#         # WRITE DATA
#         # ====================================================

#         df.to_excel(
#             writer,
#             index=False,
#             sheet_name="Final File"
#         )

#         workbook = writer.book
#         worksheet = writer.sheets["Final File"]


#         # ====================================================
#         # FORMATS
#         # ====================================================

#         header_format = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True
#         })


#         normal_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter"
#         })


#         number_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0.00"
#         })


#         percent_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0.00"
#         })


#         date_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "dd-mm-yyyy"
#         })


#         # ====================================================
#         # HEADER
#         # ====================================================

#         for col_number, column in enumerate(
#             df.columns
#         ):

#             worksheet.write(
#                 0,
#                 col_number,
#                 column,
#                 header_format
#             )


#         # ====================================================
#         # FIND COLUMN NUMBERS
#         # ====================================================

#         column_numbers = {
#             str(column).strip(): index
#             for index, column in enumerate(
#                 df.columns
#             )
#         }


#         # ====================================================
#         # COLUMNS WHICH WILL CONTAIN FORMULAS
#         # ====================================================

#         formula_columns = [
#             "KEY",
#             "TOTAL AMT",
#             "VDB AMOUNT INDIA",
#             "VDB AMOUNT USA",
#             "WITH TARIFF COST",
#             "WITH TARIFF AMOUNT",
#             "IND%",
#             "USA%",
#             "AFTER TARIFF DIFF$",
#             "SAME"
#         ]


#         # ====================================================
#         # WRITE NORMAL DATA
#         # ====================================================

#         for row_number in range(
#             len(df)
#         ):

#             for col_number, column in enumerate(
#                 df.columns
#             ):

#                 # ------------------------------------------------
#                 # Skip formula columns.
#                 # They will be written below as Excel formulas.
#                 # ------------------------------------------------

#                 if str(column).strip() in formula_columns:
#                     continue


#                 value = df.iloc[
#                     row_number,
#                     col_number
#                 ]


#                 # ------------------------------------------------
#                 # Blank value
#                 # ------------------------------------------------

#                 if pd.isna(value):

#                     value = ""


#                 # ------------------------------------------------
#                 # DATE COLUMN
#                 # ------------------------------------------------

#                 if str(column).strip() == "DATE":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         date_format
#                     )

#                 else:

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         normal_format
#                     )


#         # ====================================================
#         # WRITE EXCEL FORMULAS
#         # ====================================================

#         for row_number in range(
#             len(df)
#         ):

#             # Excel row starts from 2 because row 1 is header
#             excel_row = row_number + 2

            
#         # =================================================
#         # O - KEY
#         #
#         # Excel:
#         # =CONCATENATE(J2,L2,M2,N2)
#         # =================================================

#         if "KEY" in column_numbers:

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["KEY"],
#                 f'=CONCATENATE(J{excel_row},L{excel_row},M{excel_row},N{excel_row})',
#                 normal_format
#             )


#         # =================================================
#         # SAME
#         #
#         # Excel:
#         # =COUNTIF(O:O,O2)
#         # =================================================

#         if "SAME" in column_numbers:

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["SAME"],
#                 f'=COUNTIF(O:O,O{excel_row})',
#                 normal_format
#             )
                    


#             # =================================================
#             # U - TOTAL AMT
#             #
#             # Excel:
#             # =ROUND((T2*K2),2)
#             # =================================================

#             if "TOTAL AMT" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["TOTAL AMT"],
#                     f'=ROUND((T{excel_row}*K{excel_row}),2)',
#                     number_format
#                 )


#             # =================================================
#             # W - VDB AMOUNT INDIA
#             #
#             # Excel:
#             # =ROUND((V2*K2),2)
#             # =================================================

#             if "VDB AMOUNT INDIA" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["VDB AMOUNT INDIA"],
#                     f'=ROUND((V{excel_row}*K{excel_row}),2)',
#                     number_format
#                 )


#             # =================================================
#             # Y - VDB AMOUNT USA
#             #
#             # Excel:
#             # =ROUND((X2*K2),2)
#             # =================================================

#             if "VDB AMOUNT USA" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["VDB AMOUNT USA"],
#                     f'=ROUND((X{excel_row}*K{excel_row}),2)',
#                     number_format
#                 )


#             # =================================================
#             # Z - WITH TARIFF COST
#             #
#             # Excel:
#             # =ROUND((T2*1.08),2)
#             # =================================================

#             if "WITH TARIFF COST" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["WITH TARIFF COST"],
#                     f'=ROUND((T{excel_row}*1.08),2)',
#                     number_format
#                 )


#             # =================================================
#             # AA - WITH TARIFF AMOUNT
#             #
#             # Excel:
#             # =ROUND((Z2*K2),2)
#             # =================================================

#             if "WITH TARIFF AMOUNT" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["WITH TARIFF AMOUNT"],
#                     f'=ROUND((Z{excel_row}*K{excel_row}),2)',
#                     number_format
#                 )


#             # =================================================
#             # AB - IND%
#             #
#             # Excel:
#             # =ROUND((100-(T2*100)/V2),2)
#             #
#             # IFERROR added to avoid #DIV/0!
#             # =================================================

#             if "IND%" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["IND%"],
#                     f'=IFERROR(ROUND((100-(T{excel_row}*100)/V{excel_row}),2),"")',
#                     percent_format
#                 )


#             # =================================================
#             # AC - USA%
#             #
#             # Excel:
#             # =ROUND((100-(Z2*100)/X2),2)
#             #
#             # IFERROR added to avoid #DIV/0!
#             # =================================================

#             if "USA%" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["USA%"],
#                     f'=IFERROR(ROUND((100-(Z{excel_row}*100)/X{excel_row}),2),"")',
#                     percent_format
#                 )


#             # =================================================
#             # AD - AFTER TARIFF DIFF$
#             #
#             # Excel:
#             # =X2-Z2
#             # =================================================

#             if "AFTER TARIFF DIFF$" in column_numbers:

#                 worksheet.write_formula(
#                     row_number + 1,
#                     column_numbers["AFTER TARIFF DIFF$"],
#                     f'=X{excel_row}-Z{excel_row}',
#                     number_format
#                 )


#         # ====================================================
#         # COLUMN WIDTHS
#         # ====================================================

#         for col_number, column in enumerate(
#             df.columns
#         ):

#             max_length = len(
#                 str(column)
#             )


#             if len(df) > 0:

#                 sample = df[
#                     column
#                 ].head(100)


#                 for value in sample:

#                     if pd.notna(value):

#                         max_length = max(
#                             max_length,
#                             len(str(value))
#                         )


#             worksheet.set_column(
#                 col_number,
#                 col_number,
#                 min(
#                     max(max_length + 2, 12),
#                     35
#                 )
#             )


#         # ====================================================
#         # FREEZE HEADER
#         # ====================================================

#         worksheet.freeze_panes(
#             1,
#             0
#         )


#         # ====================================================
#         # FILTER
#         # ====================================================

#         if len(df.columns) > 0:

#             worksheet.autofilter(
#                 0,
#                 0,
#                 len(df),
#                 len(df.columns) - 1
#             )


#         # ====================================================
#         # SET CALCULATION MODE
#         # ====================================================
#         # Excel will recalculate formulas when the file opens.

#         workbook.set_calc_mode("auto")


#     # ========================================================
#     # RETURN FILE
#     # ========================================================

#     output.seek(0)

#     return output
# def create_download_excel(df):
#     """
#     Create downloadable Excel file with actual Excel formulas.
#     """

#     output = BytesIO()

#     # Make a copy so original dataframe is not changed
#     df = df.copy()

#     # ====================================================
#     # MAKE SURE FORMULA COLUMNS EXIST
#     # ====================================================

#     formula_columns = [
#         "KEY",
#         "TOTAL AMT",
#         "VDB AMOUNT INDIA",
#         "VDB AMOUNT USA",
#         "WITH TARIFF COST",
#         "WITH TARIFF AMOUNT",
#         "IND%",
#         "USA%",
#         "AFTER TARIFF DIFF$",
#         "SAME"
#     ]

#     for column in formula_columns:

#         if column not in df.columns:
#             df[column] = ""


#     # ====================================================
#     # WRITE EXCEL
#     # ====================================================

#     with pd.ExcelWriter(
#         output,
#         engine="xlsxwriter"
#     ) as writer:

#         df.to_excel(
#             writer,
#             index=False,
#             sheet_name="Final File"
#         )

#         workbook = writer.book
#         worksheet = writer.sheets["Final File"]


#         # ====================================================
#         # FORMATS
#         # ====================================================

#         header_format = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True
#         })

#         normal_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter"
#         })

#         number_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0.00"
#         })

#         percent_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0.00"
#         })

#         date_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "dd-mm-yyyy"
#         })


#         # ====================================================
#         # COLUMN NUMBERS
#         # ====================================================

#         column_numbers = {
#             str(column).strip(): index
#             for index, column in enumerate(df.columns)
#         }


#         # ====================================================
#         # HEADER
#         # ====================================================

#         for col_number, column in enumerate(df.columns):

#             worksheet.write(
#                 0,
#                 col_number,
#                 column,
#                 header_format
#             )


#         # ====================================================
#         # FORMULA COLUMNS
#         # ====================================================

#         formula_columns = [
#             "KEY",
#             "TOTAL AMT",
#             "VDB AMOUNT INDIA",
#             "VDB AMOUNT USA",
#             "WITH TARIFF COST",
#             "WITH TARIFF AMOUNT",
#             "IND%",
#             "USA%",
#             "AFTER TARIFF DIFF$",
#             "SAME"
#         ]


#         # ====================================================
#         # WRITE NORMAL DATA
#         # ====================================================

#         for row_number in range(len(df)):

#             for col_number, column in enumerate(df.columns):

#                 column_name = str(column).strip()

#                 # Skip formula columns
#                 if column_name in formula_columns:
#                     continue

#                 value = df.iloc[
#                     row_number,
#                     col_number
#                 ]

#                 if pd.isna(value):
#                     value = ""

#                 if column_name == "DATE":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         date_format
#                     )

#                 else:

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         normal_format
#                     )


#         # ====================================================
#         # WRITE FORMULAS
#         # ====================================================

#         for row_number in range(len(df)):

#             excel_row = row_number + 2


#             # =================================================
#             # KEY
#             #
#             # =CONCATENATE(J2,L2,M2,N2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["KEY"],
#                 f'=CONCATENATE(J{excel_row},L{excel_row},M{excel_row},N{excel_row})',
#                 normal_format
#             )


#             # =================================================
#             # SAME
#             #
#             # =COUNTIF(O:O,O2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["SAME"],
#                 f'=COUNTIF(O:O,O{excel_row})',
#                 normal_format
#             )


#             # =================================================
#             # TOTAL AMT
#             #
#             # =ROUND((T2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["TOTAL AMT"],
#                 f'=ROUND((T{excel_row}*K{excel_row}),2)',
#                 number_format
#             )


#             # =================================================
#             # VDB AMOUNT INDIA
#             #
#             # =ROUND((V2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["VDB AMOUNT INDIA"],
#                 f'=ROUND((V{excel_row}*K{excel_row}),2)',
#                 number_format
#             )


#             # =================================================
#             # VDB AMOUNT USA
#             #
#             # =ROUND((X2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["VDB AMOUNT USA"],
#                 f'=ROUND((X{excel_row}*K{excel_row}),2)',
#                 number_format
#             )


#             # =================================================
#             # WITH TARIFF COST
#             #
#             # =ROUND((T2*1.08),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["WITH TARIFF COST"],
#                 f'=ROUND((T{excel_row}*1.08),2)',
#                 number_format
#             )


#             # =================================================
#             # WITH TARIFF AMOUNT
#             #
#             # =ROUND((Z2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["WITH TARIFF AMOUNT"],
#                 f'=ROUND((Z{excel_row}*K{excel_row}),2)',
#                 number_format
#             )


#             # =================================================
#             # INDIA %
#             #
#             # =ROUND((100-(T2*100)/V2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["IND%"],
#                 f'=IFERROR(ROUND((100-(T{excel_row}*100)/V{excel_row}),2),"")',
#                 percent_format
#             )


#             # =================================================
#             # USA %
#             #
#             # =ROUND((100-(Z2*100)/X2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["USA%"],
#                 f'=IFERROR(ROUND((100-(Z{excel_row}*100)/X{excel_row}),2),"")',
#                 percent_format
#             )


#             # =================================================
#             # AFTER TARIFF DIFF$
#             #
#             # =X2-Z2
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["AFTER TARIFF DIFF$"],
#                 f'=X{excel_row}-Z{excel_row}',
#                 number_format
#             )


#         # ====================================================
#         # COLUMN WIDTH
#         # ====================================================

#         for col_number, column in enumerate(df.columns):

#             max_length = len(
#                 str(column)
#             )

#             if len(df) > 0:

#                 sample = df[column].head(100)

#                 for value in sample:

#                     if pd.notna(value):

#                         max_length = max(
#                             max_length,
#                             len(str(value))
#                         )

#             worksheet.set_column(
#                 col_number,
#                 col_number,
#                 min(
#                     max(max_length + 2, 12),
#                     35
#                 )
#             )


#         # ====================================================
#         # FREEZE HEADER
#         # ====================================================

#         worksheet.freeze_panes(
#             1,
#             0
#         )


#         # ====================================================
#         # FILTER
#         # ====================================================

#         if len(df.columns) > 0:

#             worksheet.autofilter(
#                 0,
#                 0,
#                 len(df),
#                 len(df.columns) - 1
#             )


#         # ====================================================
#         # EXCEL CALCULATION MODE
#         # ====================================================

#         workbook.set_calc_mode("auto")


#     # ====================================================
#     # RETURN FILE
#     # ====================================================

#     output.seek(0)

#     return output

# # ============================================================
# # TITLE
# # ============================================================

# st.title(
#     "💎 Company Standard Format Converter"
# )

# st.caption(
#     "Convert different Party Excel Formats into Company Standard Format"
# )


# # ============================================================
# # STEP 1 — UPLOAD FILES
# # ============================================================

# st.header("1️⃣ Upload Files")


# col1, col2 = st.columns(2)


# with col1:

#     company_file = st.file_uploader(
#         "Company Standard Format",
#         type=["xlsx", "xls"],
#         key="company_file"
#     )


# with col2:

#     master_file = st.file_uploader(
#         "Master Report",
#         type=["xlsx", "xls"],
#         key="master_file"
#     )


# party_files = st.file_uploader(
#     "Party Files",
#     type=["xlsx", "xls"],
#     accept_multiple_files=True,
#     key="party_files"
# )


# # ============================================================
# # CHECK UPLOAD
# # ============================================================

# if company_file is None:

#     st.info(
#         "Please upload Company Standard Format."
#     )

#     st.stop()


# if master_file is None:

#     st.info(
#         "Please upload Master Report."
#     )

#     st.stop()


# if not party_files:

#     st.info(
#         "Please upload at least one Party File."
#     )

#     st.stop()


# # ============================================================
# # READ COMPANY FORMAT
# # ============================================================

# try:

#     company_df = read_excel(
#         company_file
#     )

# except Exception as e:

#     st.error(
#         f"Unable to read Company Standard Format: {e}"
#     )

#     st.stop()


# # ============================================================
# # VALIDATE COMPANY FORMAT
# # ============================================================

# missing_company_columns = validate_company_format(
#     company_df.columns
# )


# if missing_company_columns:

#     st.error(
#         "Your Company Standard Format is missing required columns:"
#     )

#     for column in missing_company_columns:

#         st.write(
#             f"❌ {column}"
#         )

#     st.stop()


# # ============================================================
# # READ MASTER
# # ============================================================

# try:

#     master_df = read_excel(
#         master_file
#     )

# except Exception as e:

#     st.error(
#         f"Unable to read Master Report: {e}"
#     )

#     st.stop()


# # ============================================================
# # SHOW COMPANY FORMAT
# # ============================================================

# st.divider()

# st.header(
#     "🏢 Company Standard Format"
# )

# st.success(
#     f"Company Format validated successfully — "
#     f"{len(company_df.columns)} columns found."
# )


# with st.expander(
#     "👁️ Preview Company Standard Format",
#     expanded=False
# ):

#     st.dataframe(
#         company_df.head(10),
#         use_container_width=True
#     )


# # ============================================================
# # SHOW MASTER REPORT
# # ============================================================

# with st.expander(
#     "📊 Master Report Preview",
#     expanded=False
# ):

#     st.write(
#         f"Rows: **{len(master_df)}**"
#     )

#     st.write(
#         f"Columns: **{len(master_df.columns)}**"
#     )

#     st.dataframe(
#         master_df.head(20),
#         use_container_width=True
#     )


# # ============================================================
# # STEP 2 — A-E USER INFORMATION
# # ============================================================

# st.divider()

# st.header(
#     "2️⃣ Enter File Information"
# )

# st.info(
#     "These five values will be automatically filled "
#     "in Columns A–E for every Party File."
# )


# info_col1, info_col2 = st.columns(2)


# with info_col1:

#     selection_done_by = st.text_input(
#         "A — SELECTION DONE BY",
#         placeholder="Enter person name",
#         key="selection_done_by"
#     )


#     india_price_filled_by = st.text_input(
#         "B — INDIA PRICE FILLED BY",
#         placeholder="Enter person name",
#         key="india_price_filled_by"
#     )


#     usa_price_filled_by = st.text_input(
#         "C — USA PRICE FILLED BY",
#         placeholder="Enter person name",
#         key="usa_price_filled_by"
#     )


# with info_col2:

#     final_file_by = st.text_input(
#         "D — FINAL THIS FILE BY",
#         placeholder="Enter person name",
#         key="final_file_by"
#     )


#     selected_date = st.date_input(
#         "E — DATE",
#         value=date.today(),
#         key="selected_date"
#     )


# # ============================================================
# # VALIDATE A-E
# # ============================================================

# user_information_complete = all(
#     [
#         selection_done_by.strip(),
#         india_price_filled_by.strip(),
#         usa_price_filled_by.strip(),
#         final_file_by.strip(),
#         selected_date
#     ]
# )


# if not user_information_complete:

#     st.warning(
#         "Please fill all five fields before converting Party Files."
#     )


# # ============================================================
# # STEP 3 — PARTY FILE MAPPING
# # ============================================================

# st.divider()

# st.header(
#     "3️⃣ Party File Column Mapping"
# )

# st.info(
#     "Every Party can have different column names. "
#     "Map each Party File separately."
# )


# # ============================================================
# # CLEAR OLD OUTPUT
# # ============================================================

# if st.button(
#     "🔄 Reset Converted Files"
# ):

#     st.session_state.converted_files = {}

#     st.rerun()


# # ============================================================
# # PROCESS PARTY FILES
# # ============================================================

# for file_index, party_file in enumerate(
#     party_files
# ):

#     st.divider()

#     st.subheader(
#         f"📁 Party File {file_index + 1}: "
#         f"{party_file.name}"
#     )


#     # --------------------------------------------------------
#     # READ PARTY FILE
#     # --------------------------------------------------------

#     try:

#         party_df = read_excel(
#             party_file
#         )

#     except Exception as e:

#         st.error(
#             f"Unable to read {party_file.name}: {e}"
#         )

#         continue


#     party_columns = list(
#         party_df.columns
#     )


#     # --------------------------------------------------------
#     # PARTY NAME
#     # --------------------------------------------------------

#     party_name = st.text_input(
#         "PARTY NAME",
#         placeholder="Enter Party Name",
#         key=f"party_name_{file_index}"
#     )


#     # --------------------------------------------------------
#     # PREVIEW
#     # --------------------------------------------------------

#     with st.expander(
#         "👁️ Preview Party File",
#         expanded=False
#     ):

#         st.write(
#             f"Rows: **{len(party_df)}**"
#         )

#         st.write(
#             f"Columns: **{len(party_columns)}**"
#         )

#         st.dataframe(
#             party_df.head(15),
#             use_container_width=True
#         )


#     # --------------------------------------------------------
#     # MAPPING
#     # --------------------------------------------------------

#     st.markdown(
#         "### 🔗 Select Party Columns"
#     )


#     mapping = {}


#     left_col, right_col = st.columns(2)


#     for field_index, field in enumerate(
#         PARTY_FIELDS
#     ):

#         container = (
#             left_col
#             if field_index % 2 == 0
#             else right_col
#         )


#         with container:

#             mapping[field] = st.selectbox(
#                 f"{field}",
#                 options=[
#                     "-- Select Party Column --"
#                 ] + party_columns,
#                 key=(
#                     f"mapping_"
#                     f"{file_index}_"
#                     f"{field_index}"
#                 )
#             )


#     # --------------------------------------------------------
#     # MAPPING STATUS
#     # --------------------------------------------------------

#     missing_mapping = [
#         field
#         for field, column in mapping.items()
#         if column == "-- Select Party Column --"
#     ]


#     if missing_mapping:

#         st.warning(
#             f"{len(missing_mapping)} field(s) "
#             "still need mapping."
#         )

#     else:

#         st.success(
#             "✅ All Party Columns Mapped"
#         )


#     # --------------------------------------------------------
#     # CONVERT BUTTON
#     # --------------------------------------------------------

#     convert_button = st.button(
#         "🚀 Convert This Party File",
#         key=f"convert_{file_index}",
#         type="primary"
#     )


#     if convert_button:

#         # ====================================================
#         # VALIDATION
#         # ====================================================

#         errors = []


#         if not selection_done_by.strip():

#             errors.append(
#                 "A — SELECTION DONE BY is required."
#             )


#         if not india_price_filled_by.strip():

#             errors.append(
#                 "B — INDIA PRICE FILLED BY is required."
#             )


#         if not usa_price_filled_by.strip():

#             errors.append(
#                 "C — USA PRICE FILLED BY is required."
#             )


#         if not final_file_by.strip():

#             errors.append(
#                 "D — FINAL THIS FILE BY is required."
#             )


#         if not party_name.strip():

#             errors.append(
#                 "PARTY NAME is required."
#             )


#         if missing_mapping:

#             errors.append(
#                 "All Party Columns must be mapped."
#             )


#         if errors:

#             st.error(
#                 "Please fix the following:"
#             )

#             for error in errors:

#                 st.write(
#                     f"❌ {error}"
#                 )

#             continue


#         # ====================================================
#         # CREATE OUTPUT
#         # ====================================================

#         output_df = convert_party_file(
#             party_df=party_df,
#             master_df=master_df, 
#             mapping=mapping,
#             party_name=party_name,
#             selection_done_by=selection_done_by,
#             india_price_filled_by=india_price_filled_by,
#             usa_price_filled_by=usa_price_filled_by,
#             final_file_by=final_file_by,
#             selected_date=selected_date
#         )

       


#         # ====================================================
#         # SAVE TO SESSION
#         # ====================================================

#         st.session_state.converted_files[
#             file_index
#         ] = {
#             "file_name": party_file.name,
#             "party_name": party_name,
#             "data": output_df
#         }


#         # ====================================================
#         # SUCCESS
#         # ====================================================

#         st.success(
#             f"✅ {party_file.name} converted successfully."
#         )


#         # ====================================================
#         # PREVIEW
#         # ====================================================

#         with st.expander(
#             "📊 Converted Data Preview",
#             expanded=True
#         ):

#             st.dataframe(
#                 output_df.head(20),
#                 use_container_width=True
#             )


# # ============================================================
# # FINAL COMBINATION
# # ============================================================

# if st.session_state.converted_files:

#     st.divider()

#     st.header(
#         "4️⃣ Final Company Standard File"
#     )


#     converted_data = [
#         item["data"]
#         for item in
#         st.session_state.converted_files.values()
#     ]


#     final_df = pd.concat(
#         converted_data,
#         ignore_index=True
#     )


#     # ========================================================
#     # EXACT COMPANY ORDER
#     # ========================================================

#     final_df = final_df[
#         COMPANY_COLUMNS
#     ]


#     # ========================================================
#     # SUMMARY
#     # ========================================================

#     summary_col1, summary_col2 = st.columns(2)


#     with summary_col1:

#         st.metric(
#             "Party Files Converted",
#             len(converted_data)
#         )


#     with summary_col2:

#         st.metric(
#             "Total Stones",
#             len(final_df)
#         )


#     # ========================================================
#     # FINAL PREVIEW
#     # ========================================================

#     st.subheader(
#         "📋 Final Preview"
#     )

#     st.dataframe(
#         final_df,
#         use_container_width=True,
#         height=500
#     )



  

#     # ========================================================
#     # DOWNLOAD
#     # ========================================================

#     excel_data = create_download_excel(
#         final_df
#     )


#     st.download_button(
#         label="⬇️ Download Company Standard File",
#         data=excel_data,
#         file_name=(
#             "Company_Standard_Final.xlsx"
#         ),
#         mime=(
#             "application/vnd.openxmlformats-officedocument."
#             "spreadsheetml.sheet"
#         ),
#         type="primary",
#         use_container_width=True
#     )












# import streamlit as st
# import pandas as pd
# from io import BytesIO
# from datetime import date


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Company Standard Format",
#     page_icon="💎",
#     layout="wide"
# )


# # ============================================================
# # COMPANY STANDARD COLUMNS
# # ============================================================

# COMPANY_COLUMNS = [

#     "SELECTION DONE BY",

#     "INDIA PRICE FILLED BY",

#     "USA PRICE FILLED BY",

#     "FINAL THIS FILE BY",

#     "DATE",

#     "STONE ID",

#     "PARTY NAME",

#     "REPORT NO.",

#     "GROWTH TYPE",

#     "SHAPE",

#     "CTS",

#     "SIZE GROUP",

#     "COLOR",

#     "CLARITY",

#     "KEY",

#     "GRID",

#     "AVAILABLE",

#     "SAME",

#     "REMARK",

#     "PER CARAT",

#     "TOTAL AMT",

#     "VDB PRICE INDIA",

#     "VDB AMOUNT INDIA",

#     "VDB PRICE USA",

#     "VDB AMOUNT USA",

#     "WITH TARIFF COST",

#     "WITH TARIFF AMOUNT",

#     "IND%",

#     "USA%",

#     "AFTER TARIFF DIFF$"
# ]


# # ============================================================
# # PARTY FIELDS USER MUST MAP
# # ============================================================

# PARTY_FIELDS = [
#     "STONE ID",
#     "REPORT NO.",
#     "GROWTH TYPE",
#     "SHAPE",
#     "CTS",
#     "COLOR",
#     "CLARITY",
#     "PER CARAT",
#     "VDB PRICE INDIA",
#     "VDB PRICE USA"
# ]


# # ============================================================
# # PARTY FIELD → COMPANY COLUMN
# # ============================================================

# FIELD_TO_COMPANY_COLUMN = {

#     "STONE ID": "STONE ID",

#     "REPORT NO.": "REPORT NO.",

#     "GROWTH TYPE": "GROWTH TYPE",

#     "SHAPE": "SHAPE",

#     "CTS": "CTS",

#     "COLOR": "COLOR",

#     "CLARITY": "CLARITY",

#     "PER CARAT": "PER CARAT",

#     "VDB PRICE INDIA": "VDB PRICE INDIA",

#     "VDB PRICE USA": "VDB PRICE USA"
# }


# # ============================================================
# # SESSION STATE
# # ============================================================

# if "converted_files" not in st.session_state:

#     st.session_state.converted_files = {}


# # ============================================================
# # NORMALIZE COLUMN NAME
# # ============================================================
# def normalize_column_name(value):
#     """
#     Normalize Excel column names.

#     Removes:
#     - Leading spaces
#     - Trailing spaces
#     - Multiple spaces
#     - New lines

#     Makes comparison case-insensitive.
#     """

#     if value is None:
#         return ""

#     value = str(value)

#     value = value.replace("\n", " ")

#     # Convert multiple spaces into one
#     value = " ".join(
#         value.split()
#     )

#     return value.strip().upper()


# def validate_company_format(columns):

#     # Normalize actual Excel headers
#     actual_columns = {
#         normalize_column_name(column): column
#         for column in columns
#     }

#     missing = []

#     for required_column in COMPANY_COLUMNS:

#         normalized_required = (
#             normalize_column_name(
#                 required_column
#             )
#         )

#         if normalized_required not in actual_columns:

#             missing.append(
#                 required_column
#             )

#     return missing
# def normalize_column_name(value):

#     if value is None:

#         return ""

#     return (
#         str(value)
#         .strip()
#         .upper()
#         .replace("\n", " ")
#         .replace("_", " ")
#     )


# # ============================================================
# # FIND ACTUAL COLUMN
# # ============================================================

# def find_column(df, wanted_name):

#     wanted = normalize_column_name(
#         wanted_name
#     )

#     for column in df.columns:

#         if normalize_column_name(column) == wanted:

#             return column

#     return None


# # ============================================================
# # READ EXCEL
# # ============================================================

# def read_excel(file):

#     file.seek(0)

#     return pd.read_excel(
#         file,
#         engine="openpyxl"
#     )


# # ============================================================
# # SIZE GROUP
# # ============================================================

# def get_size_group(cts):
#     """
#     Calculate Size Group from CTS.
#     """

#     if pd.isna(cts):

#         return ""

#     try:

#         cts = float(cts)

#     except (ValueError, TypeError):

#         return ""


#     # --------------------------------------------------------
#     # Below 0.30
#     # --------------------------------------------------------

#     if cts < 0.30:

#         return ""


#     # --------------------------------------------------------
#     # 0.30 - 0.50
#     # --------------------------------------------------------

#     if cts <= 0.50:

#         return "0.30 - 0.50"


#     # --------------------------------------------------------
#     # 0.50 - 0.59
#     # --------------------------------------------------------

#     if cts <= 0.59:

#         return "0.50 - 0.59"


#     # --------------------------------------------------------
#     # 0.60 - 0.69
#     # --------------------------------------------------------

#     if cts <= 0.69:

#         return "0.60 - 0.69"


#     # --------------------------------------------------------
#     # 0.70 - 0.79
#     # --------------------------------------------------------

#     if cts <= 0.79:

#         return "0.70 - 0.79"


#     # --------------------------------------------------------
#     # 0.80 - 0.89
#     # --------------------------------------------------------

#     if cts <= 0.89:

#         return "0.80 - 0.89"


#     # --------------------------------------------------------
#     # 0.90 - 0.94
#     # --------------------------------------------------------

#     if cts <= 0.94:

#         return "0.90 - 0.94"


#     # --------------------------------------------------------
#     # 0.95 - 0.99
#     # --------------------------------------------------------

#     if cts <= 0.99:

#         return "0.95 - 0.99"


#     # --------------------------------------------------------
#     # 1.00 - 1.10
#     # --------------------------------------------------------

#     if cts <= 1.10:

#         return "1.00 - 1.10"


#     # --------------------------------------------------------
#     # 1.11 - 1.19
#     # --------------------------------------------------------

#     if cts <= 1.19:

#         return "1.11 - 1.19"


#     # --------------------------------------------------------
#     # 1.20 - 1.29
#     # --------------------------------------------------------

#     if cts <= 1.29:

#         return "1.20 - 1.29"


#     # --------------------------------------------------------
#     # 1.30 - 1.39
#     # --------------------------------------------------------

#     if cts <= 1.39:

#         return "1.30 - 1.39"


#     # --------------------------------------------------------
#     # 1.40 - 1.49
#     # --------------------------------------------------------

#     if cts <= 1.49:

#         return "1.40 - 1.49"


#     # --------------------------------------------------------
#     # 1.50 - 3.99
#     # --------------------------------------------------------

#     if cts < 4.00:

#         lower = int(cts * 10) / 10

#         upper = lower + 0.09

#         return (
#             f"{lower:.2f} - {upper:.2f}"
#         )


#     # --------------------------------------------------------
#     # 4.00 - 4.10
#     # --------------------------------------------------------

#     if cts <= 4.10:

#         return "4.00 - 4.10"


#     # --------------------------------------------------------
#     # 4.11 - 4.49
#     # --------------------------------------------------------

#     if cts < 4.50:

#         return "4.11 - 4.49"


#     # --------------------------------------------------------
#     # 4.50 - 4.59
#     # --------------------------------------------------------

#     if cts <= 4.59:

#         return "4.50 - 4.59"


#     # --------------------------------------------------------
#     # 4.60 - 4.99
#     # --------------------------------------------------------

#     if cts < 5.00:

#         return "4.60 - 4.99"


#     # --------------------------------------------------------
#     # 5.00 - 5.59
#     # --------------------------------------------------------

#     if cts <= 5.59:

#         return "5.00 - 5.59"


#     # --------------------------------------------------------
#     # 5.60 - 5.99
#     # --------------------------------------------------------

#     if cts < 6.00:

#         return "5.60 - 5.99"


#     # --------------------------------------------------------
#     # 6.00 - 6.99
#     # --------------------------------------------------------

#     if cts < 7.00:

#         return "6.00 - 6.99"


#     # --------------------------------------------------------
#     # 7 CTS onwards
#     # --------------------------------------------------------

#     whole = int(cts)

#     decimal = cts - whole


#     if decimal <= 0.10:

#         return (
#             f"{whole:.2f} - "
#             f"{whole + 0.10:.2f}"
#         )


#     return (
#         f"{whole + 0.11:.2f} - "
#         f"{whole + 0.99:.2f}"
#     )


# # ============================================================
# # VALIDATE COMPANY FORMAT
# # ============================================================

# def validate_company_format(columns):

#     actual = [
#         normalize_column_name(column)
#         for column in columns
#     ]

#     required = [
#         normalize_column_name(column)
#         for column in COMPANY_COLUMNS
#     ]

#     missing = []

#     for column in required:

#         if column not in actual:

#             missing.append(column)

#     return missing


# # ============================================================
# # CREATE BLANK OUTPUT
# # ============================================================

# def create_blank_output(number_of_rows):

#     return pd.DataFrame(
#         "",
#         index=range(number_of_rows),
#         columns=COMPANY_COLUMNS
#     )


# # ============================================================
# # CONVERT PARTY FILE
# # ============================================================

# def convert_party_file(
#     party_df,
#     master_df,
#     mapping,
#     party_name,
#     selection_done_by,
#     india_price_filled_by,
#     usa_price_filled_by,
#     final_file_by,
#     selected_date
# ):
#     """
#     Convert Party File into Company Standard Format.

#     IMPORTANT:
#     Party File does NOT contain KEY.

#     KEY is created after converting the Party
#     columns into Company Standard Format.

#     KEY =
#         SHAPE
#         + SIZE GROUP
#         + COLOR
#         + CLARITY

#     Then KEY is matched with Master File
#     to get GRID and AVAILABLE.
#     """


#     # ========================================================
#     # CREATE OUTPUT
#     # ========================================================

#     output = create_blank_output(
#         len(party_df)
#     )


#     # ========================================================
#     # USER ENTERED INFORMATION
#     # ========================================================

#     output["SELECTION DONE BY"] = (
#         selection_done_by
#     )

#     output["INDIA PRICE FILLED BY"] = (
#         india_price_filled_by
#     )

#     output["USA PRICE FILLED BY"] = (
#         usa_price_filled_by
#     )

#     output["FINAL THIS FILE BY"] = (
#         final_file_by
#     )

#     output["DATE"] = selected_date


#     # ========================================================
#     # PARTY NAME
#     # ========================================================

#     output["PARTY NAME"] = party_name


#     # ========================================================
#     # PARTY COLUMN MAPPING
#     # ========================================================

#     for party_field, party_column in mapping.items():

#         if party_column is None:

#             continue

#         if party_column == "-- Select Party Column --":

#             continue

#         if party_column not in party_df.columns:

#             continue

#         company_column = (
#             FIELD_TO_COMPANY_COLUMN[
#                 party_field
#             ]
#         )

#         output[company_column] = (
#             party_df[party_column]
#             .reset_index(drop=True)
#         )


#     # ========================================================
#     # SIZE GROUP
#     # ========================================================

#     output["SIZE GROUP"] = (
#         output["CTS"].apply(
#             get_size_group
#         )
#     )


#     # ========================================================
#     # CLEAN KEY FIELDS
#     # ========================================================

#     key_columns = [
#         "SHAPE",
#         "SIZE GROUP",
#         "COLOR",
#         "CLARITY"
#     ]


#     for column in key_columns:

#         output[column] = (
#             output[column]
#             .fillna("")
#             .astype(str)
#             .str.strip()
#         )


#     # ========================================================
#     # CREATE KEY
#     #
#     # Shape + Size Group + Color + Clarity
#     #
#     # PARTY FILE DOES NOT NEED KEY
#     # ========================================================

#     output["KEY"] = (
#         output["SHAPE"]
#         + output["SIZE GROUP"]
#         + output["COLOR"]
#         + output["CLARITY"]
#     )


#     # ========================================================
#     # PREPARE MASTER FILE
#     # ========================================================

#     master = master_df.copy()


#     # ========================================================
#     # FIND MASTER KEY COLUMN
#     # ========================================================

#     master_key_column = find_column(
#         master,
#         "KEY"
#     )


#     if master_key_column is None:

#         raise ValueError(
#             "Master File does not contain a KEY column."
#         )


#     # ========================================================
#     # FIND MASTER GRID COLUMN
#     # ========================================================

#     master_grid_column = find_column(
#         master,
#         "GRID"
#     )


#     if master_grid_column is None:

#         raise ValueError(
#             "Master File does not contain a Grid column."
#         )


#     # ========================================================
#     # FIND MASTER AVAILABLE COLUMN
#     # ========================================================

#     master_available_column = find_column(
#         master,
#         "AVAILABLE"
#     )


#     if master_available_column is None:

#         raise ValueError(
#             "Master File does not contain an Available column."
#         )


#     # ========================================================
#     # CREATE MASTER LOOKUP
#     # ========================================================

#     master_lookup = master[
#         [
#             master_key_column,
#             master_grid_column,
#             master_available_column
#         ]
#     ].copy()


#     # ========================================================
#     # STANDARD MASTER COLUMN NAMES
#     # ========================================================

#     master_lookup.columns = [
#         "MASTER_KEY",
#         "MASTER_GRID",
#         "MASTER_AVAILABLE"
#     ]


#     # ========================================================
#     # CLEAN MASTER KEY
#     # ========================================================

#     master_lookup["MASTER_KEY"] = (
#         master_lookup["MASTER_KEY"]
#         .fillna("")
#         .astype(str)
#         .str.strip()
#     )


#     # ========================================================
#     # CONVERT MASTER GRID TO NUMBER
#     # ========================================================

#     master_lookup["MASTER_GRID"] = (
#         pd.to_numeric(
#             master_lookup["MASTER_GRID"],
#             errors="coerce"
#         )
#         .fillna(0)
#     )


#     # ========================================================
#     # CONVERT MASTER AVAILABLE TO NUMBER
#     # ========================================================

#     master_lookup["MASTER_AVAILABLE"] = (
#         pd.to_numeric(
#             master_lookup["MASTER_AVAILABLE"],
#             errors="coerce"
#         )
#         .fillna(0)
#     )


#     # ========================================================
#     # REMOVE DUPLICATE MASTER KEYS
#     # ========================================================

#     master_lookup = (
#         master_lookup
#         .drop_duplicates(
#             subset=["MASTER_KEY"],
#             keep="first"
#         )
#     )


#     # ========================================================
#     # MATCH COMPANY KEY WITH MASTER KEY
#     # ========================================================

#     output = output.merge(
#         master_lookup,
#         left_on="KEY",
#         right_on="MASTER_KEY",
#         how="left"
#     )


#     # ========================================================
#     # GRID
#     #
#     # DIRECT NUMBER FROM MASTER
#     # NOT EXCEL FORMULA
#     # ========================================================

#     output["GRID"] = (
#         pd.to_numeric(
#             output["MASTER_GRID"],
#             errors="coerce"
#         )
#         .fillna(0)
#     )


#     # ========================================================
#     # AVAILABLE
#     #
#     # DIRECT NUMBER FROM MASTER
#     # NOT EXCEL FORMULA
#     # ========================================================

#     output["AVAILABLE"] = (
#         pd.to_numeric(
#             output["MASTER_AVAILABLE"],
#             errors="coerce"
#         )
#         .fillna(0)
#     )


#     # ========================================================
#     # REMOVE TEMPORARY MASTER COLUMNS
#     # ========================================================

#     output.drop(
#         columns=[
#             "MASTER_KEY",
#             "MASTER_GRID",
#             "MASTER_AVAILABLE"
#         ],
#         inplace=True,
#         errors="ignore"
#     )


#     # ========================================================
#     # SAME
#     #
#     # Excel formula will be added during download.
#     # ========================================================

#     output["SAME"] = ""


#     # ========================================================
#     # REMARK
#     # ========================================================

#     output["REMARK"] = ""


#     # ========================================================
#     # FORMULA COLUMNS
#     # ========================================================

#     formula_columns = [

#         "TOTAL AMT",

#         "VDB AMOUNT INDIA",

#         "VDB AMOUNT USA",

#         "WITH TARIFF COST",

#         "WITH TARIFF AMOUNT",

#         "IND%",

#         "USA%",

#         "AFTER TARIFF DIFF$"
#     ]


#     for column in formula_columns:

#         output[column] = ""


#     # ========================================================
#     # FINAL COLUMN ORDER
#     # ========================================================

#     for column in COMPANY_COLUMNS:

#         if column not in output.columns:

#             output[column] = ""


#     output = output[
#         COMPANY_COLUMNS
#     ]


#     # ========================================================
#     # RESET INDEX
#     # ========================================================

#     output = output.reset_index(
#         drop=True
#     )


#     return output


# # ============================================================
# # CREATE DOWNLOAD EXCEL
# # ============================================================

# # def create_download_excel(df):
#     """
#     Create final Excel file.

#     Grid and Available are already numbers
#     from Master File.

#     Formula columns contain real Excel formulas.
#     """

#     output = BytesIO()


#     # ========================================================
#     # CLEAN COLUMN NAMES
#     # ========================================================

#     df = df.copy()

#     df.columns = [
#         str(column).strip()
#         for column in df.columns
#     ]


#     # ========================================================
#     # MAKE SURE REQUIRED COLUMNS EXIST
#     # ========================================================

#     for column in COMPANY_COLUMNS:

#         clean_column = column.strip()

#         if clean_column not in df.columns:

#             df[clean_column] = ""


#     # ========================================================
#     # FINAL COLUMN ORDER
#     # ========================================================

#     final_columns = [
#         column.strip()
#         for column in COMPANY_COLUMNS
#     ]

#     df = df[
#         final_columns
#     ]


#     # ========================================================
#     # EXCEL WRITER
#     # ========================================================

#     with pd.ExcelWriter(
#         output,
#         engine="xlsxwriter"
#     ) as writer:


#         df.to_excel(
#             writer,
#             index=False,
#             sheet_name="Final File"
#         )


#         workbook = writer.book

#         worksheet = writer.sheets[
#             "Final File"
#         ]


#         # ====================================================
#         # FORMATS
#         # ====================================================

#         header_format = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True
#         })


#         normal_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter"
#         })


#         number_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0.00"
#         })


#         integer_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0"
#         })


#         percent_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0.00"
#         })


#         date_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "dd-mm-yyyy"
#         })


#         # ====================================================
#         # COLUMN NUMBERS
#         # ====================================================

#         column_numbers = {
#             str(column).strip(): index
#             for index, column
#             in enumerate(df.columns)
#         }


#         # ====================================================
#         # HEADER
#         # ====================================================

#         for col_number, column in enumerate(
#             df.columns
#         ):

#             worksheet.write(
#                 0,
#                 col_number,
#                 column,
#                 header_format
#             )


#         # ====================================================
#         # FORMULA COLUMNS
#         # ====================================================

#         formula_columns = [

#             "KEY",

#             "SAME",

#             "TOTAL AMT",

#             "VDB AMOUNT INDIA",

#             "VDB AMOUNT USA",

#             "WITH TARIFF COST",

#             "WITH TARIFF AMOUNT",

#             "IND%",

#             "USA%",

#             "AFTER TARIFF DIFF$"
#         ]


#         # ====================================================
#         # WRITE NORMAL DATA
#         # ====================================================

#         for row_number in range(
#             len(df)
#         ):

#             for col_number, column in enumerate(
#                 df.columns
#             ):

#                 column_name = (
#                     str(column).strip()
#                 )


#                 # Skip formula columns
#                 if column_name in formula_columns:

#                     continue


#                 value = df.iloc[
#                     row_number,
#                     col_number
#                 ]


#                 if pd.isna(value):

#                     value = ""


#                 # ------------------------------------------------
#                 # DATE
#                 # ------------------------------------------------

#                 if column_name == "DATE":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         date_format
#                     )


#                 # ------------------------------------------------
#                 # GRID / AVAILABLE
#                 # ------------------------------------------------

#                 elif column_name in [
#                     "GRID",
#                     "AVAILABLE"
#                 ]:

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         integer_format
#                     )


#                 # ------------------------------------------------
#                 # NORMAL
#                 # ------------------------------------------------

#                 else:

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         normal_format
#                     )


#         # ====================================================
#         # WRITE FORMULAS
#         # ====================================================

#         for row_number in range(
#             len(df)
#         ):

#             # Excel row
#             excel_row = row_number + 2


#             # =================================================
#             # KEY
#             #
#             # O2
#             #
#             # =CONCATENATE(J2,L2,M2,N2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["KEY"],
#                 (
#                     f'=CONCATENATE('
#                     f'J{excel_row},'
#                     f'L{excel_row},'
#                     f'M{excel_row},'
#                     f'N{excel_row})'
#                 ),
#                 normal_format
#             )


#             # =================================================
#             # SAME
#             #
#             # R2
#             #
#             # =COUNTIF(O:O,O2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["SAME"],
#                 (
#                     f'=COUNTIF('
#                     f'O:O,'
#                     f'O{excel_row})'
#                 ),
#                 integer_format
#             )


#             # =================================================
#             # TOTAL AMT
#             #
#             # U2
#             #
#             # =ROUND((T2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["TOTAL AMT"],
#                 (
#                     f'=ROUND('
#                     f'(T{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 number_format
#             )


#             # =================================================
#             # VDB AMOUNT INDIA
#             #
#             # W2
#             #
#             # =ROUND((V2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["VDB AMOUNT INDIA"],
#                 (
#                     f'=ROUND('
#                     f'(V{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 number_format
#             )


#             # =================================================
#             # VDB AMOUNT USA
#             #
#             # Y2
#             #
#             # =ROUND((X2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["VDB AMOUNT USA"],
#                 (
#                     f'=ROUND('
#                     f'(X{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 number_format
#             )


#             # =================================================
#             # WITH TARIFF COST
#             #
#             # Z2
#             #
#             # =ROUND((T2*1.08),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["WITH TARIFF COST"],
#                 (
#                     f'=ROUND('
#                     f'(T{excel_row}*1.08),2)'
#                 ),
#                 number_format
#             )


#             # =================================================
#             # WITH TARIFF AMOUNT
#             #
#             # AA2
#             #
#             # =ROUND((Z2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["WITH TARIFF AMOUNT"],
#                 (
#                     f'=ROUND('
#                     f'(Z{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 number_format
#             )


#             # =================================================
#             # INDIA %
#             #
#             # AB2
#             #
#             # =ROUND((100-(T2*100)/V2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["IND%"],
#                 (
#                     f'=IFERROR('
#                     f'ROUND('
#                     f'(100-('
#                     f'T{excel_row}*100)/'
#                     f'V{excel_row}),2),'
#                     f'"")'
#                 ),
#                 percent_format
#             )


#             # =================================================
#             # USA %
#             #
#             # AC2
#             #
#             # =ROUND((100-(Z2*100)/X2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["USA%"],
#                 (
#                     f'=IFERROR('
#                     f'ROUND('
#                     f'(100-('
#                     f'Z{excel_row}*100)/'
#                     f'X{excel_row}),2),'
#                     f'"")'
#                 ),
#                 percent_format
#             )


#             # =================================================
#             # AFTER TARIFF DIFF$
#             #
#             # AD2
#             #
#             # =X2-Z2
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["AFTER TARIFF DIFF$"],
#                 (
#                     f'=X{excel_row}-'
#                     f'Z{excel_row}'
#                 ),
#                 number_format
#             )


#         # ====================================================
#         # COLUMN WIDTHS
#         # ====================================================

#         for col_number, column in enumerate(
#             df.columns
#         ):

#             max_length = len(
#                 str(column)
#             )


#             if len(df) > 0:

#                 sample = df[
#                     column
#                 ].head(100)


#                 for value in sample:

#                     if pd.notna(value):

#                         max_length = max(
#                             max_length,
#                             len(str(value))
#                         )


#             worksheet.set_column(
#                 col_number,
#                 col_number,
#                 min(
#                     max(max_length + 2, 12),
#                     35
#                 )
#             )


#         # ====================================================
#         # FREEZE HEADER
#         # ====================================================

#         worksheet.freeze_panes(
#             1,
#             0
#         )


#         # ====================================================
#         # FILTER
#         # ====================================================

#         if len(df.columns) > 0:

#             worksheet.autofilter(
#                 0,
#                 0,
#                 len(df),
#                 len(df.columns) - 1
#             )


#         # ====================================================
#         # AUTO CALCULATION
#         # ====================================================

#         workbook.set_calc_mode(
#             "auto"
#         )


#     output.seek(0)

#     return output

# def create_download_excel(df):
#     """
#     Create final Excel file.

#     Features:
#     - Keeps all existing data
#     - Keeps Excel formulas
#     - Creates KEY formula
#     - Creates SAME formula
#     - Creates amount formulas
#     - Creates tariff formulas
#     - Creates percentage formulas
#     - Creates AFTER TARIFF DIFF$ formula
#     - Highlights requested column groups
#     """

#     output = BytesIO()

#     # ========================================================
#     # COPY DATAFRAME
#     # ========================================================

#     df = df.copy()

#     # Remove accidental spaces from column names
#     df.columns = [
#         str(column).strip()
#         for column in df.columns
#     ]

#     # ========================================================
#     # REQUIRED COMPANY COLUMNS
#     # ========================================================

#     for column in COMPANY_COLUMNS:

#         clean_column = str(column).strip()

#         if clean_column not in df.columns:

#             df[clean_column] = ""

#     # ========================================================
#     # FINAL COLUMN ORDER
#     # ========================================================

#     final_columns = [
#         str(column).strip()
#         for column in COMPANY_COLUMNS
#     ]

#     df = df[
#         final_columns
#     ]

#     # ========================================================
#     # EXCEL WRITER
#     # ========================================================

#     with pd.ExcelWriter(
#         output,
#         engine="xlsxwriter"
#     ) as writer:

#         df.to_excel(
#             writer,
#             index=False,
#             sheet_name="Final File"
#         )

#         workbook = writer.book

#         worksheet = writer.sheets[
#             "Final File"
#         ]

#         # ====================================================
#         # HEADER FORMAT
#         # ====================================================

#         # ====================================================
#         # HEADER FORMATS
#         # ====================================================

#         header_format = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True
#         })


#         # ====================================================
#         # COLORED HEADER FORMATS
#         # ====================================================

#         header_size_grid_same = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True,
#             "bg_color": "#DDEBF7"
#         })


#         header_per_carat_total = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True,
#             "bg_color": "#E2F0D9"
#         })


#         header_india = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True,
#             "bg_color": "#FFF2CC"
#         })


#         header_usa = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True,
#             "bg_color": "#FCE4D6"
#         })


#         header_tariff = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True,
#             "bg_color": "#E4DFEC"
#         })


#         header_difference = workbook.add_format({
#             "bold": True,
#             "border": 1,
#             "align": "center",
#             "valign": "vcenter",
#             "text_wrap": True,
#             "bg_color": "#F4CCCC"
#         })

#         # ====================================================
#         # NORMAL FORMAT
#         # ====================================================

#         normal_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter"
#         })

#         # ====================================================
#         # NUMBER FORMAT
#         # ====================================================

#         number_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0.00"
#         })

#         # ====================================================
#         # INTEGER FORMAT
#         # ====================================================

#         integer_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "0"
#         })

#         # ====================================================
#         # DATE FORMAT
#         # ====================================================

#         date_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "num_format": "dd-mm-yyyy"
#         })

#         # ====================================================
#         # COLUMN GROUP COLORS
#         #
#         # You can change these colors later.
#         # ====================================================

#         # ----------------------------------------------------
#         # SIZE GROUP + GRID + AVAILABLE + SAME
#         # ----------------------------------------------------

#         size_grid_same_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#DDEBF7"
#         })

#         # ----------------------------------------------------
#         # PER CARAT + TOTAL AMT
#         # ----------------------------------------------------

#         per_carat_total_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#E2F0D9",
#             "num_format": "0.00"
#         })

#         # ----------------------------------------------------
#         # VDB INDIA PRICE + VDB INDIA AMOUNT
#         # ----------------------------------------------------

#         india_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#FFF2CC",
#             "num_format": "0.00"
#         })

#         # ----------------------------------------------------
#         # VDB USA PRICE + VDB USA AMOUNT
#         # ----------------------------------------------------

#         usa_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#FCE4D6",
#             "num_format": "0.00"
#         })

#         # ----------------------------------------------------
#         # WITH TARIFF COST + WITH TARIFF AMOUNT
#         # ----------------------------------------------------

#         tariff_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#E4DFEC",
#             "num_format": "0.00"
#         })

#         # ----------------------------------------------------
#         # IND% + USA% + AFTER TARIFF DIFF$
#         # ----------------------------------------------------

#         difference_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#F4CCCC",
#             "num_format": "0.00"
#         })

#         # ====================================================
#         # FORMULA FORMATS
#         # ====================================================

#         # SAME
#         same_formula_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#DDEBF7",
#             "num_format": "0"
#         })

#         # TOTAL AMT
#         total_formula_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#E2F0D9",
#             "num_format": "0.00"
#         })

#         # VDB INDIA AMOUNT
#         vdb_india_formula_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#FFF2CC",
#             "num_format": "0.00"
#         })

#         # VDB USA AMOUNT
#         vdb_usa_formula_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#FCE4D6",
#             "num_format": "0.00"
#         })

#         # TARIFF FORMULAS
#         tariff_formula_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#E4DFEC",
#             "num_format": "0.00"
#         })

#         # DIFFERENCE FORMULAS
#         difference_formula_format = workbook.add_format({
#             "border": 1,
#             "valign": "vcenter",
#             "bg_color": "#F4CCCC",
#             "num_format": "0.00"
#         })

#         # ====================================================
#         # COLUMN NUMBERS
#         # ====================================================

#         column_numbers = {
#             str(column).strip(): index
#             for index, column
#             in enumerate(df.columns)
#         }

#         # ====================================================
#         # HEADER
#         # ====================================================

#         # ====================================================
#         # HEADER
#         # ====================================================

#         for col_number, column in enumerate(
#             df.columns
#         ):

#             column_name = str(column).strip()

#             # --------------------------------------------
#             # SIZE GROUP / GRID / AVAILABLE / SAME
#             # --------------------------------------------

#             if column_name in [
#                 "SIZE GROUP",
#                 "GRID",
#                 "AVAILABLE",
#                 "SAME"
#             ]:

#                 cell_header_format = (
#                     header_size_grid_same
#                 )

#             # --------------------------------------------
#             # PER CARAT / TOTAL AMT
#             # --------------------------------------------

#             elif column_name in [
#                 "PER CARAT",
#                 "TOTAL AMT"
#             ]:

#                 cell_header_format = (
#                     header_per_carat_total
#                 )

#             # --------------------------------------------
#             # INDIA
#             # --------------------------------------------

#             elif column_name in [
#                 "VDB PRICE INDIA",
#                 "VDB AMOUNT INDIA"
#             ]:

#                 cell_header_format = (
#                     header_india
#                 )

#             # --------------------------------------------
#             # USA
#             # --------------------------------------------

#             elif column_name in [
#                 "VDB PRICE USA",
#                 "VDB AMOUNT USA"
#             ]:

#                 cell_header_format = (
#                     header_usa
#                 )

#             # --------------------------------------------
#             # TARIFF
#             # --------------------------------------------

#             elif column_name in [
#                 "WITH TARIFF COST",
#                 "WITH TARIFF AMOUNT"
#             ]:

#                 cell_header_format = (
#                     header_tariff
#                 )

#             # --------------------------------------------
#             # DIFFERENCE
#             # --------------------------------------------

#             elif column_name in [
#                 "IND%",
#                 "USA%",
#                 "AFTER TARIFF DIFF$"
#             ]:

#                 cell_header_format = (
#                     header_difference
#                 )

#             # --------------------------------------------
#             # NORMAL COLUMNS
#             # --------------------------------------------

#             else:

#                 cell_header_format = (
#                     header_format
#                 )

#             worksheet.write(
#                 0,
#                 col_number,
#                 column_name,
#                 cell_header_format
#             )

#         # ====================================================
#         # FORMULA COLUMNS
#         # ====================================================

#         formula_columns = [

#             "KEY",

#             "SAME",

#             "TOTAL AMT",

#             "VDB AMOUNT INDIA",

#             "VDB AMOUNT USA",

#             "WITH TARIFF COST",

#             "WITH TARIFF AMOUNT",

#             "IND%",

#             "USA%",

#             "AFTER TARIFF DIFF$"
#         ]

#         # ====================================================
#         # WRITE NORMAL DATA
#         # ====================================================

#         for row_number in range(
#             len(df)
#         ):

#             for col_number, column in enumerate(
#                 df.columns
#             ):

#                 column_name = (
#                     str(column).strip()
#                 )

#                 # --------------------------------------------
#                 # Formula columns are written later
#                 # --------------------------------------------

#                 if column_name in formula_columns:

#                     continue

#                 value = df.iloc[
#                     row_number,
#                     col_number
#                 ]

#                 if pd.isna(value):

#                     value = ""

#                 # --------------------------------------------
#                 # DATE
#                 # --------------------------------------------

#                 if column_name == "DATE":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         date_format
#                     )

#                 # --------------------------------------------
#                 # SIZE GROUP
#                 # --------------------------------------------

#                 elif column_name == "SIZE GROUP":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         size_grid_same_format
#                     )

#                 # --------------------------------------------
#                 # GRID / AVAILABLE
#                 # --------------------------------------------

#                 elif column_name in [
#                     "GRID",
#                     "AVAILABLE"
#                 ]:

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         size_grid_same_format
#                     )

#                 # --------------------------------------------
#                 # PER CARAT
#                 # --------------------------------------------

#                 elif column_name == "PER CARAT":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         per_carat_total_format
#                     )

#                 # --------------------------------------------
#                 # VDB INDIA PRICE
#                 # --------------------------------------------

#                 elif column_name == "VDB PRICE INDIA":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         india_format
#                     )

#                 # --------------------------------------------
#                 # VDB USA PRICE
#                 # --------------------------------------------

#                 elif column_name == "VDB PRICE USA":

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         usa_format
#                     )

#                 # --------------------------------------------
#                 # TARIFF
#                 # --------------------------------------------

#                 elif column_name in [
#                     "WITH TARIFF COST"
#                 ]:

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         tariff_format
#                     )

#                 # --------------------------------------------
#                 # NORMAL COLUMNS
#                 # --------------------------------------------

#                 else:

#                     worksheet.write(
#                         row_number + 1,
#                         col_number,
#                         value,
#                         normal_format
#                     )

#         # ====================================================
#         # WRITE FORMULAS
#         # ====================================================

#         for row_number in range(
#             len(df)
#         ):

#             # Excel row starts at 2
#             excel_row = row_number + 2

#             # =================================================
#             # KEY
#             #
#             # J = Shape
#             # L = Size Group
#             # M = Color
#             # N = Clarity
#             #
#             # O = KEY
#             #
#             # =CONCATENATE(J2,L2,M2,N2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["KEY"],
#                 (
#                     f'=CONCATENATE('
#                     f'J{excel_row},'
#                     f'L{excel_row},'
#                     f'M{excel_row},'
#                     f'N{excel_row})'
#                 ),
#                 normal_format
#             )

#             # =================================================
#             # SAME
#             #
#             # O = KEY
#             #
#             # =COUNTIF(O:O,O2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["SAME"],
#                 (
#                     f'=COUNTIF('
#                     f'O:O,'
#                     f'O{excel_row})'
#                 ),
#                 same_formula_format
#             )

#             # =================================================
#             # TOTAL AMT
#             #
#             # T = PER CARAT
#             # K = CTS
#             #
#             # =ROUND((T2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["TOTAL AMT"],
#                 (
#                     f'=ROUND('
#                     f'(T{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 total_formula_format
#             )

#             # =================================================
#             # VDB AMOUNT INDIA
#             #
#             # V = VDB PRICE INDIA
#             # K = CTS
#             #
#             # =ROUND((V2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["VDB AMOUNT INDIA"],
#                 (
#                     f'=ROUND('
#                     f'(V{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 vdb_india_formula_format
#             )

#             # =================================================
#             # VDB AMOUNT USA
#             #
#             # X = VDB PRICE USA
#             # K = CTS
#             #
#             # =ROUND((X2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["VDB AMOUNT USA"],
#                 (
#                     f'=ROUND('
#                     f'(X{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 vdb_usa_formula_format
#             )

#             # =================================================
#             # WITH TARIFF COST
#             #
#             # T = PER CARAT
#             #
#             # =ROUND((T2*1.08),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["WITH TARIFF COST"],
#                 (
#                     f'=ROUND('
#                     f'(T{excel_row}*1.08),2)'
#                 ),
#                 tariff_formula_format
#             )

#             # =================================================
#             # WITH TARIFF AMOUNT
#             #
#             # Z = WITH TARIFF COST
#             # K = CTS
#             #
#             # =ROUND((Z2*K2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["WITH TARIFF AMOUNT"],
#                 (
#                     f'=ROUND('
#                     f'(Z{excel_row}*'
#                     f'K{excel_row}),2)'
#                 ),
#                 tariff_formula_format
#             )

#             # =================================================
#             # INDIA %
#             #
#             # T = PER CARAT
#             # V = VDB PRICE INDIA
#             #
#             # =ROUND((100-(T2*100)/V2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["IND%"],
#                 (
#                     f'=IFERROR('
#                     f'ROUND('
#                     f'(100-('
#                     f'T{excel_row}*100)/'
#                     f'V{excel_row}),2),'
#                     f'"")'
#                 ),
#                 difference_formula_format
#             )

#             # =================================================
#             # USA %
#             #
#             # Z = WITH TARIFF COST
#             # X = VDB PRICE USA
#             #
#             # =ROUND((100-(Z2*100)/X2),2)
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers["USA%"],
#                 (
#                     f'=IFERROR('
#                     f'ROUND('
#                     f'(100-('
#                     f'Z{excel_row}*100)/'
#                     f'X{excel_row}),2),'
#                     f'"")'
#                 ),
#                 difference_formula_format
#             )

#             # =================================================
#             # AFTER TARIFF DIFF$
#             #
#             # X = VDB PRICE USA
#             # Z = WITH TARIFF COST
#             #
#             # =X2-Z2
#             # =================================================

#             worksheet.write_formula(
#                 row_number + 1,
#                 column_numbers[
#                     "AFTER TARIFF DIFF$"
#                 ],
#                 (
#                     f'=X{excel_row}-'
#                     f'Z{excel_row}'
#                 ),
#                 difference_formula_format
#             )

#         # ====================================================
#         # COLUMN WIDTHS
#         # ====================================================

#         for col_number, column in enumerate(
#             df.columns
#         ):

#             max_length = len(
#                 str(column)
#             )

#             if len(df) > 0:

#                 sample = df[
#                     column
#                 ].head(100)

#                 for value in sample:

#                     if pd.notna(value):

#                         max_length = max(
#                             max_length,
#                             len(str(value))
#                         )

#             worksheet.set_column(
#                 col_number,
#                 col_number,
#                 min(
#                     max(max_length + 2, 12),
#                     35
#                 )
#             )

#         # ====================================================
#         # FREEZE HEADER
#         # ====================================================

#         worksheet.freeze_panes(
#             1,
#             0
#         )

#         # ====================================================
#         # FILTER
#         # ====================================================

#         if len(df.columns) > 0:

#             worksheet.autofilter(
#                 0,
#                 0,
#                 len(df),
#                 len(df.columns) - 1
#             )

#         # ====================================================
#         # AUTO CALCULATION
#         # ====================================================

#         workbook.set_calc_mode(
#             "auto"
#         )

#     # ========================================================
#     # RETURN EXCEL FILE
#     # ========================================================

#     output.seek(0)

#     return output
# # ============================================================
# # TITLE
# # ============================================================

# st.title(
#     "💎 Company Standard Format Converter"
# )

# st.caption(
#     "Convert different Party Excel Formats into Company Standard Format"
# )


# # ============================================================
# # STEP 1 — UPLOAD FILES
# # ============================================================

# st.header(
#     "1️⃣ Upload Files"
# )


# col1, col2 = st.columns(2)


# with col1:

#     company_file = st.file_uploader(
#         "Company Standard Format",
#         type=["xlsx", "xls"],
#         key="company_file"
#     )


# with col2:

#     master_file = st.file_uploader(
#         "Master Report",
#         type=["xlsx", "xls"],
#         key="master_file"
#     )


# party_files = st.file_uploader(
#     "Party Files",
#     type=["xlsx", "xls"],
#     accept_multiple_files=True,
#     key="party_files"
# )


# # ============================================================
# # CHECK UPLOAD
# # ============================================================

# if company_file is None:

#     st.info(
#         "Please upload Company Standard Format."
#     )

#     st.stop()


# if master_file is None:

#     st.info(
#         "Please upload Master Report."
#     )

#     st.stop()


# if not party_files:

#     st.info(
#         "Please upload at least one Party File."
#     )

#     st.stop()


# # ============================================================
# # READ COMPANY FORMAT
# # ============================================================

# try:

#     company_df = read_excel(
#         company_file
#     )

# except Exception as e:

#     st.error(
#         f"Unable to read Company Standard Format: {e}"
#     )

#     st.stop()


# # ============================================================
# # VALIDATE COMPANY FORMAT
# # ============================================================

# missing_company_columns = (
#     validate_company_format(
#         company_df.columns
#     )
# )


# if missing_company_columns:

#     st.error(
#         "Your Company Standard Format is missing required columns:"
#     )

#     for column in missing_company_columns:

#         st.write(
#             f"❌ {column}"
#         )

#     st.stop()


# # ============================================================
# # READ MASTER
# # ============================================================

# try:

#     master_df = read_excel(
#         master_file
#     )

# except Exception as e:

#     st.error(
#         f"Unable to read Master Report: {e}"
#     )

#     st.stop()


# # ============================================================
# # VALIDATE MASTER
# # ============================================================

# master_key_column = find_column(
#     master_df,
#     "KEY"
# )

# master_grid_column = find_column(
#     master_df,
#     "GRID"
# )

# master_available_column = find_column(
#     master_df,
#     "AVAILABLE"
# )


# if master_key_column is None:

#     st.error(
#         "❌ Master Report does not contain KEY column."
#     )

#     st.stop()


# if master_grid_column is None:

#     st.error(
#         "❌ Master Report does not contain GRID column."
#     )

#     st.stop()


# if master_available_column is None:

#     st.error(
#         "❌ Master Report does not contain AVAILABLE column."
#     )

#     st.stop()


# # ============================================================
# # COMPANY FORMAT PREVIEW
# # ============================================================

# st.divider()

# st.header(
#     "🏢 Company Standard Format"
# )

# st.success(
#     f"Company Format validated successfully — "
#     f"{len(company_df.columns)} columns found."
# )


# with st.expander(
#     "👁️ Preview Company Standard Format",
#     expanded=False
# ):

#     st.dataframe(
#         company_df.head(10),
#         use_container_width=True
#     )


# # ============================================================
# # MASTER PREVIEW
# # ============================================================

# with st.expander(
#     "📊 Master Report Preview",
#     expanded=False
# ):

#     st.write(
#         f"Rows: **{len(master_df)}**"
#     )

#     st.write(
#         f"KEY Column: **{master_key_column}**"
#     )

#     st.write(
#         f"GRID Column: **{master_grid_column}**"
#     )

#     st.write(
#         f"AVAILABLE Column: **{master_available_column}**"
#     )

#     st.dataframe(
#         master_df.head(15),
#         use_container_width=True
#     )


# # ============================================================
# # STEP 2 — PARTY FILES
# # ============================================================

# st.divider()

# st.header(
#     "2️⃣ Party File Conversion"
# )


# # ============================================================
# # LOOP PARTY FILES
# # ============================================================

# for file_index, party_file in enumerate(
#     party_files
# ):


#     st.divider()


#     st.subheader(
#         f"📄 {party_file.name}"
#     )


#     # ========================================================
#     # READ PARTY FILE
#     # ========================================================

#     try:

#         party_df = read_excel(
#             party_file
#         )

#     except Exception as e:

#         st.error(
#             f"Unable to read {party_file.name}: {e}"
#         )

#         continue


#     party_columns = list(
#         party_df.columns
#     )


#     # ========================================================
#     # USER INFORMATION
#     # ========================================================

#     st.markdown(
#         "### 👤 File Information"
#     )


#     info_col1, info_col2 = st.columns(2)


#     with info_col1:

#         selection_done_by = st.text_input(
#             "SELECTION DONE BY",
#             placeholder="Enter person name",
#             key=f"selection_done_by_{file_index}"
#         )


#         india_price_filled_by = st.text_input(
#             "INDIA PRICE FILLED BY",
#             placeholder="Enter person name",
#             key=f"india_price_filled_by_{file_index}"
#         )


#         usa_price_filled_by = st.text_input(
#             "USA PRICE FILLED BY",
#             placeholder="Enter person name",
#             key=f"usa_price_filled_by_{file_index}"
#         )


#     with info_col2:

#         final_file_by = st.text_input(
#             "FINAL THIS FILE BY",
#             placeholder="Enter person name",
#             key=f"final_file_by_{file_index}"
#         )


#         selected_date = st.date_input(
#             "DATE",
#             value=date.today(),
#             key=f"selected_date_{file_index}"
#         )


#         party_name = st.text_input(
#             "PARTY NAME",
#             placeholder="Enter Party Name",
#             key=f"party_name_{file_index}"
#         )


#     # ========================================================
#     # PARTY PREVIEW
#     # ========================================================

#     with st.expander(
#         "👁️ Preview Party File",
#         expanded=False
#     ):

#         st.write(
#             f"Rows: **{len(party_df)}**"
#         )

#         st.write(
#             f"Columns: **{len(party_columns)}**"
#         )

#         st.dataframe(
#             party_df.head(15),
#             use_container_width=True
#         )


#     # ========================================================
#     # MAPPING
#     # ========================================================

#     st.markdown(
#         "### 🔗 Map Party Columns"
#     )


#     mapping = {}


#     left_col, right_col = st.columns(2)


#     for field_index, field in enumerate(
#         PARTY_FIELDS
#     ):

#         container = (
#             left_col
#             if field_index % 2 == 0
#             else right_col
#         )


#         with container:

#             mapping[field] = st.selectbox(
#                 f"{field}",
#                 options=[
#                     "-- Select Party Column --"
#                 ] + party_columns,
#                 key=(
#                     f"mapping_"
#                     f"{file_index}_"
#                     f"{field_index}"
#                 )
#             )


#     # ========================================================
#     # MAPPING STATUS
#     # ========================================================

#     missing_mapping = [
#         field
#         for field, column in mapping.items()
#         if column == "-- Select Party Column --"
#     ]


#     if missing_mapping:

#         st.warning(
#             f"{len(missing_mapping)} field(s) "
#             "still need mapping."
#         )

#     else:

#         st.success(
#             "✅ All Party Columns Mapped"
#         )


#     # ========================================================
#     # CONVERT BUTTON
#     # ========================================================

#     convert_button = st.button(
#         "🚀 Convert This Party File",
#         key=f"convert_{file_index}",
#         type="primary"
#     )


#     if convert_button:


#         # ====================================================
#         # VALIDATION
#         # ====================================================

#         errors = []


#         if not selection_done_by.strip():

#             errors.append(
#                 "SELECTION DONE BY is required."
#             )


#         if not india_price_filled_by.strip():

#             errors.append(
#                 "INDIA PRICE FILLED BY is required."
#             )


#         if not usa_price_filled_by.strip():

#             errors.append(
#                 "USA PRICE FILLED BY is required."
#             )


#         if not final_file_by.strip():

#             errors.append(
#                 "FINAL THIS FILE BY is required."
#             )


#         if not party_name.strip():

#             errors.append(
#                 "PARTY NAME is required."
#             )


#         if missing_mapping:

#             errors.append(
#                 "All Party Columns must be mapped."
#             )


#         # ====================================================
#         # DUPLICATE PARTY COLUMN MAPPING
#         # ====================================================

#         selected_party_columns = [
#             column
#             for column in mapping.values()
#             if column != "-- Select Party Column --"
#         ]


#         duplicates = (
#             len(selected_party_columns)
#             != len(set(selected_party_columns))
#         )


#         if duplicates:

#             errors.append(
#                 "Each Party column should be mapped only once."
#             )


#         # ====================================================
#         # SHOW ERRORS
#         # ====================================================

#         if errors:

#             st.error(
#                 "Please fix the following:"
#             )


#             for error in errors:

#                 st.write(
#                     f"❌ {error}"
#                 )


#             continue


#         # ====================================================
#         # CREATE OUTPUT
#         # ====================================================

#         try:

#             output_df = convert_party_file(

#                 party_df=party_df,

#                 master_df=master_df,

#                 mapping=mapping,

#                 party_name=party_name,

#                 selection_done_by=(
#                     selection_done_by
#                 ),

#                 india_price_filled_by=(
#                     india_price_filled_by
#                 ),

#                 usa_price_filled_by=(
#                     usa_price_filled_by
#                 ),

#                 final_file_by=(
#                     final_file_by
#                 ),

#                 selected_date=(
#                     selected_date
#                 )
#             )


#         except Exception as e:

#             st.error(
#                 f"❌ Conversion failed: {e}"
#             )

#             continue


#         # ====================================================
#         # SAVE TO SESSION
#         # ====================================================

#         st.session_state.converted_files[
#             file_index
#         ] = {

#             "file_name":
#                 party_file.name,

#             "party_name":
#                 party_name,

#             "data":
#                 output_df
#         }


#         # ====================================================
#         # SUCCESS
#         # ====================================================

#         st.success(
#             f"✅ {party_file.name} "
#             "converted successfully."
#         )


#         # ====================================================
#         # PREVIEW
#         # ====================================================

#         with st.expander(
#             "📊 Converted Data Preview",
#             expanded=True
#         ):

#             st.dataframe(
#                 output_df.head(20),
#                 use_container_width=True
#             )


# # ============================================================
# # STEP 3 — FINAL COMBINATION
# # ============================================================

# if st.session_state.converted_files:

#     st.divider()

#     st.header(
#         "3️⃣ Final Company Standard File"
#     )


#     converted_data = [
#         item["data"]
#         for item in
#         st.session_state.converted_files.values()
#     ]


#     # ========================================================
#     # COMBINE ALL PARTY FILES
#     # ========================================================

#     final_df = pd.concat(
#         converted_data,
#         ignore_index=True
#     )


#     # ========================================================
#     # EXACT COMPANY ORDER
#     # ========================================================

#     for column in COMPANY_COLUMNS:

#         if column not in final_df.columns:

#             final_df[column] = ""


#     final_df = final_df[
#         COMPANY_COLUMNS
#     ]


#     # ========================================================
#     # SUMMARY
#     # ========================================================

#     summary_col1, summary_col2 = (
#         st.columns(2)
#     )


#     with summary_col1:

#         st.metric(
#             "Party Files Converted",
#             len(converted_data)
#         )


#     with summary_col2:

#         st.metric(
#             "Total Stones",
#             len(final_df)
#         )


#     # ========================================================
#     # FINAL PREVIEW
#     # ========================================================

#     st.subheader(
#         "📋 Final Preview"
#     )


#     st.dataframe(
#         final_df,
#         use_container_width=True,
#         height=500
#     )


#     # ========================================================
#     # DOWNLOAD
#     # ========================================================

#     excel_data = create_download_excel(
#         final_df
#     )


#     st.download_button(
#         label=(
#             "⬇️ Download Company Standard File"
#         ),

#         data=excel_data,

#         file_name=(
#             "Company_Standard_Final.xlsx"
#         ),

#         mime=(
#             "application/vnd.openxmlformats-officedocument."
#             "spreadsheetml.sheet"
#         ),

#         type="primary",

#         use_container_width=True
#     )












# import streamlit as st
# import pandas as pd
# from io import BytesIO
# from datetime import date


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Diamond Format Converter",
#     page_icon="💎",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )


# # ============================================================
# # CUSTOM CSS — Professional Dark Luxury Theme
# # ============================================================

# st.markdown("""
# <style>
# /* ── Google Fonts ─────────────────────────────────────────── */
# @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

# /* ── Root Variables ───────────────────────────────────────── */
# :root {
#     --navy:    #0B1120;
#     --navy2:   #111827;
#     --card:    #161F30;
#     --border:  #1E2D45;
#     --gold:    #C9A84C;
#     --gold2:   #E5C97A;
#     --silver:  #8EA6BF;
#     --text:    #E8EEF5;
#     --muted:   #6B7E93;
#     --success: #2ECC71;
#     --warn:    #F59E0B;
#     --error:   #EF4444;
#     --radius:  10px;
# }

# /* ── App Background ───────────────────────────────────────── */
# .stApp {
#     background: var(--navy) !important;
#     font-family: 'Inter', sans-serif;
#     color: var(--text);
# }

# /* ── Main block padding ───────────────────────────────────── */
# .block-container {
#     padding: 2rem 3rem 4rem 3rem !important;
#     max-width: 1300px;
# }

# /* ── Hero Banner ──────────────────────────────────────────── */
# .hero-banner {
#     background: linear-gradient(135deg, #0D1B2E 0%, #162033 50%, #0D1B2E 100%);
#     border: 1px solid var(--border);
#     border-top: 3px solid var(--gold);
#     border-radius: var(--radius);
#     padding: 2.5rem 3rem;
#     margin-bottom: 2.5rem;
#     position: relative;
#     overflow: hidden;
# }
# .hero-banner::before {
#     content: "◆";
#     position: absolute;
#     right: 2.5rem;
#     top: 50%;
#     transform: translateY(-50%);
#     font-size: 7rem;
#     color: rgba(201,168,76,0.06);
#     pointer-events: none;
# }
# .hero-title {
#     font-family: 'Playfair Display', serif;
#     font-size: 2.1rem;
#     font-weight: 700;
#     color: var(--gold2);
#     margin: 0 0 0.4rem 0;
#     letter-spacing: 0.01em;
# }
# .hero-subtitle {
#     font-size: 0.95rem;
#     color: var(--silver);
#     margin: 0;
#     font-weight: 300;
# }

# /* ── Section Headers ──────────────────────────────────────── */
# .section-header {
#     display: flex;
#     align-items: center;
#     gap: 0.75rem;
#     margin: 2.2rem 0 1.2rem 0;
#     padding-bottom: 0.65rem;
#     border-bottom: 1px solid var(--border);
# }
# .section-badge {
#     background: linear-gradient(135deg, var(--gold), #A07830);
#     color: #0B1120;
#     font-size: 0.7rem;
#     font-weight: 700;
#     padding: 0.2rem 0.55rem;
#     border-radius: 4px;
#     letter-spacing: 0.08em;
#     text-transform: uppercase;
# }
# .section-title {
#     font-family: 'Playfair Display', serif;
#     font-size: 1.25rem;
#     font-weight: 600;
#     color: var(--text);
#     margin: 0;
# }

# /* ── Cards ────────────────────────────────────────────────── */
# .info-card {
#     background: var(--card);
#     border: 1px solid var(--border);
#     border-radius: var(--radius);
#     padding: 1.5rem;
#     margin-bottom: 1rem;
# }
# .upload-zone {
#     background: linear-gradient(135deg, #111827 0%, #0D1926 100%);
#     border: 1px dashed #2A3D55;
#     border-radius: var(--radius);
#     padding: 1.75rem 1.5rem;
#     text-align: center;
#     transition: border-color 0.2s;
# }
# .upload-zone:hover { border-color: var(--gold); }

# /* ── Status Chips ─────────────────────────────────────────── */
# .chip {
#     display: inline-flex;
#     align-items: center;
#     gap: 0.35rem;
#     font-size: 0.78rem;
#     font-weight: 500;
#     padding: 0.3rem 0.75rem;
#     border-radius: 20px;
#     margin: 0.2rem;
# }
# .chip-success { background: rgba(46,204,113,0.12); color: #2ECC71; border: 1px solid rgba(46,204,113,0.25); }
# .chip-warn    { background: rgba(245,158,11,0.12); color: #F59E0B; border: 1px solid rgba(245,158,11,0.25); }
# .chip-error   { background: rgba(239,68,68,0.12);  color: #EF4444; border: 1px solid rgba(239,68,68,0.25); }
# .chip-info    { background: rgba(201,168,76,0.10); color: var(--gold2); border: 1px solid rgba(201,168,76,0.2); }

# /* ── Metric Cards ─────────────────────────────────────────── */
# .metric-card {
#     background: var(--card);
#     border: 1px solid var(--border);
#     border-left: 3px solid var(--gold);
#     border-radius: var(--radius);
#     padding: 1.2rem 1.5rem;
#     text-align: center;
# }
# .metric-value {
#     font-family: 'Playfair Display', serif;
#     font-size: 2rem;
#     font-weight: 700;
#     color: var(--gold2);
#     line-height: 1;
# }
# .metric-label {
#     font-size: 0.78rem;
#     color: var(--muted);
#     text-transform: uppercase;
#     letter-spacing: 0.06em;
#     margin-top: 0.35rem;
# }

# /* ── Streamlit widget overrides ───────────────────────────── */
# div[data-testid="stFileUploader"] {
#     background: #111827;
#     border: 1px dashed #2A3D55;
#     border-radius: var(--radius);
#     padding: 1rem;
# }
# div[data-testid="stFileUploader"]:hover { border-color: var(--gold); }

# .stTextInput > div > div > input,
# .stSelectbox > div > div > div {
#     background: #111827 !important;
#     border: 1px solid #2A3D55 !important;
#     color: var(--text) !important;
#     border-radius: 6px !important;
# }
# .stTextInput > div > div > input:focus {
#     border-color: var(--gold) !important;
#     box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
# }

# .stDateInput > div > div > input {
#     background: #111827 !important;
#     border: 1px solid #2A3D55 !important;
#     color: var(--text) !important;
#     border-radius: 6px !important;
# }

# /* Labels */
# .stTextInput label,
# .stSelectbox label,
# .stDateInput label {
#     color: var(--silver) !important;
#     font-size: 0.82rem !important;
#     font-weight: 500 !important;
#     letter-spacing: 0.02em !important;
#     text-transform: uppercase !important;
# }

# /* Primary buttons */
# .stButton > button[kind="primary"] {
#     background: linear-gradient(135deg, var(--gold), #A07830) !important;
#     color: #0B1120 !important;
#     border: none !important;
#     font-weight: 600 !important;
#     font-size: 0.9rem !important;
#     letter-spacing: 0.04em !important;
#     padding: 0.6rem 1.8rem !important;
#     border-radius: 6px !important;
#     transition: all 0.2s !important;
#     box-shadow: 0 2px 12px rgba(201,168,76,0.25) !important;
# }
# .stButton > button[kind="primary"]:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 4px 20px rgba(201,168,76,0.35) !important;
# }
# .stButton > button[kind="secondary"],
# .stButton > button:not([kind]) {
#     background: transparent !important;
#     color: var(--gold2) !important;
#     border: 1px solid var(--gold) !important;
#     border-radius: 6px !important;
#     font-weight: 500 !important;
#     transition: all 0.2s !important;
# }
# .stButton > button[kind="secondary"]:hover,
# .stButton > button:not([kind]):hover {
#     background: rgba(201,168,76,0.08) !important;
# }

# /* Download button */
# .stDownloadButton > button {
#     background: linear-gradient(135deg, #1A6B3C, #155230) !important;
#     color: #E8F5EE !important;
#     border: 1px solid #2ECC71 !important;
#     font-weight: 600 !important;
#     letter-spacing: 0.04em !important;
#     font-size: 0.95rem !important;
#     border-radius: 6px !important;
#     padding: 0.7rem 2rem !important;
#     box-shadow: 0 2px 12px rgba(46,204,113,0.2) !important;
#     transition: all 0.2s !important;
# }
# .stDownloadButton > button:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 4px 20px rgba(46,204,113,0.3) !important;
# }

# /* Expander */
# .streamlit-expanderHeader {
#     background: #111827 !important;
#     border: 1px solid var(--border) !important;
#     border-radius: var(--radius) !important;
#     color: var(--silver) !important;
#     font-size: 0.88rem !important;
#     font-weight: 500 !important;
# }
# .streamlit-expanderContent {
#     background: #0F1A27 !important;
#     border: 1px solid var(--border) !important;
#     border-top: none !important;
#     border-radius: 0 0 var(--radius) var(--radius) !important;
# }

# /* Alerts */
# .stAlert {
#     border-radius: var(--radius) !important;
#     font-size: 0.88rem !important;
# }
# div[data-testid="stInfoMessage"] {
#     background: rgba(201,168,76,0.08) !important;
#     border-left: 3px solid var(--gold) !important;
#     color: var(--gold2) !important;
# }
# div[data-testid="stSuccessMessage"] {
#     background: rgba(46,204,113,0.08) !important;
#     border-left: 3px solid var(--success) !important;
# }
# div[data-testid="stErrorMessage"] {
#     background: rgba(239,68,68,0.08) !important;
#     border-left: 3px solid var(--error) !important;
# }
# div[data-testid="stWarningMessage"] {
#     background: rgba(245,158,11,0.08) !important;
#     border-left: 3px solid var(--warn) !important;
# }

# /* Dataframe */
# .stDataFrame { border-radius: var(--radius) !important; overflow: hidden; }

# /* Divider */
# hr { border-color: var(--border) !important; }

# /* Sidebar (if used) */
# section[data-testid="stSidebar"] {
#     background: var(--navy2) !important;
#     border-right: 1px solid var(--border) !important;
# }

# /* Column group labels */
# .col-group-label {
#     font-size: 0.72rem;
#     font-weight: 600;
#     text-transform: uppercase;
#     letter-spacing: 0.08em;
#     color: var(--muted);
#     margin-bottom: 0.5rem;
#     padding-bottom: 0.25rem;
#     border-bottom: 1px solid var(--border);
# }

# /* Party file card */
# .party-card {
#     background: var(--card);
#     border: 1px solid var(--border);
#     border-radius: var(--radius);
#     padding: 1.75rem 2rem 1.5rem 2rem;
#     margin-bottom: 1.5rem;
# }
# .party-card-title {
#     font-family: 'Playfair Display', serif;
#     font-size: 1.1rem;
#     font-weight: 600;
#     color: var(--gold2);
#     margin-bottom: 0.25rem;
# }
# .party-card-meta {
#     font-size: 0.8rem;
#     color: var(--muted);
# }

# /* Step indicator */
# .step-row {
#     display: flex;
#     gap: 0;
#     margin-bottom: 2rem;
# }
# .step-item {
#     flex: 1;
#     display: flex;
#     align-items: center;
#     gap: 0.6rem;
#     padding: 0.7rem 1rem;
#     background: #111827;
#     border: 1px solid var(--border);
#     font-size: 0.82rem;
#     color: var(--muted);
#     font-weight: 500;
# }
# .step-item:first-child { border-radius: 6px 0 0 6px; }
# .step-item:last-child  { border-radius: 0 6px 6px 0; }
# .step-item.active {
#     background: rgba(201,168,76,0.08);
#     border-color: var(--gold);
#     color: var(--gold2);
# }
# .step-num {
#     width: 22px; height: 22px;
#     border-radius: 50%;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 0.72rem; font-weight: 700;
#     flex-shrink: 0;
#     background: var(--border); color: var(--muted);
# }
# .step-item.active .step-num {
#     background: var(--gold); color: #0B1120;
# }

# /* Mapping grid */
# .mapping-label {
#     font-size: 0.75rem;
#     font-weight: 600;
#     color: var(--gold2);
#     text-transform: uppercase;
#     letter-spacing: 0.06em;
#     padding: 0.35rem 0.7rem;
#     background: rgba(201,168,76,0.08);
#     border-radius: 4px;
#     display: inline-block;
#     margin-bottom: 0.3rem;
# }

# /* Hide streamlit branding */
# #MainMenu, footer, header { visibility: hidden; }
# </style>
# """, unsafe_allow_html=True)


# # ============================================================
# # COMPANY STANDARD COLUMNS
# # ============================================================

# COMPANY_COLUMNS = [
#     "SELECTION DONE BY",
#     "INDIA PRICE FILLED BY",
#     "USA PRICE FILLED BY",
#     "FINAL THIS FILE BY",
#     "DATE",
#     "STONE ID",
#     "PARTY NAME",
#     "REPORT NO.",
#     "GROWTH TYPE",
#     "SHAPE",
#     "CTS",
#     "SIZE GROUP",
#     "COLOR",
#     "CLARITY",
#     "KEY",
#     "GRID",
#     "AVAILABLE",
#     "SAME",
#     "REMARK",
#     "PER CARAT",
#     "TOTAL AMT",
#     "VDB PRICE INDIA",
#     "VDB AMOUNT INDIA",
#     "VDB PRICE USA",
#     "VDB AMOUNT USA",
#     "WITH TARIFF COST",
#     "WITH TARIFF AMOUNT",
#     "IND%",
#     "USA%",
#     "AFTER TARIFF DIFF$"
# ]

# PARTY_FIELDS = [
#     "STONE ID",
#     "REPORT NO.",
#     "GROWTH TYPE",
#     "SHAPE",
#     "CTS",
#     "COLOR",
#     "CLARITY",
#     "PER CARAT",
#     "VDB PRICE INDIA",
#     "VDB PRICE USA"
# ]

# FIELD_TO_COMPANY_COLUMN = {
#     "STONE ID": "STONE ID",
#     "REPORT NO.": "REPORT NO.",
#     "GROWTH TYPE": "GROWTH TYPE",
#     "SHAPE": "SHAPE",
#     "CTS": "CTS",
#     "COLOR": "COLOR",
#     "CLARITY": "CLARITY",
#     "PER CARAT": "PER CARAT",
#     "VDB PRICE INDIA": "VDB PRICE INDIA",
#     "VDB PRICE USA": "VDB PRICE USA"
# }

# if "converted_files" not in st.session_state:
#     st.session_state.converted_files = {}


# # ============================================================
# # UTILITIES
# # ============================================================

# def normalize_column_name(value):
#     if value is None:
#         return ""
#     return (
#         str(value)
#         .strip()
#         .upper()
#         .replace("\n", " ")
#         .replace("_", " ")
#     )

# def find_column(df, wanted_name):
#     wanted = normalize_column_name(wanted_name)
#     for column in df.columns:
#         if normalize_column_name(column) == wanted:
#             return column
#     return None

# def read_excel(file):
#     file.seek(0)
#     return pd.read_excel(file, engine="openpyxl")

# def validate_company_format(columns):
#     actual = [normalize_column_name(c) for c in columns]
#     required = [normalize_column_name(c) for c in COMPANY_COLUMNS]
#     return [c for c in required if c not in actual]

# def get_size_group(cts):
#     if pd.isna(cts):
#         return ""
#     try:
#         cts = float(cts)
#     except (ValueError, TypeError):
#         return ""

#     if cts < 0.30:   return ""
#     if cts <= 0.50:  return "0.30 - 0.50"
#     if cts <= 0.59:  return "0.50 - 0.59"
#     if cts <= 0.69:  return "0.60 - 0.69"
#     if cts <= 0.79:  return "0.70 - 0.79"
#     if cts <= 0.89:  return "0.80 - 0.89"
#     if cts <= 0.94:  return "0.90 - 0.94"
#     if cts <= 0.99:  return "0.95 - 0.99"
#     if cts <= 1.10:  return "1.00 - 1.10"
#     if cts <= 1.19:  return "1.11 - 1.19"
#     if cts <= 1.29:  return "1.20 - 1.29"
#     if cts <= 1.39:  return "1.30 - 1.39"
#     if cts <= 1.49:  return "1.40 - 1.49"
#     if cts < 4.00:
#         lower = int(cts * 10) / 10
#         upper = lower + 0.09
#         return f"{lower:.2f} - {upper:.2f}"
#     if cts <= 4.10:  return "4.00 - 4.10"
#     if cts < 4.50:   return "4.11 - 4.49"
#     if cts <= 4.59:  return "4.50 - 4.59"
#     if cts < 5.00:   return "4.60 - 4.99"
#     if cts <= 5.59:  return "5.00 - 5.59"
#     if cts < 6.00:   return "5.60 - 5.99"
#     if cts < 7.00:   return "6.00 - 6.99"

#     whole = int(cts)
#     decimal = cts - whole
#     if decimal <= 0.10:
#         return f"{whole:.2f} - {whole + 0.10:.2f}"
#     return f"{whole + 0.11:.2f} - {whole + 0.99:.2f}"

# def create_blank_output(number_of_rows):
#     return pd.DataFrame("", index=range(number_of_rows), columns=COMPANY_COLUMNS)


# # ============================================================
# # CONVERT PARTY FILE  (unchanged logic)
# # ============================================================

# def convert_party_file(
#     party_df, master_df, mapping, party_name,
#     selection_done_by, india_price_filled_by,
#     usa_price_filled_by, final_file_by, selected_date
# ):
#     output = create_blank_output(len(party_df))

#     output["SELECTION DONE BY"]   = selection_done_by
#     output["INDIA PRICE FILLED BY"] = india_price_filled_by
#     output["USA PRICE FILLED BY"]  = usa_price_filled_by
#     output["FINAL THIS FILE BY"]   = final_file_by
#     output["DATE"]                 = selected_date
#     output["PARTY NAME"]           = party_name

#     for party_field, party_column in mapping.items():
#         if party_column is None:
#             continue
#         if party_column == "-- Select Party Column --":
#             continue
#         if party_column not in party_df.columns:
#             continue
#         company_column = FIELD_TO_COMPANY_COLUMN[party_field]
#         output[company_column] = party_df[party_column].reset_index(drop=True)

#     output["SIZE GROUP"] = output["CTS"].apply(get_size_group)

#     for column in ["SHAPE", "SIZE GROUP", "COLOR", "CLARITY"]:
#         output[column] = output[column].fillna("").astype(str).str.strip()

#     output["KEY"] = (
#         output["SHAPE"]
#         + output["SIZE GROUP"]
#         + output["COLOR"]
#         + output["CLARITY"]
#     )

#     master = master_df.copy()
#     master_key_column       = find_column(master, "KEY")
#     master_grid_column      = find_column(master, "GRID")
#     master_available_column = find_column(master, "AVAILABLE")

#     if master_key_column is None:
#         raise ValueError("Master File does not contain a KEY column.")
#     if master_grid_column is None:
#         raise ValueError("Master File does not contain a Grid column.")
#     if master_available_column is None:
#         raise ValueError("Master File does not contain an Available column.")

#     master_lookup = master[[master_key_column, master_grid_column, master_available_column]].copy()
#     master_lookup.columns = ["MASTER_KEY", "MASTER_GRID", "MASTER_AVAILABLE"]
#     master_lookup["MASTER_KEY"] = master_lookup["MASTER_KEY"].fillna("").astype(str).str.strip()
#     master_lookup["MASTER_GRID"] = pd.to_numeric(master_lookup["MASTER_GRID"], errors="coerce").fillna(0)
#     master_lookup["MASTER_AVAILABLE"] = pd.to_numeric(master_lookup["MASTER_AVAILABLE"], errors="coerce").fillna(0)
#     master_lookup = master_lookup.drop_duplicates(subset=["MASTER_KEY"], keep="first")

#     output = output.merge(master_lookup, left_on="KEY", right_on="MASTER_KEY", how="left")
#     output["GRID"]      = pd.to_numeric(output["MASTER_GRID"], errors="coerce").fillna(0)
#     output["AVAILABLE"] = pd.to_numeric(output["MASTER_AVAILABLE"], errors="coerce").fillna(0)
#     output.drop(columns=["MASTER_KEY", "MASTER_GRID", "MASTER_AVAILABLE"], inplace=True, errors="ignore")

#     output["SAME"]   = ""
#     output["REMARK"] = ""

#     for column in ["TOTAL AMT", "VDB AMOUNT INDIA", "VDB AMOUNT USA",
#                    "WITH TARIFF COST", "WITH TARIFF AMOUNT", "IND%", "USA%", "AFTER TARIFF DIFF$"]:
#         output[column] = ""

#     for column in COMPANY_COLUMNS:
#         if column not in output.columns:
#             output[column] = ""

#     output = output[COMPANY_COLUMNS].reset_index(drop=True)
#     return output


# # ============================================================
# # CREATE DOWNLOAD EXCEL  (unchanged logic)
# # ============================================================

# def create_download_excel(df):
#     output = BytesIO()
#     df = df.copy()
#     df.columns = [str(c).strip() for c in df.columns]

#     for column in COMPANY_COLUMNS:
#         if str(column).strip() not in df.columns:
#             df[str(column).strip()] = ""

#     df = df[[str(c).strip() for c in COMPANY_COLUMNS]]

#     with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
#         df.to_excel(writer, index=False, sheet_name="Final File")
#         workbook  = writer.book
#         worksheet = writer.sheets["Final File"]

#         header_format = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True})

#         header_size_grid_same = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#fcba03"})
#         header_per_carat_total = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#5aa6c7"})
#         header_india = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#b592d6"})
#         header_usa = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#6aba95"})
#         header_tariff = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#c27676"})
#         header_difference = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#f8fc03"})

#         normal_format  = workbook.add_format({"border": 1, "valign": "vcenter"})
#         number_format  = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "0.00"})
#         integer_format = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "0"})
#         date_format    = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "dd-mm-yyyy"})

#         size_grid_same_format  = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#fcba03"})
#         per_carat_total_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#5aa6c7", "num_format": "0.00"})
#         india_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#b592d6", "num_format": "0.00"})
#         usa_format   = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#6aba95", "num_format": "0.00"})
#         tariff_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#c27676", "num_format": "0.00"})

#         same_formula_format       = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#fcba03", "num_format": "0"})
#         total_formula_format      = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#5aa6c7", "num_format": "0.00"})
#         vdb_india_formula_format  = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#b592d6", "num_format": "0.00"})
#         vdb_usa_formula_format    = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#6aba95", "num_format": "0.00"})
#         tariff_formula_format     = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#c27676", "num_format": "0.00"})
#         difference_formula_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#f8fc03", "num_format": "0.00"})

#         column_numbers = {str(c).strip(): i for i, c in enumerate(df.columns)}

#         formula_columns = [
#             "KEY", "SAME", "TOTAL AMT", "VDB AMOUNT INDIA", "VDB AMOUNT USA",
#             "WITH TARIFF COST", "WITH TARIFF AMOUNT", "IND%", "USA%", "AFTER TARIFF DIFF$"
#         ]

#         for col_number, column in enumerate(df.columns):
#             column_name = str(column).strip()
#             if column_name in ["SIZE GROUP", "GRID", "AVAILABLE", "SAME"]:
#                 fmt = header_size_grid_same
#             elif column_name in ["PER CARAT", "TOTAL AMT"]:
#                 fmt = header_per_carat_total
#             elif column_name in ["VDB PRICE INDIA", "VDB AMOUNT INDIA"]:
#                 fmt = header_india
#             elif column_name in ["VDB PRICE USA", "VDB AMOUNT USA"]:
#                 fmt = header_usa
#             elif column_name in ["WITH TARIFF COST", "WITH TARIFF AMOUNT"]:
#                 fmt = header_tariff
#             elif column_name in ["IND%", "USA%", "AFTER TARIFF DIFF$"]:
#                 fmt = header_difference
#             else:
#                 fmt = header_format
#             worksheet.write(0, col_number, column_name, fmt)

#         for row_number in range(len(df)):
#             for col_number, column in enumerate(df.columns):
#                 column_name = str(column).strip()
#                 if column_name in formula_columns:
#                     continue
#                 value = df.iloc[row_number, col_number]
#                 if pd.isna(value):
#                     value = ""
#                 if column_name == "DATE":
#                     worksheet.write(row_number + 1, col_number, value, date_format)
#                 elif column_name == "SIZE GROUP":
#                     worksheet.write(row_number + 1, col_number, value, size_grid_same_format)
#                 elif column_name in ["GRID", "AVAILABLE"]:
#                     worksheet.write(row_number + 1, col_number, value, size_grid_same_format)
#                 elif column_name == "PER CARAT":
#                     worksheet.write(row_number + 1, col_number, value, per_carat_total_format)
#                 elif column_name == "VDB PRICE INDIA":
#                     worksheet.write(row_number + 1, col_number, value, india_format)
#                 elif column_name == "VDB PRICE USA":
#                     worksheet.write(row_number + 1, col_number, value, usa_format)
#                 elif column_name in ["WITH TARIFF COST"]:
#                     worksheet.write(row_number + 1, col_number, value, tariff_format)
#                 else:
#                     worksheet.write(row_number + 1, col_number, value, normal_format)

#         for row_number in range(len(df)):
#             excel_row = row_number + 2
#             worksheet.write_formula(row_number + 1, column_numbers["KEY"],
#                 f'=CONCATENATE(J{excel_row},L{excel_row},M{excel_row},N{excel_row})', normal_format)
#             worksheet.write_formula(row_number + 1, column_numbers["SAME"],
#                 f'=COUNTIF(O:O,O{excel_row})', same_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["TOTAL AMT"],
#                 f'=ROUND((T{excel_row}*K{excel_row}),2)', total_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["VDB AMOUNT INDIA"],
#                 f'=ROUND((V{excel_row}*K{excel_row}),2)', vdb_india_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["VDB AMOUNT USA"],
#                 f'=ROUND((X{excel_row}*K{excel_row}),2)', vdb_usa_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["WITH TARIFF COST"],
#                 f'=ROUND((T{excel_row}*1.08),2)', tariff_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["WITH TARIFF AMOUNT"],
#                 f'=ROUND((Z{excel_row}*K{excel_row}),2)', tariff_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["IND%"],
#                 f'=IFERROR(ROUND((100-(T{excel_row}*100)/V{excel_row}),2),"")', difference_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["USA%"],
#                 f'=IFERROR(ROUND((100-(Z{excel_row}*100)/X{excel_row}),2),"")', difference_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["AFTER TARIFF DIFF$"],
#                 f'=X{excel_row}-Z{excel_row}', difference_formula_format)

#         for col_number, column in enumerate(df.columns):
#             max_length = len(str(column))
#             if len(df) > 0:
#                 for value in df[column].head(100):
#                     if pd.notna(value):
#                         max_length = max(max_length, len(str(value)))
#             worksheet.set_column(col_number, col_number, min(max(max_length + 2, 12), 35))

#         worksheet.freeze_panes(1, 0)
#         if len(df.columns) > 0:
#             worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
#         workbook.set_calc_mode("auto")

#     output.seek(0)
#     return output


# # ============================================================
# # HERO BANNER
# # ============================================================

# st.markdown("""
# <div class="hero-banner">
#     <div class="hero-title">◆ Diamond Format Converter</div>
#     <div class="hero-subtitle">
#         Transform any Party Excel file into Company Standard Format — with Master pricing, tariff calculations, and formula-ready output
#     </div>
# </div>
# """, unsafe_allow_html=True)


# # ============================================================
# # STEP INDICATOR
# # ============================================================

# files_uploaded  = False
# files_converted = bool(st.session_state.converted_files)

# st.markdown("""
# <div class="step-row">
#     <div class="step-item active">
#         <div class="step-num">1</div>
#         Upload Files
#     </div>
#     <div class="step-item">
#         <div class="step-num">2</div>
#         Map &amp; Convert Party Files
#     </div>
#     <div class="step-item">
#         <div class="step-num">3</div>
#         Download Final File
#     </div>
# </div>
# """, unsafe_allow_html=True)


# # ============================================================
# # STEP 1 — UPLOAD FILES
# # ============================================================

# st.markdown("""
# <div class="section-header">
#     <span class="section-badge">Step 1</span>
#     <span class="section-title">Upload Files</span>
# </div>
# """, unsafe_allow_html=True)

# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="col-group-label">Company &amp; Master Files</div>', unsafe_allow_html=True)
#     company_file = st.file_uploader(
#         "Company Standard Format",
#         type=["xlsx", "xls"],
#         key="company_file",
#         help="Upload your company's standard Excel template"
#     )
#     master_file = st.file_uploader(
#         "Master Report",
#         type=["xlsx", "xls"],
#         key="master_file",
#         help="Upload the master pricing report with KEY, GRID & AVAILABLE columns"
#     )

# with col2:
#     st.markdown('<div class="col-group-label">Party Files (multiple allowed)</div>', unsafe_allow_html=True)
#     party_files = st.file_uploader(
#         "Party Files",
#         type=["xlsx", "xls"],
#         accept_multiple_files=True,
#         key="party_files",
#         help="Upload one or more party Excel files to convert"
#     )


# # ── Upload Status ──────────────────────────────────────────

# status_html = '<div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin:1rem 0;">'
# status_html += f'<span class="chip {"chip-success" if company_file else "chip-warn"}">{"✓" if company_file else "○"} Company Format</span>'
# status_html += f'<span class="chip {"chip-success" if master_file else "chip-warn"}">{"✓" if master_file else "○"} Master Report</span>'
# status_html += f'<span class="chip {"chip-success" if party_files else "chip-warn"}">{"✓" if party_files else "○"} Party Files ({len(party_files) if party_files else 0} uploaded)</span>'
# status_html += '</div>'
# st.markdown(status_html, unsafe_allow_html=True)

# if company_file is None:
#     st.info("⬆️  Upload your Company Standard Format file to continue.")
#     st.stop()

# if master_file is None:
#     st.info("⬆️  Upload the Master Report file to continue.")
#     st.stop()

# if not party_files:
#     st.info("⬆️  Upload at least one Party File to convert.")
#     st.stop()


# # ── Read & Validate ────────────────────────────────────────

# try:
#     company_df = read_excel(company_file)
# except Exception as e:
#     st.error(f"Cannot read Company Standard Format: {e}")
#     st.stop()

# missing_cols = validate_company_format(company_df.columns)
# if missing_cols:
#     st.error("Company Standard Format is missing required columns:")
#     for c in missing_cols:
#         st.write(f"  ❌ {c}")
#     st.stop()

# try:
#     master_df = read_excel(master_file)
# except Exception as e:
#     st.error(f"Cannot read Master Report: {e}")
#     st.stop()

# master_key_column       = find_column(master_df, "KEY")
# master_grid_column      = find_column(master_df, "GRID")
# master_available_column = find_column(master_df, "AVAILABLE")

# if not master_key_column:
#     st.error("❌ Master Report is missing the KEY column.")
#     st.stop()
# if not master_grid_column:
#     st.error("❌ Master Report is missing the GRID column.")
#     st.stop()
# if not master_available_column:
#     st.error("❌ Master Report is missing the AVAILABLE column.")
#     st.stop()


# # ── File Preview Cards ─────────────────────────────────────

# preview_col1, preview_col2 = st.columns(2)

# with preview_col1:
#     with st.expander("👁  Company Standard Format — Preview", expanded=False):
#         st.markdown(f'<span class="chip chip-success">✓ {len(company_df.columns)} columns validated</span>', unsafe_allow_html=True)
#         st.dataframe(company_df.head(10), use_container_width=True)

# with preview_col2:
#     with st.expander("📊 Master Report — Preview", expanded=False):
#         st.markdown(
#             f'<span class="chip chip-info">KEY: {master_key_column}</span>'
#             f'<span class="chip chip-info">GRID: {master_grid_column}</span>'
#             f'<span class="chip chip-info">AVAIL: {master_available_column}</span>'
#             f'<span class="chip chip-success">{len(master_df):,} rows</span>',
#             unsafe_allow_html=True
#         )
#         st.dataframe(master_df.head(15), use_container_width=True)


# # ============================================================
# # STEP 2 — PARTY FILE CONVERSION
# # ============================================================

# st.markdown("""
# <div class="section-header">
#     <span class="section-badge">Step 2</span>
#     <span class="section-title">Map &amp; Convert Party Files</span>
# </div>
# """, unsafe_allow_html=True)

# for file_index, party_file in enumerate(party_files):

#     st.markdown(f"""
#     <div class="party-card">
#         <div class="party-card-title">◇ {party_file.name}</div>
#         <div class="party-card-meta">Party File {file_index + 1} of {len(party_files)}</div>
#     </div>
#     """, unsafe_allow_html=True)

#     try:
#         party_df = read_excel(party_file)
#     except Exception as e:
#         st.error(f"Cannot read {party_file.name}: {e}")
#         continue

#     party_columns = list(party_df.columns)

#     # ── File Information ──────────────────────────────────
#     st.markdown('<div class="col-group-label" style="margin-top:0.5rem;">File Information</div>', unsafe_allow_html=True)

#     info_col1, info_col2, info_col3 = st.columns(3)

#     with info_col1:
#         selection_done_by = st.text_input(
#             "Selection Done By",
#             placeholder="Person name",
#             key=f"selection_done_by_{file_index}"
#         )
#         india_price_filled_by = st.text_input(
#             "India Price Filled By",
#             placeholder="Person name",
#             key=f"india_price_filled_by_{file_index}"
#         )

#     with info_col2:
#         usa_price_filled_by = st.text_input(
#             "USA Price Filled By",
#             placeholder="Person name",
#             key=f"usa_price_filled_by_{file_index}"
#         )
#         final_file_by = st.text_input(
#             "Final File By",
#             placeholder="Person name",
#             key=f"final_file_by_{file_index}"
#         )

#     with info_col3:
#         party_name = st.text_input(
#             "Party Name",
#             placeholder="Enter party name",
#             key=f"party_name_{file_index}"
#         )
#         selected_date = st.date_input(
#             "Date",
#             value=date.today(),
#             key=f"selected_date_{file_index}"
#         )

#     # ── Party Preview ─────────────────────────────────────
#     with st.expander(f"👁  Preview — {party_file.name}", expanded=False):
#         st.markdown(
#             f'<span class="chip chip-info">{len(party_df):,} rows</span>'
#             f'<span class="chip chip-info">{len(party_columns)} columns</span>',
#             unsafe_allow_html=True
#         )
#         st.dataframe(party_df.head(15), use_container_width=True)

#     # ── Column Mapping ────────────────────────────────────
#     st.markdown('<div class="col-group-label" style="margin-top:1.25rem;">Column Mapping — Match party columns to company fields</div>', unsafe_allow_html=True)

#     mapping = {}
#     cols = st.columns(2)

#     for field_index, field in enumerate(PARTY_FIELDS):
#         container = cols[field_index % 2]
#         with container:
#             mapping[field] = st.selectbox(
#                 field,
#                 options=["-- Select Party Column --"] + party_columns,
#                 key=f"mapping_{file_index}_{field_index}"
#             )

#     missing_mapping = [
#         f for f, c in mapping.items()
#         if c == "-- Select Party Column --"
#     ]

#     if missing_mapping:
#         st.markdown(
#             f'<div style="margin-top:0.5rem;"><span class="chip chip-warn">⚠ {len(missing_mapping)} field(s) unmapped</span></div>',
#             unsafe_allow_html=True
#         )
#     else:
#         st.markdown(
#             '<div style="margin-top:0.5rem;"><span class="chip chip-success">✓ All columns mapped</span></div>',
#             unsafe_allow_html=True
#         )

#     st.write("")
#     convert_button = st.button(
#         f"◆  Convert  {party_file.name}",
#         key=f"convert_{file_index}",
#         type="primary"
#     )

#     if convert_button:
#         errors = []
#         if not selection_done_by.strip():   errors.append("Selection Done By is required.")
#         if not india_price_filled_by.strip(): errors.append("India Price Filled By is required.")
#         if not usa_price_filled_by.strip():  errors.append("USA Price Filled By is required.")
#         if not final_file_by.strip():        errors.append("Final File By is required.")
#         if not party_name.strip():           errors.append("Party Name is required.")
#         if missing_mapping:                  errors.append("All party columns must be mapped.")

#         selected_vals = [c for c in mapping.values() if c != "-- Select Party Column --"]
#         if len(selected_vals) != len(set(selected_vals)):
#             errors.append("Each party column should be mapped only once.")

#         if errors:
#             st.error("Fix the following before converting:")
#             for err in errors:
#                 st.write(f"  ❌ {err}")
#             continue

#         try:
#             output_df = convert_party_file(
#                 party_df=party_df,
#                 master_df=master_df,
#                 mapping=mapping,
#                 party_name=party_name,
#                 selection_done_by=selection_done_by,
#                 india_price_filled_by=india_price_filled_by,
#                 usa_price_filled_by=usa_price_filled_by,
#                 final_file_by=final_file_by,
#                 selected_date=selected_date
#             )
#         except Exception as e:
#             st.error(f"Conversion failed: {e}")
#             continue

#         st.session_state.converted_files[file_index] = {
#             "file_name": party_file.name,
#             "party_name": party_name,
#             "data": output_df
#         }

#         st.success(f"✓ {party_file.name} converted — {len(output_df):,} rows ready.")

#         with st.expander("📊 Converted Data Preview", expanded=True):
#             st.dataframe(output_df.head(20), use_container_width=True)

#     st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)


# # ============================================================
# # STEP 3 — FINAL FILE
# # ============================================================

# if st.session_state.converted_files:

#     st.markdown("""
#     <div class="section-header">
#         <span class="section-badge">Step 3</span>
#         <span class="section-title">Final Company Standard File</span>
#     </div>
#     """, unsafe_allow_html=True)

#     converted_data = [item["data"] for item in st.session_state.converted_files.values()]
#     final_df = pd.concat(converted_data, ignore_index=True)

#     for column in COMPANY_COLUMNS:
#         if column not in final_df.columns:
#             final_df[column] = ""
#     final_df = final_df[COMPANY_COLUMNS]

#     # ── Summary Metrics ───────────────────────────────────
#     m1, m2, m3 = st.columns(3)
#     with m1:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{len(converted_data)}</div>
#             <div class="metric-label">Party Files Converted</div>
#         </div>""", unsafe_allow_html=True)
#     with m2:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{len(final_df):,}</div>
#             <div class="metric-label">Total Stones</div>
#         </div>""", unsafe_allow_html=True)
#     with m3:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{len(COMPANY_COLUMNS)}</div>
#             <div class="metric-label">Output Columns</div>
#         </div>""", unsafe_allow_html=True)

#     st.write("")

#     # ── Final Preview ─────────────────────────────────────
#     st.markdown('<div class="col-group-label">Final Data Preview</div>', unsafe_allow_html=True)
#     st.dataframe(final_df, use_container_width=True, height=460)

#     st.write("")

#     # ── Download ──────────────────────────────────────────
#     excel_data = create_download_excel(final_df)

#     st.download_button(
#         label="⬇  Download Company Standard File  (.xlsx)",
#         data=excel_data,
#         file_name="Company_Standard_Final.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         type="primary",
#         use_container_width=True
#     )

#     st.markdown("""
#     <div style="text-align:center; margin-top:1rem; font-size:0.78rem; color:#4A6070;">
#         Excel formulas, color-coded columns, freeze panes, and auto-filter are included in the downloaded file.
#     </div>
#     """, unsafe_allow_html=True)





# import streamlit as st
# import pandas as pd
# from io import BytesIO
# from datetime import date


# # ============================================================
# # PAGE CONFIG
# # ============================================================

# st.set_page_config(
#     page_title="Diamond Format Converter",
#     page_icon="💎",
#     layout="wide",
#     initial_sidebar_state="collapsed"
# )


# # ============================================================
# # CUSTOM CSS — Professional Dark Luxury Theme
# # ============================================================

# st.markdown("""
# <style>
# /* ── Google Fonts ─────────────────────────────────────────── */
# @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

# /* ── Root Variables ───────────────────────────────────────── */
# :root {
#     --navy:    #0B1120;
#     --navy2:   #111827;
#     --card:    #161F30;
#     --border:  #1E2D45;
#     --gold:    #C9A84C;
#     --gold2:   #E5C97A;
#     --silver:  #8EA6BF;
#     --text:    #E8EEF5;
#     --muted:   #6B7E93;
#     --success: #2ECC71;
#     --warn:    #F59E0B;
#     --error:   #EF4444;
#     --radius:  10px;
# }

# /* ── App Background ───────────────────────────────────────── */
# .stApp {
#     background: var(--navy) !important;
#     font-family: 'Inter', sans-serif;
#     color: var(--text);
# }

# /* ── Main block padding ───────────────────────────────────── */
# .block-container {
#     padding: 2rem 3rem 4rem 3rem !important;
#     max-width: 1300px;
# }

# /* ── Hero Banner ──────────────────────────────────────────── */
# .hero-banner {
#     background: linear-gradient(135deg, #0D1B2E 0%, #162033 50%, #0D1B2E 100%);
#     border: 1px solid var(--border);
#     border-top: 3px solid var(--gold);
#     border-radius: var(--radius);
#     padding: 2.5rem 3rem;
#     margin-bottom: 2.5rem;
#     position: relative;
#     overflow: hidden;
# }
# .hero-banner::before {
#     content: "◆";
#     position: absolute;
#     right: 2.5rem;
#     top: 50%;
#     transform: translateY(-50%);
#     font-size: 7rem;
#     color: rgba(201,168,76,0.06);
#     pointer-events: none;
# }
# .hero-title {
#     font-family: 'Playfair Display', serif;
#     font-size: 2.1rem;
#     font-weight: 700;
#     color: var(--gold2);
#     margin: 0 0 0.4rem 0;
#     letter-spacing: 0.01em;
# }
# .hero-subtitle {
#     font-size: 0.95rem;
#     color: var(--silver);
#     margin: 0;
#     font-weight: 300;
# }

# /* ── Section Headers ──────────────────────────────────────── */
# .section-header {
#     display: flex;
#     align-items: center;
#     gap: 0.75rem;
#     margin: 2.2rem 0 1.2rem 0;
#     padding-bottom: 0.65rem;
#     border-bottom: 1px solid var(--border);
# }
# .section-badge {
#     background: linear-gradient(135deg, var(--gold), #A07830);
#     color: #0B1120;
#     font-size: 0.7rem;
#     font-weight: 700;
#     padding: 0.2rem 0.55rem;
#     border-radius: 4px;
#     letter-spacing: 0.08em;
#     text-transform: uppercase;
# }
# .section-title {
#     font-family: 'Playfair Display', serif;
#     font-size: 1.25rem;
#     font-weight: 600;
#     color: var(--text);
#     margin: 0;
# }

# /* ── Cards ────────────────────────────────────────────────── */
# .info-card {
#     background: var(--card);
#     border: 1px solid var(--border);
#     border-radius: var(--radius);
#     padding: 1.5rem;
#     margin-bottom: 1rem;
# }
# .upload-zone {
#     background: linear-gradient(135deg, #111827 0%, #0D1926 100%);
#     border: 1px dashed #2A3D55;
#     border-radius: var(--radius);
#     padding: 1.75rem 1.5rem;
#     text-align: center;
#     transition: border-color 0.2s;
# }
# .upload-zone:hover { border-color: var(--gold); }

# /* ── Status Chips ─────────────────────────────────────────── */
# .chip {
#     display: inline-flex;
#     align-items: center;
#     gap: 0.35rem;
#     font-size: 0.78rem;
#     font-weight: 500;
#     padding: 0.3rem 0.75rem;
#     border-radius: 20px;
#     margin: 0.2rem;
# }
# .chip-success { background: rgba(46,204,113,0.12); color: #2ECC71; border: 1px solid rgba(46,204,113,0.25); }
# .chip-warn    { background: rgba(245,158,11,0.12); color: #F59E0B; border: 1px solid rgba(245,158,11,0.25); }
# .chip-error   { background: rgba(239,68,68,0.12);  color: #EF4444; border: 1px solid rgba(239,68,68,0.25); }
# .chip-info    { background: rgba(201,168,76,0.10); color: var(--gold2); border: 1px solid rgba(201,168,76,0.2); }

# /* ── Metric Cards ─────────────────────────────────────────── */
# .metric-card {
#     background: var(--card);
#     border: 1px solid var(--border);
#     border-left: 3px solid var(--gold);
#     border-radius: var(--radius);
#     padding: 1.2rem 1.5rem;
#     text-align: center;
# }
# .metric-value {
#     font-family: 'Playfair Display', serif;
#     font-size: 2rem;
#     font-weight: 700;
#     color: var(--gold2);
#     line-height: 1;
# }
# .metric-label {
#     font-size: 0.78rem;
#     color: var(--muted);
#     text-transform: uppercase;
#     letter-spacing: 0.06em;
#     margin-top: 0.35rem;
# }

# /* ── Streamlit widget overrides ───────────────────────────── */
# div[data-testid="stFileUploader"] {
#     background: #111827;
#     border: 1px dashed #2A3D55;
#     border-radius: var(--radius);
#     padding: 1rem;
# }
# div[data-testid="stFileUploader"]:hover { border-color: var(--gold); }

# .stTextInput > div > div > input,
# .stSelectbox > div > div > div {
#     background: #111827 !important;
#     border: 1px solid #2A3D55 !important;
#     color: var(--text) !important;
#     border-radius: 6px !important;
# }
# .stTextInput > div > div > input:focus {
#     border-color: var(--gold) !important;
#     box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
# }

# .stDateInput > div > div > input {
#     background: #111827 !important;
#     border: 1px solid #2A3D55 !important;
#     color: var(--text) !important;
#     border-radius: 6px !important;
# }

# /* Labels */
# .stTextInput label,
# .stSelectbox label,
# .stDateInput label {
#     color: var(--silver) !important;
#     font-size: 0.82rem !important;
#     font-weight: 500 !important;
#     letter-spacing: 0.02em !important;
#     text-transform: uppercase !important;
# }

# /* Primary buttons */
# .stButton > button[kind="primary"] {
#     background: linear-gradient(135deg, var(--gold), #A07830) !important;
#     color: #0B1120 !important;
#     border: none !important;
#     font-weight: 600 !important;
#     font-size: 0.9rem !important;
#     letter-spacing: 0.04em !important;
#     padding: 0.6rem 1.8rem !important;
#     border-radius: 6px !important;
#     transition: all 0.2s !important;
#     box-shadow: 0 2px 12px rgba(201,168,76,0.25) !important;
# }
# .stButton > button[kind="primary"]:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 4px 20px rgba(201,168,76,0.35) !important;
# }
# .stButton > button[kind="secondary"],
# .stButton > button:not([kind]) {
#     background: transparent !important;
#     color: var(--gold2) !important;
#     border: 1px solid var(--gold) !important;
#     border-radius: 6px !important;
#     font-weight: 500 !important;
#     transition: all 0.2s !important;
# }
# .stButton > button[kind="secondary"]:hover,
# .stButton > button:not([kind]):hover {
#     background: rgba(201,168,76,0.08) !important;
# }

# /* Download button */
# .stDownloadButton > button {
#     background: linear-gradient(135deg, #1A6B3C, #155230) !important;
#     color: #E8F5EE !important;
#     border: 1px solid #2ECC71 !important;
#     font-weight: 600 !important;
#     letter-spacing: 0.04em !important;
#     font-size: 0.95rem !important;
#     border-radius: 6px !important;
#     padding: 0.7rem 2rem !important;
#     box-shadow: 0 2px 12px rgba(46,204,113,0.2) !important;
#     transition: all 0.2s !important;
# }
# .stDownloadButton > button:hover {
#     transform: translateY(-1px) !important;
#     box-shadow: 0 4px 20px rgba(46,204,113,0.3) !important;
# }

# /* Expander */
# .streamlit-expanderHeader {
#     background: #111827 !important;
#     border: 1px solid var(--border) !important;
#     border-radius: var(--radius) !important;
#     color: var(--silver) !important;
#     font-size: 0.88rem !important;
#     font-weight: 500 !important;
# }
# .streamlit-expanderContent {
#     background: #0F1A27 !important;
#     border: 1px solid var(--border) !important;
#     border-top: none !important;
#     border-radius: 0 0 var(--radius) var(--radius) !important;
# }

# /* Alerts */
# .stAlert {
#     border-radius: var(--radius) !important;
#     font-size: 0.88rem !important;
# }
# div[data-testid="stInfoMessage"] {
#     background: rgba(201,168,76,0.08) !important;
#     border-left: 3px solid var(--gold) !important;
#     color: var(--gold2) !important;
# }
# div[data-testid="stSuccessMessage"] {
#     background: rgba(46,204,113,0.08) !important;
#     border-left: 3px solid var(--success) !important;
# }
# div[data-testid="stErrorMessage"] {
#     background: rgba(239,68,68,0.08) !important;
#     border-left: 3px solid var(--error) !important;
# }
# div[data-testid="stWarningMessage"] {
#     background: rgba(245,158,11,0.08) !important;
#     border-left: 3px solid var(--warn) !important;
# }

# /* Dataframe */
# .stDataFrame { border-radius: var(--radius) !important; overflow: hidden; }

# /* Divider */
# hr { border-color: var(--border) !important; }

# /* Sidebar (if used) */
# section[data-testid="stSidebar"] {
#     background: var(--navy2) !important;
#     border-right: 1px solid var(--border) !important;
# }

# /* Column group labels */
# .col-group-label {
#     font-size: 0.72rem;
#     font-weight: 600;
#     text-transform: uppercase;
#     letter-spacing: 0.08em;
#     color: var(--muted);
#     margin-bottom: 0.5rem;
#     padding-bottom: 0.25rem;
#     border-bottom: 1px solid var(--border);
# }

# /* Party file card */
# .party-card {
#     background: var(--card);
#     border: 1px solid var(--border);
#     border-radius: var(--radius);
#     padding: 1.75rem 2rem 1.5rem 2rem;
#     margin-bottom: 1.5rem;
# }
# .party-card-title {
#     font-family: 'Playfair Display', serif;
#     font-size: 1.1rem;
#     font-weight: 600;
#     color: var(--gold2);
#     margin-bottom: 0.25rem;
# }
# .party-card-meta {
#     font-size: 0.8rem;
#     color: var(--muted);
# }

# /* Step indicator */
# .step-row {
#     display: flex;
#     gap: 0;
#     margin-bottom: 2rem;
# }
# .step-item {
#     flex: 1;
#     display: flex;
#     align-items: center;
#     gap: 0.6rem;
#     padding: 0.7rem 1rem;
#     background: #111827;
#     border: 1px solid var(--border);
#     font-size: 0.82rem;
#     color: var(--muted);
#     font-weight: 500;
# }
# .step-item:first-child { border-radius: 6px 0 0 6px; }
# .step-item:last-child  { border-radius: 0 6px 6px 0; }
# .step-item.active {
#     background: rgba(201,168,76,0.08);
#     border-color: var(--gold);
#     color: var(--gold2);
# }
# .step-num {
#     width: 22px; height: 22px;
#     border-radius: 50%;
#     display: flex; align-items: center; justify-content: center;
#     font-size: 0.72rem; font-weight: 700;
#     flex-shrink: 0;
#     background: var(--border); color: var(--muted);
# }
# .step-item.active .step-num {
#     background: var(--gold); color: #0B1120;
# }

# /* Mapping grid */
# .mapping-label {
#     font-size: 0.75rem;
#     font-weight: 600;
#     color: var(--gold2);
#     text-transform: uppercase;
#     letter-spacing: 0.06em;
#     padding: 0.35rem 0.7rem;
#     background: rgba(201,168,76,0.08);
#     border-radius: 4px;
#     display: inline-block;
#     margin-bottom: 0.3rem;
# }

# /* Hide streamlit branding */
# #MainMenu, footer, header { visibility: hidden; }
# </style>
# """, unsafe_allow_html=True)


# # ============================================================
# # COMPANY STANDARD COLUMNS
# # ============================================================

# COMPANY_COLUMNS = [
#     "SELECTION DONE BY",
#     "INDIA PRICE FILLED BY",
#     "USA PRICE FILLED BY",
#     "FINAL THIS FILE BY",
#     "DATE",
#     "STONE ID",
#     "PARTY NAME",
#     "REPORT NO.",
#     "GROWTH TYPE",
#     "SHAPE",
#     "CTS",
#     "SIZE GROUP",
#     "COLOR",
#     "CLARITY",
#     "KEY",
#     "GRID",
#     "AVAILABLE",
#     "SAME",
#     "REMARK",
#     "PER CARAT",
#     "TOTAL AMT",
#     "VDB PRICE INDIA",
#     "VDB AMOUNT INDIA",
#     "VDB PRICE USA",
#     "VDB AMOUNT USA",
#     "WITH TARIFF COST",
#     "WITH TARIFF AMOUNT",
#     "IND%",
#     "USA%",
#     "AFTER TARIFF DIFF$"
# ]

# PARTY_FIELDS = [
#     "STONE ID",
#     "REPORT NO.",
#     "GROWTH TYPE",
#     "SHAPE",
#     "CTS",
#     "COLOR",
#     "CLARITY",
#     "PER CARAT",
#     "VDB PRICE INDIA",
#     "VDB PRICE USA"
# ]

# FIELD_TO_COMPANY_COLUMN = {
#     "STONE ID": "STONE ID",
#     "REPORT NO.": "REPORT NO.",
#     "GROWTH TYPE": "GROWTH TYPE",
#     "SHAPE": "SHAPE",
#     "CTS": "CTS",
#     "COLOR": "COLOR",
#     "CLARITY": "CLARITY",
#     "PER CARAT": "PER CARAT",
#     "VDB PRICE INDIA": "VDB PRICE INDIA",
#     "VDB PRICE USA": "VDB PRICE USA"
# }

# if "converted_files" not in st.session_state:
#     st.session_state.converted_files = {}


# # ============================================================
# # UTILITIES
# # ============================================================

# def normalize_column_name(value):
#     if value is None:
#         return ""
#     return (
#         str(value)
#         .strip()
#         .upper()
#         .replace("\n", " ")
#         .replace("_", " ")
#     )

# def find_column(df, wanted_name):
#     wanted = normalize_column_name(wanted_name)
#     for column in df.columns:
#         if normalize_column_name(column) == wanted:
#             return column
#     return None

# def read_excel(file):
#     file.seek(0)
#     return pd.read_excel(file, engine="openpyxl")

# def validate_company_format(columns):
#     actual = [normalize_column_name(c) for c in columns]
#     required = [normalize_column_name(c) for c in COMPANY_COLUMNS]
#     return [c for c in required if c not in actual]

# def get_size_group(cts):
#     """Return the SIZE GROUP using the user's supplied Excel IFS ranges."""
#     if pd.isna(cts):
#         return ""
#     try:
#         cts = float(cts)
#     except (ValueError, TypeError):
#         return ""

#     # Keep the ranges and labels exactly aligned with the supplied IFS formula.
#     size_groups = [
#         (0.30, 0.49, "0.30 - 0.49"),
#         (0.50, 0.59, "0.50 - 0.59"),
#         (0.60, 0.69, "0.60 - 0.69"),
#         (0.70, 0.79, "0.70 - 0.79"),
#         (0.80, 0.89, "0.80 - 0.89"),
#         (0.90, 0.94, "0.90 - 0.94"),
#         (0.95, 0.99, "0.95 - 0.99"),
#         (1.00, 1.10, "1.00 - 1.10"),
#         (1.11, 1.19, "1.11 - 1.19"),
#         (1.20, 1.29, "1.20 - 1.29"),
#         (1.30, 1.39, "1.30 - 1.39"),
#         (1.40, 1.49, "1.40 - 1.49"),
#         (1.50, 1.59, "1.50 - 1.59"),
#         (1.60, 1.69, "1.60 - 1.69"),
#         (1.70, 1.79, "1.70 - 1.79"),
#         (1.80, 1.89, "1.80 - 1.89"),
#         (1.90, 1.99, "1.90 - 1.99"),
#         (2.00, 2.09, "2.00 - 2.09"),
#         (2.10, 2.19, "2.10 - 2.19"),
#         (2.20, 2.29, "2.20 - 2.29"),
#         (2.30, 2.39, "2.30 - 2.39"),
#         (2.40, 2.49, "2.40 - 2.49"),
#         (2.50, 2.59, "2.50 - 2.59"),
#         (2.60, 2.69, "2.60 - 2.69"),
#         (2.70, 2.79, "2.70 - 2.79"),
#         (2.80, 2.89, "2.80 - 2.89"),
#         (2.90, 2.99, "2.90 - 2.99"),
#         (3.00, 3.09, "3.00 - 3.09"),
#         (3.10, 3.19, "3.10 - 3.19"),
#         (3.20, 3.29, "3.20 - 3.29"),
#         (3.30, 3.39, "3.30 - 3.39"),
#         (3.40, 3.49, "3.40 - 3.49"),
#         (3.50, 3.59, "3.50 - 3.59"),
#         (3.60, 3.69, "3.60 - 3.69"),
#         (3.70, 3.79, "3.70 - 3.79"),
#         (3.80, 3.89, "3.80 - 3.89"),
#         (3.90, 3.99, "3.90 - 3.99"),
#         (4.00, 4.10, "4.00 - 4.10"),
#         (4.50, 4.59, "4.50 - 4.59"),
#         (5.00, 5.10, "5.00 - 5.10"),
#         (5.50, 5.59, "5.50 - 5.59"),
#         (6.00, 6.10, "6.00 - 6.10"),
#         (6.50, 6.59, "6.50 - 6.59"),
#         (7.00, 7.10, "7.00 - 7.10"),
#         (8.00, 8.10, "8.00 - 8.10"),
#         (9.00, 9.10, "9.00 - 9.10"),
#         (10.00, 10.10, "10.00 - 10.10"),
#         (11.00, 11.10, "11.00 - 11.10"),
#         (12.00, 12.10, "12.00 - 12.10"),
#         (13.00, 13.10, "13.00 - 13.10"),
#         (14.00, 14.10, "14.00 - 14.10"),
#         (15.00, 15.10, "15.00 - 15.10"),
#         (16.00, 16.10, "16.00 - 16.10"),
#         (17.00, 17.10, "17.00 - 17.10"),
#         (18.00, 18.10, "18.00 - 18.10"),
#         (19.00, 19.10, "19.00 - 19.10"),
#         (20.00, 21.99, "20.00 - 21.99"),
#     ]

#     for lower, upper, label in size_groups:
#         if lower <= cts <= upper:
#             return label

#     return "Out of Range"

# def create_blank_output(number_of_rows):
#     return pd.DataFrame("", index=range(number_of_rows), columns=COMPANY_COLUMNS)


# # ============================================================
# # CONVERT PARTY FILE  (unchanged logic)
# # ============================================================

# def convert_party_file(
#     party_df, master_df, mapping, party_name,
#     selection_done_by, india_price_filled_by,
#     usa_price_filled_by, final_file_by, selected_date
# ):
#     output = create_blank_output(len(party_df))

#     output["SELECTION DONE BY"]   = selection_done_by
#     output["INDIA PRICE FILLED BY"] = india_price_filled_by
#     output["USA PRICE FILLED BY"]  = usa_price_filled_by
#     output["FINAL THIS FILE BY"]   = final_file_by
#     output["DATE"]                 = selected_date
#     output["PARTY NAME"]           = party_name

#     for party_field, party_column in mapping.items():
#         if party_column is None:
#             continue
#         if party_column == "-- Select Party Column --":
#             continue
#         if party_column not in party_df.columns:
#             continue
#         company_column = FIELD_TO_COMPANY_COLUMN[party_field]
#         output[company_column] = party_df[party_column].reset_index(drop=True)

#     output["SIZE GROUP"] = output["CTS"].apply(get_size_group)

#     for column in ["SHAPE", "SIZE GROUP", "COLOR", "CLARITY"]:
#         output[column] = output[column].fillna("").astype(str).str.strip()

#     output["KEY"] = (
#         output["SHAPE"]
#         + output["SIZE GROUP"]
#         + output["COLOR"]
#         + output["CLARITY"]
#     )

#     master = master_df.copy()
#     master_key_column       = find_column(master, "KEY")
#     master_grid_column      = find_column(master, "GRID")
#     master_available_column = find_column(master, "AVAILABLE")

#     if master_key_column is None:
#         raise ValueError("Master File does not contain a KEY column.")
#     if master_grid_column is None:
#         raise ValueError("Master File does not contain a Grid column.")
#     if master_available_column is None:
#         raise ValueError("Master File does not contain an Available column.")

#     master_lookup = master[[master_key_column, master_grid_column, master_available_column]].copy()
#     master_lookup.columns = ["MASTER_KEY", "MASTER_GRID", "MASTER_AVAILABLE"]
#     master_lookup["MASTER_KEY"] = master_lookup["MASTER_KEY"].fillna("").astype(str).str.strip()
#     master_lookup["MASTER_GRID"] = pd.to_numeric(master_lookup["MASTER_GRID"], errors="coerce").fillna(0)
#     master_lookup["MASTER_AVAILABLE"] = pd.to_numeric(master_lookup["MASTER_AVAILABLE"], errors="coerce").fillna(0)
#     master_lookup = master_lookup.drop_duplicates(subset=["MASTER_KEY"], keep="first")

#     output = output.merge(master_lookup, left_on="KEY", right_on="MASTER_KEY", how="left")
#     output["GRID"]      = pd.to_numeric(output["MASTER_GRID"], errors="coerce").fillna(0)
#     output["AVAILABLE"] = pd.to_numeric(output["MASTER_AVAILABLE"], errors="coerce").fillna(0)
#     output.drop(columns=["MASTER_KEY", "MASTER_GRID", "MASTER_AVAILABLE"], inplace=True, errors="ignore")

#     output["SAME"]   = ""
#     output["REMARK"] = ""

#     for column in ["TOTAL AMT", "VDB AMOUNT INDIA", "VDB AMOUNT USA",
#                    "WITH TARIFF COST", "WITH TARIFF AMOUNT", "IND%", "USA%", "AFTER TARIFF DIFF$"]:
#         output[column] = ""

#     for column in COMPANY_COLUMNS:
#         if column not in output.columns:
#             output[column] = ""

#     output = output[COMPANY_COLUMNS].reset_index(drop=True)
#     return output


# # ============================================================
# # CREATE DOWNLOAD EXCEL  (unchanged logic)
# # ============================================================

# def create_download_excel(df):
#     output = BytesIO()
#     df = df.copy()
#     df.columns = [str(c).strip() for c in df.columns]

#     for column in COMPANY_COLUMNS:
#         if str(column).strip() not in df.columns:
#             df[str(column).strip()] = ""

#     df = df[[str(c).strip() for c in COMPANY_COLUMNS]]

#     with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
#         df.to_excel(writer, index=False, sheet_name="Final File")
#         workbook  = writer.book
#         worksheet = writer.sheets["Final File"]

#         header_format = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True})

#         header_size_grid_same = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#fcba03"})
#         header_per_carat_total = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#5aa6c7"})
#         header_india = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#b592d6"})
#         header_usa = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#6aba95"})
#         header_tariff = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#c27676"})
#         header_difference = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#f8fc03"})

#         normal_format  = workbook.add_format({"border": 1, "valign": "vcenter"})
#         number_format  = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "0.00"})
#         integer_format = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "0"})
#         date_format    = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "dd-mm-yyyy"})

#         size_grid_same_format  = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#fcba03"})
#         per_carat_total_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#5aa6c7", "num_format": "0.00"})
#         india_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#b592d6", "num_format": "0.00"})
#         usa_format   = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#6aba95", "num_format": "0.00"})
#         tariff_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#c27676", "num_format": "0.00"})

#         same_formula_format       = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#fcba03", "num_format": "0"})
#         total_formula_format      = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#5aa6c7", "num_format": "0.00"})
#         vdb_india_formula_format  = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#b592d6", "num_format": "0.00"})
#         vdb_usa_formula_format    = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#6aba95", "num_format": "0.00"})
#         tariff_formula_format     = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#c27676", "num_format": "0.00"})
#         difference_formula_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#f8fc03", "num_format": "0.00"})

#         column_numbers = {str(c).strip(): i for i, c in enumerate(df.columns)}

#         formula_columns = [
#             "KEY", "SAME", "TOTAL AMT", "VDB AMOUNT INDIA", "VDB AMOUNT USA",
#             "WITH TARIFF COST", "WITH TARIFF AMOUNT", "IND%", "USA%", "AFTER TARIFF DIFF$"
#         ]

#         for col_number, column in enumerate(df.columns):
#             column_name = str(column).strip()
#             if column_name in ["SIZE GROUP", "GRID", "AVAILABLE", "SAME"]:
#                 fmt = header_size_grid_same
#             elif column_name in ["PER CARAT", "TOTAL AMT"]:
#                 fmt = header_per_carat_total
#             elif column_name in ["VDB PRICE INDIA", "VDB AMOUNT INDIA"]:
#                 fmt = header_india
#             elif column_name in ["VDB PRICE USA", "VDB AMOUNT USA"]:
#                 fmt = header_usa
#             elif column_name in ["WITH TARIFF COST", "WITH TARIFF AMOUNT"]:
#                 fmt = header_tariff
#             elif column_name in ["IND%", "USA%", "AFTER TARIFF DIFF$"]:
#                 fmt = header_difference
#             else:
#                 fmt = header_format
#             worksheet.write(0, col_number, column_name, fmt)

#         for row_number in range(len(df)):
#             for col_number, column in enumerate(df.columns):
#                 column_name = str(column).strip()
#                 if column_name in formula_columns:
#                     continue
#                 value = df.iloc[row_number, col_number]
#                 if pd.isna(value):
#                     value = ""
#                 if column_name == "DATE":
#                     worksheet.write(row_number + 1, col_number, value, date_format)
#                 elif column_name == "SIZE GROUP":
#                     worksheet.write(row_number + 1, col_number, value, size_grid_same_format)
#                 elif column_name in ["GRID", "AVAILABLE"]:
#                     worksheet.write(row_number + 1, col_number, value, size_grid_same_format)
#                 elif column_name == "PER CARAT":
#                     worksheet.write(row_number + 1, col_number, value, per_carat_total_format)
#                 elif column_name == "VDB PRICE INDIA":
#                     worksheet.write(row_number + 1, col_number, value, india_format)
#                 elif column_name == "VDB PRICE USA":
#                     worksheet.write(row_number + 1, col_number, value, usa_format)
#                 elif column_name in ["WITH TARIFF COST"]:
#                     worksheet.write(row_number + 1, col_number, value, tariff_format)
#                 else:
#                     worksheet.write(row_number + 1, col_number, value, normal_format)

#         for row_number in range(len(df)):
#             excel_row = row_number + 2
#             worksheet.write_formula(row_number + 1, column_numbers["KEY"],
#                 f'=CONCATENATE(J{excel_row},L{excel_row},M{excel_row},N{excel_row})', normal_format)
#             worksheet.write_formula(row_number + 1, column_numbers["SAME"],
#                 f'=COUNTIF(O:O,O{excel_row})', same_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["TOTAL AMT"],
#                 f'=ROUND((T{excel_row}*K{excel_row}),2)', total_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["VDB AMOUNT INDIA"],
#                 f'=ROUND((V{excel_row}*K{excel_row}),2)', vdb_india_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["VDB AMOUNT USA"],
#                 f'=ROUND((X{excel_row}*K{excel_row}),2)', vdb_usa_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["WITH TARIFF COST"],
#                 f'=ROUND((T{excel_row}*1.08),2)', tariff_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["WITH TARIFF AMOUNT"],
#                 f'=ROUND((Z{excel_row}*K{excel_row}),2)', tariff_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["IND%"],
#                 f'=IFERROR(ROUND((100-(T{excel_row}*100)/V{excel_row}),2),"")', difference_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["USA%"],
#                 f'=IFERROR(ROUND((100-(Z{excel_row}*100)/X{excel_row}),2),"")', difference_formula_format)
#             worksheet.write_formula(row_number + 1, column_numbers["AFTER TARIFF DIFF$"],
#                 f'=X{excel_row}-Z{excel_row}', difference_formula_format)

#         for col_number, column in enumerate(df.columns):
#             max_length = len(str(column))
#             if len(df) > 0:
#                 for value in df[column].head(100):
#                     if pd.notna(value):
#                         max_length = max(max_length, len(str(value)))
#             worksheet.set_column(col_number, col_number, min(max(max_length + 2, 12), 35))

#         worksheet.freeze_panes(1, 0)
#         if len(df.columns) > 0:
#             worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
#         workbook.set_calc_mode("auto")

#     output.seek(0)
#     return output


# # ============================================================
# # HERO BANNER
# # ============================================================

# st.markdown("""
# <div class="hero-banner">
#     <div class="hero-title">◆ Diamond Format Converter</div>
#     <div class="hero-subtitle">
#         Transform any Party Excel file into Company Standard Format — with Master pricing, tariff calculations, and formula-ready output
#     </div>
# </div>
# """, unsafe_allow_html=True)


# # ============================================================
# # STEP INDICATOR
# # ============================================================

# files_uploaded  = False
# files_converted = bool(st.session_state.converted_files)

# st.markdown("""
# <div class="step-row">
#     <div class="step-item active">
#         <div class="step-num">1</div>
#         Upload Files
#     </div>
#     <div class="step-item">
#         <div class="step-num">2</div>
#         Map &amp; Convert Party Files
#     </div>
#     <div class="step-item">
#         <div class="step-num">3</div>
#         Download Final File
#     </div>
# </div>
# """, unsafe_allow_html=True)


# # ============================================================
# # STEP 1 — UPLOAD FILES
# # ============================================================

# st.markdown("""
# <div class="section-header">
#     <span class="section-badge">Step 1</span>
#     <span class="section-title">Upload Files</span>
# </div>
# """, unsafe_allow_html=True)

# col1, col2 = st.columns(2)

# with col1:
#     st.markdown('<div class="col-group-label">Company &amp; Master Files</div>', unsafe_allow_html=True)
#     company_file = st.file_uploader(
#         "Company Standard Format",
#         type=["xlsx", "xls"],
#         key="company_file",
#         help="Upload your company's standard Excel template"
#     )
#     master_file = st.file_uploader(
#         "Master Report",
#         type=["xlsx", "xls"],
#         key="master_file",
#         help="Upload the master pricing report with KEY, GRID & AVAILABLE columns"
#     )

# with col2:
#     st.markdown('<div class="col-group-label">Party Files (multiple allowed)</div>', unsafe_allow_html=True)
#     party_files = st.file_uploader(
#         "Party Files",
#         type=["xlsx", "xls"],
#         accept_multiple_files=True,
#         key="party_files",
#         help="Upload one or more party Excel files to convert"
#     )


# # ── Upload Status ──────────────────────────────────────────

# status_html = '<div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin:1rem 0;">'
# status_html += f'<span class="chip {"chip-success" if company_file else "chip-warn"}">{"✓" if company_file else "○"} Company Format</span>'
# status_html += f'<span class="chip {"chip-success" if master_file else "chip-warn"}">{"✓" if master_file else "○"} Master Report</span>'
# status_html += f'<span class="chip {"chip-success" if party_files else "chip-warn"}">{"✓" if party_files else "○"} Party Files ({len(party_files) if party_files else 0} uploaded)</span>'
# status_html += '</div>'
# st.markdown(status_html, unsafe_allow_html=True)

# if company_file is None:
#     st.info("⬆️  Upload your Company Standard Format file to continue.")
#     st.stop()

# if master_file is None:
#     st.info("⬆️  Upload the Master Report file to continue.")
#     st.stop()

# if not party_files:
#     st.info("⬆️  Upload at least one Party File to convert.")
#     st.stop()


# # ── Read & Validate ────────────────────────────────────────

# try:
#     company_df = read_excel(company_file)
# except Exception as e:
#     st.error(f"Cannot read Company Standard Format: {e}")
#     st.stop()

# missing_cols = validate_company_format(company_df.columns)
# if missing_cols:
#     st.error("Company Standard Format is missing required columns:")
#     for c in missing_cols:
#         st.write(f"  ❌ {c}")
#     st.stop()

# try:
#     master_df = read_excel(master_file)
# except Exception as e:
#     st.error(f"Cannot read Master Report: {e}")
#     st.stop()

# master_key_column       = find_column(master_df, "KEY")
# master_grid_column      = find_column(master_df, "GRID")
# master_available_column = find_column(master_df, "AVAILABLE")

# if not master_key_column:
#     st.error("❌ Master Report is missing the KEY column.")
#     st.stop()
# if not master_grid_column:
#     st.error("❌ Master Report is missing the GRID column.")
#     st.stop()
# if not master_available_column:
#     st.error("❌ Master Report is missing the AVAILABLE column.")
#     st.stop()


# # ── File Preview Cards ─────────────────────────────────────

# preview_col1, preview_col2 = st.columns(2)

# with preview_col1:
#     with st.expander("👁  Company Standard Format — Preview", expanded=False):
#         st.markdown(f'<span class="chip chip-success">✓ {len(company_df.columns)} columns validated</span>', unsafe_allow_html=True)
#         st.dataframe(company_df.head(10), use_container_width=True)

# with preview_col2:
#     with st.expander("📊 Master Report — Preview", expanded=False):
#         st.markdown(
#             f'<span class="chip chip-info">KEY: {master_key_column}</span>'
#             f'<span class="chip chip-info">GRID: {master_grid_column}</span>'
#             f'<span class="chip chip-info">AVAIL: {master_available_column}</span>'
#             f'<span class="chip chip-success">{len(master_df):,} rows</span>',
#             unsafe_allow_html=True
#         )
#         st.dataframe(master_df.head(15), use_container_width=True)


# # ============================================================
# # STEP 2 — PARTY FILE CONVERSION
# # ============================================================

# st.markdown("""
# <div class="section-header">
#     <span class="section-badge">Step 2</span>
#     <span class="section-title">Map &amp; Convert Party Files</span>
# </div>
# """, unsafe_allow_html=True)

# for file_index, party_file in enumerate(party_files):

#     st.markdown(f"""
#     <div class="party-card">
#         <div class="party-card-title">◇ {party_file.name}</div>
#         <div class="party-card-meta">Party File {file_index + 1} of {len(party_files)}</div>
#     </div>
#     """, unsafe_allow_html=True)

#     try:
#         party_df = read_excel(party_file)
#     except Exception as e:
#         st.error(f"Cannot read {party_file.name}: {e}")
#         continue

#     party_columns = list(party_df.columns)

#     # ── File Information ──────────────────────────────────
#     st.markdown('<div class="col-group-label" style="margin-top:0.5rem;">File Information</div>', unsafe_allow_html=True)

#     info_col1, info_col2, info_col3 = st.columns(3)

#     with info_col1:
#         selection_done_by = st.text_input(
#             "Selection Done By",
#             placeholder="Person name",
#             key=f"selection_done_by_{file_index}"
#         )
#         india_price_filled_by = st.text_input(
#             "India Price Filled By",
#             placeholder="Person name",
#             key=f"india_price_filled_by_{file_index}"
#         )

#     with info_col2:
#         usa_price_filled_by = st.text_input(
#             "USA Price Filled By",
#             placeholder="Person name",
#             key=f"usa_price_filled_by_{file_index}"
#         )
#         final_file_by = st.text_input(
#             "Final File By",
#             placeholder="Person name",
#             key=f"final_file_by_{file_index}"
#         )

#     with info_col3:
#         party_name = st.text_input(
#             "Party Name",
#             placeholder="Enter party name",
#             key=f"party_name_{file_index}"
#         )
#         selected_date = st.date_input(
#             "Date",
#             value=date.today(),
#             key=f"selected_date_{file_index}"
#         )

#     # ── Party Preview ─────────────────────────────────────
#     with st.expander(f"👁  Preview — {party_file.name}", expanded=False):
#         st.markdown(
#             f'<span class="chip chip-info">{len(party_df):,} rows</span>'
#             f'<span class="chip chip-info">{len(party_columns)} columns</span>',
#             unsafe_allow_html=True
#         )
#         st.dataframe(party_df.head(15), use_container_width=True)

#     # ── Column Mapping ────────────────────────────────────
#     st.markdown('<div class="col-group-label" style="margin-top:1.25rem;">Column Mapping — Match party columns to company fields</div>', unsafe_allow_html=True)

#     mapping = {}
#     cols = st.columns(2)

#     for field_index, field in enumerate(PARTY_FIELDS):
#         container = cols[field_index % 2]
#         with container:
#             mapping[field] = st.selectbox(
#                 field,
#                 options=["-- Select Party Column --"] + party_columns,
#                 key=f"mapping_{file_index}_{field_index}"
#             )

#     missing_mapping = [
#         f for f, c in mapping.items()
#         if c == "-- Select Party Column --"
#     ]

#     if missing_mapping:
#         st.markdown(
#             f'<div style="margin-top:0.5rem;"><span class="chip chip-warn">⚠ {len(missing_mapping)} field(s) unmapped</span></div>',
#             unsafe_allow_html=True
#         )
#     else:
#         st.markdown(
#             '<div style="margin-top:0.5rem;"><span class="chip chip-success">✓ All columns mapped</span></div>',
#             unsafe_allow_html=True
#         )

#     st.write("")
#     convert_button = st.button(
#         f"◆  Convert  {party_file.name}",
#         key=f"convert_{file_index}",
#         type="primary"
#     )

#     if convert_button:
#         errors = []
#         if not selection_done_by.strip():   errors.append("Selection Done By is required.")
#         if not india_price_filled_by.strip(): errors.append("India Price Filled By is required.")
#         if not usa_price_filled_by.strip():  errors.append("USA Price Filled By is required.")
#         if not final_file_by.strip():        errors.append("Final File By is required.")
#         if not party_name.strip():           errors.append("Party Name is required.")
#         if missing_mapping:                  errors.append("All party columns must be mapped.")

#         selected_vals = [c for c in mapping.values() if c != "-- Select Party Column --"]
#         if len(selected_vals) != len(set(selected_vals)):
#             errors.append("Each party column should be mapped only once.")

#         if errors:
#             st.error("Fix the following before converting:")
#             for err in errors:
#                 st.write(f"  ❌ {err}")
#             continue

#         try:
#             output_df = convert_party_file(
#                 party_df=party_df,
#                 master_df=master_df,
#                 mapping=mapping,
#                 party_name=party_name,
#                 selection_done_by=selection_done_by,
#                 india_price_filled_by=india_price_filled_by,
#                 usa_price_filled_by=usa_price_filled_by,
#                 final_file_by=final_file_by,
#                 selected_date=selected_date
#             )
#         except Exception as e:
#             st.error(f"Conversion failed: {e}")
#             continue

#         st.session_state.converted_files[file_index] = {
#             "file_name": party_file.name,
#             "party_name": party_name,
#             "data": output_df
#         }

#         st.success(f"✓ {party_file.name} converted — {len(output_df):,} rows ready.")

#         with st.expander("📊 Converted Data Preview", expanded=True):
#             st.dataframe(output_df.head(20), use_container_width=True)

#     st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)


# # ============================================================
# # STEP 3 — FINAL FILE
# # ============================================================

# if st.session_state.converted_files:

#     st.markdown("""
#     <div class="section-header">
#         <span class="section-badge">Step 3</span>
#         <span class="section-title">Final Company Standard File</span>
#     </div>
#     """, unsafe_allow_html=True)

#     converted_data = [item["data"] for item in st.session_state.converted_files.values()]
#     final_df = pd.concat(converted_data, ignore_index=True)

#     for column in COMPANY_COLUMNS:
#         if column not in final_df.columns:
#             final_df[column] = ""
#     final_df = final_df[COMPANY_COLUMNS]

#     # ── Summary Metrics ───────────────────────────────────
#     m1, m2, m3 = st.columns(3)
#     with m1:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{len(converted_data)}</div>
#             <div class="metric-label">Party Files Converted</div>
#         </div>""", unsafe_allow_html=True)
#     with m2:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{len(final_df):,}</div>
#             <div class="metric-label">Total Stones</div>
#         </div>""", unsafe_allow_html=True)
#     with m3:
#         st.markdown(f"""
#         <div class="metric-card">
#             <div class="metric-value">{len(COMPANY_COLUMNS)}</div>
#             <div class="metric-label">Output Columns</div>
#         </div>""", unsafe_allow_html=True)

#     st.write("")

#     # ── Final Preview ─────────────────────────────────────
#     st.markdown('<div class="col-group-label">Final Data Preview</div>', unsafe_allow_html=True)
#     st.dataframe(final_df, use_container_width=True, height=460)

#     st.write("")

#     # ── Download ──────────────────────────────────────────
#     excel_data = create_download_excel(final_df)

#     st.download_button(
#         label="⬇  Download Company Standard File  (.xlsx)",
#         data=excel_data,
#         file_name="Company_Standard_Final.xlsx",
#         mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#         type="primary",
#         use_container_width=True
#     )

#     st.markdown("""
#     <div style="text-align:center; margin-top:1rem; font-size:0.78rem; color:#4A6070;">
#         Excel formulas, color-coded columns, freeze panes, and auto-filter are included in the downloaded file.
#     </div>
#     """, unsafe_allow_html=True)





import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Diamond Format Converter",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS — Professional Dark Luxury Theme
# ============================================================

st.markdown("""
<style>
/* ── Google Fonts ─────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root Variables ───────────────────────────────────────── */
:root {
    --navy:    #0B1120;
    --navy2:   #111827;
    --card:    #161F30;
    --border:  #1E2D45;
    --gold:    #C9A84C;
    --gold2:   #E5C97A;
    --silver:  #8EA6BF;
    --text:    #E8EEF5;
    --muted:   #6B7E93;
    --success: #2ECC71;
    --warn:    #F59E0B;
    --error:   #EF4444;
    --radius:  10px;
}

/* ── App Background ───────────────────────────────────────── */
.stApp {
    background: var(--navy) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text);
}

/* ── Main block padding ───────────────────────────────────── */
.block-container {
    padding: 2rem 3rem 4rem 3rem !important;
    max-width: 1300px;
}

/* ── Hero Banner ──────────────────────────────────────────── */
.hero-banner {
    background: linear-gradient(135deg, #0D1B2E 0%, #162033 50%, #0D1B2E 100%);
    border: 1px solid var(--border);
    border-top: 3px solid var(--gold);
    border-radius: var(--radius);
    padding: 2.5rem 3rem;
    margin-bottom: 2.5rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: "◆";
    position: absolute;
    right: 2.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 7rem;
    color: rgba(201,168,76,0.06);
    pointer-events: none;
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.1rem;
    font-weight: 700;
    color: var(--gold2);
    margin: 0 0 0.4rem 0;
    letter-spacing: 0.01em;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: var(--silver);
    margin: 0;
    font-weight: 300;
}

/* ── Section Headers ──────────────────────────────────────── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.2rem 0 1.2rem 0;
    padding-bottom: 0.65rem;
    border-bottom: 1px solid var(--border);
}
.section-badge {
    background: linear-gradient(135deg, var(--gold), #A07830);
    color: #0B1120;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text);
    margin: 0;
}

/* ── Cards ────────────────────────────────────────────────── */
.info-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.upload-zone {
    background: linear-gradient(135deg, #111827 0%, #0D1926 100%);
    border: 1px dashed #2A3D55;
    border-radius: var(--radius);
    padding: 1.75rem 1.5rem;
    text-align: center;
    transition: border-color 0.2s;
}
.upload-zone:hover { border-color: var(--gold); }

/* ── Status Chips ─────────────────────────────────────────── */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.78rem;
    font-weight: 500;
    padding: 0.3rem 0.75rem;
    border-radius: 20px;
    margin: 0.2rem;
}
.chip-success { background: rgba(46,204,113,0.12); color: #2ECC71; border: 1px solid rgba(46,204,113,0.25); }
.chip-warn    { background: rgba(245,158,11,0.12); color: #F59E0B; border: 1px solid rgba(245,158,11,0.25); }
.chip-error   { background: rgba(239,68,68,0.12);  color: #EF4444; border: 1px solid rgba(239,68,68,0.25); }
.chip-info    { background: rgba(201,168,76,0.10); color: var(--gold2); border: 1px solid rgba(201,168,76,0.2); }

/* ── Metric Cards ─────────────────────────────────────────── */
.metric-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--gold);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    font-weight: 700;
    color: var(--gold2);
    line-height: 1;
}
.metric-label {
    font-size: 0.78rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 0.35rem;
}

/* ── Streamlit widget overrides ───────────────────────────── */
div[data-testid="stFileUploader"] {
    background: #111827;
    border: 1px dashed #2A3D55;
    border-radius: var(--radius);
    padding: 1rem;
}
div[data-testid="stFileUploader"]:hover { border-color: var(--gold); }

.stTextInput > div > div > input,
.stSelectbox > div > div > div {
    background: #111827 !important;
    border: 1px solid #2A3D55 !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}

.stDateInput > div > div > input {
    background: #111827 !important;
    border: 1px solid #2A3D55 !important;
    color: var(--text) !important;
    border-radius: 6px !important;
}

/* Labels */
.stTextInput label,
.stSelectbox label,
.stDateInput label {
    color: var(--silver) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.02em !important;
    text-transform: uppercase !important;
}

/* Primary buttons */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--gold), #A07830) !important;
    color: #0B1120 !important;
    border: none !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    padding: 0.6rem 1.8rem !important;
    border-radius: 6px !important;
    transition: all 0.2s !important;
    box-shadow: 0 2px 12px rgba(201,168,76,0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(201,168,76,0.35) !important;
}
.stButton > button[kind="secondary"],
.stButton > button:not([kind]) {
    background: transparent !important;
    color: var(--gold2) !important;
    border: 1px solid var(--gold) !important;
    border-radius: 6px !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="secondary"]:hover,
.stButton > button:not([kind]):hover {
    background: rgba(201,168,76,0.08) !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, #1A6B3C, #155230) !important;
    color: #E8F5EE !important;
    border: 1px solid #2ECC71 !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    font-size: 0.95rem !important;
    border-radius: 6px !important;
    padding: 0.7rem 2rem !important;
    box-shadow: 0 2px 12px rgba(46,204,113,0.2) !important;
    transition: all 0.2s !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(46,204,113,0.3) !important;
}

/* Expander */
.streamlit-expanderHeader {
    background: #111827 !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--silver) !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
}
.streamlit-expanderContent {
    background: #0F1A27 !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius) var(--radius) !important;
}

/* Alerts */
.stAlert {
    border-radius: var(--radius) !important;
    font-size: 0.88rem !important;
}
div[data-testid="stInfoMessage"] {
    background: rgba(201,168,76,0.08) !important;
    border-left: 3px solid var(--gold) !important;
    color: var(--gold2) !important;
}
div[data-testid="stSuccessMessage"] {
    background: rgba(46,204,113,0.08) !important;
    border-left: 3px solid var(--success) !important;
}
div[data-testid="stErrorMessage"] {
    background: rgba(239,68,68,0.08) !important;
    border-left: 3px solid var(--error) !important;
}
div[data-testid="stWarningMessage"] {
    background: rgba(245,158,11,0.08) !important;
    border-left: 3px solid var(--warn) !important;
}

/* Dataframe */
.stDataFrame { border-radius: var(--radius) !important; overflow: hidden; }

/* Divider */
hr { border-color: var(--border) !important; }

/* Sidebar (if used) */
section[data-testid="stSidebar"] {
    background: var(--navy2) !important;
    border-right: 1px solid var(--border) !important;
}

/* Column group labels */
.col-group-label {
    font-size: 0.72rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--muted);
    margin-bottom: 0.5rem;
    padding-bottom: 0.25rem;
    border-bottom: 1px solid var(--border);
}

/* Party file card */
.party-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.75rem 2rem 1.5rem 2rem;
    margin-bottom: 1.5rem;
}
.party-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--gold2);
    margin-bottom: 0.25rem;
}
.party-card-meta {
    font-size: 0.8rem;
    color: var(--muted);
}

/* Step indicator */
.step-row {
    display: flex;
    gap: 0;
    margin-bottom: 2rem;
}
.step-item {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.7rem 1rem;
    background: #111827;
    border: 1px solid var(--border);
    font-size: 0.82rem;
    color: var(--muted);
    font-weight: 500;
}
.step-item:first-child { border-radius: 6px 0 0 6px; }
.step-item:last-child  { border-radius: 0 6px 6px 0; }
.step-item.active {
    background: rgba(201,168,76,0.08);
    border-color: var(--gold);
    color: var(--gold2);
}
.step-num {
    width: 22px; height: 22px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.72rem; font-weight: 700;
    flex-shrink: 0;
    background: var(--border); color: var(--muted);
}
.step-item.active .step-num {
    background: var(--gold); color: #0B1120;
}

/* Mapping grid */
.mapping-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--gold2);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.35rem 0.7rem;
    background: rgba(201,168,76,0.08);
    border-radius: 4px;
    display: inline-block;
    margin-bottom: 0.3rem;
}

/* Hide streamlit branding */
#MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ============================================================
# COMPANY STANDARD COLUMNS
# ============================================================

COMPANY_COLUMNS = [
    "SELECTION DONE BY",
    "INDIA PRICE FILLED BY",
    "USA PRICE FILLED BY",
    "FINAL THIS FILE BY",
    "DATE",
    "STONE ID",
    "PARTY NAME",
    "REPORT NO.",
    "GROWTH TYPE",
    "SHAPE",
    "CTS",
    "SIZE GROUP",
    "COLOR",
    "CLARITY",
    "KEY",
    "GRID",
    "AVAILABLE",
    "SAME",
    "REMARK",
    "PER CARAT",
    "TOTAL AMT",
    "VDB PRICE INDIA",
    "VDB AMOUNT INDIA",
    "VDB PRICE USA",
    "VDB AMOUNT USA",
    "WITH TARIFF COST",
    "WITH TARIFF AMOUNT",
    "IND%",
    "USA%",
    "AFTER TARIFF DIFF$"
]

PARTY_FIELDS = [
    "STONE ID",
    "REPORT NO.",
    "GROWTH TYPE",
    "SHAPE",
    "CTS",
    "COLOR",
    "CLARITY",
    "PER CARAT",
    "VDB PRICE INDIA",
    "VDB PRICE USA"
]

FIELD_TO_COMPANY_COLUMN = {
    "STONE ID": "STONE ID",
    "REPORT NO.": "REPORT NO.",
    "GROWTH TYPE": "GROWTH TYPE",
    "SHAPE": "SHAPE",
    "CTS": "CTS",
    "COLOR": "COLOR",
    "CLARITY": "CLARITY",
    "PER CARAT": "PER CARAT",
    "VDB PRICE INDIA": "VDB PRICE INDIA",
    "VDB PRICE USA": "VDB PRICE USA"
}

if "converted_files" not in st.session_state:
    st.session_state.converted_files = {}


# ============================================================
# UTILITIES
# ============================================================

def normalize_column_name(value):
    if value is None:
        return ""
    return (
        str(value)
        .strip()
        .upper()
        .replace("\n", " ")
        .replace("_", " ")
    )

def find_column(df, wanted_name):
    wanted = normalize_column_name(wanted_name)
    for column in df.columns:
        if normalize_column_name(column) == wanted:
            return column
    return None

def read_excel(file):
    file.seek(0)
    return pd.read_excel(file, engine="openpyxl")

def validate_company_format(columns):
    actual = [normalize_column_name(c) for c in columns]
    required = [normalize_column_name(c) for c in COMPANY_COLUMNS]
    return [c for c in required if c not in actual]

def get_size_group(cts):
    """Return the SIZE GROUP using the user's supplied Excel IFS ranges."""
    if pd.isna(cts):
        return ""
    try:
        cts = float(cts)
    except (ValueError, TypeError):
        return ""

    # Keep the ranges and labels exactly aligned with the supplied IFS formula.
    size_groups = [
        (0.30, 0.49, "0.30 - 0.49"),
        (0.50, 0.59, "0.50 - 0.59"),
        (0.60, 0.69, "0.60 - 0.69"),
        (0.70, 0.79, "0.70 - 0.79"),
        (0.80, 0.89, "0.80 - 0.89"),
        (0.90, 0.94, "0.90 - 0.94"),
        (0.95, 0.99, "0.95 - 0.99"),
        (1.00, 1.10, "1.00 - 1.10"),
        (1.11, 1.19, "1.11 - 1.19"),
        (1.20, 1.29, "1.20 - 1.29"),
        (1.30, 1.39, "1.30 - 1.39"),
        (1.40, 1.49, "1.40 - 1.49"),
        (1.50, 1.59, "1.50 - 1.59"),
        (1.60, 1.69, "1.60 - 1.69"),
        (1.70, 1.79, "1.70 - 1.79"),
        (1.80, 1.89, "1.80 - 1.89"),
        (1.90, 1.99, "1.90 - 1.99"),
        (2.00, 2.09, "2.00 - 2.09"),
        (2.10, 2.19, "2.10 - 2.19"),
        (2.20, 2.29, "2.20 - 2.29"),
        (2.30, 2.39, "2.30 - 2.39"),
        (2.40, 2.49, "2.40 - 2.49"),
        (2.50, 2.59, "2.50 - 2.59"),
        (2.60, 2.69, "2.60 - 2.69"),
        (2.70, 2.79, "2.70 - 2.79"),
        (2.80, 2.89, "2.80 - 2.89"),
        (2.90, 2.99, "2.90 - 2.99"),
        (3.00, 3.09, "3.00 - 3.09"),
        (3.10, 3.19, "3.10 - 3.19"),
        (3.20, 3.29, "3.20 - 3.29"),
        (3.30, 3.39, "3.30 - 3.39"),
        (3.40, 3.49, "3.40 - 3.49"),
        (3.50, 3.59, "3.50 - 3.59"),
        (3.60, 3.69, "3.60 - 3.69"),
        (3.70, 3.79, "3.70 - 3.79"),
        (3.80, 3.89, "3.80 - 3.89"),
        (3.90, 3.99, "3.90 - 3.99"),
        (4.00, 4.10, "4.00 - 4.10"),
        (4.50, 4.59, "4.50 - 4.59"),
        (5.00, 5.10, "5.00 - 5.10"),
        (5.50, 5.59, "5.50 - 5.59"),
        (6.00, 6.10, "6.00 - 6.10"),
        (6.50, 6.59, "6.50 - 6.59"),
        (7.00, 7.10, "7.00 - 7.10"),
        (8.00, 8.10, "8.00 - 8.10"),
        (9.00, 9.10, "9.00 - 9.10"),
        (10.00, 10.10, "10.00 - 10.10"),
        (11.00, 11.10, "11.00 - 11.10"),
        (12.00, 12.10, "12.00 - 12.10"),
        (13.00, 13.10, "13.00 - 13.10"),
        (14.00, 14.10, "14.00 - 14.10"),
        (15.00, 15.10, "15.00 - 15.10"),
        (16.00, 16.10, "16.00 - 16.10"),
        (17.00, 17.10, "17.00 - 17.10"),
        (18.00, 18.10, "18.00 - 18.10"),
        (19.00, 19.10, "19.00 - 19.10"),
        (20.00, 21.99, "20.00 - 21.99"),
    ]

    for lower, upper, label in size_groups:
        if lower <= cts <= upper:
            return label

    return "Out of Range"

def create_blank_output(number_of_rows):
    return pd.DataFrame("", index=range(number_of_rows), columns=COMPANY_COLUMNS)


# ============================================================
# CONVERT PARTY FILE  (unchanged logic)
# ============================================================

def convert_party_file(
    party_df, master_df, mapping, party_name,
    selection_done_by, india_price_filled_by,
    usa_price_filled_by, final_file_by, selected_date
):
    output = create_blank_output(len(party_df))

    output["SELECTION DONE BY"]   = selection_done_by
    output["INDIA PRICE FILLED BY"] = india_price_filled_by
    output["USA PRICE FILLED BY"]  = usa_price_filled_by
    output["FINAL THIS FILE BY"]   = final_file_by
    output["DATE"]                 = selected_date
    output["PARTY NAME"]           = party_name

    for party_field, party_column in mapping.items():
        if party_column is None:
            continue
        if party_column == "-- Select Party Column --":
            continue
        if party_column not in party_df.columns:
            continue
        company_column = FIELD_TO_COMPANY_COLUMN[party_field]
        output[company_column] = party_df[party_column].reset_index(drop=True)

    output["SIZE GROUP"] = output["CTS"].apply(get_size_group)

    for column in ["SHAPE", "SIZE GROUP", "COLOR", "CLARITY"]:
        output[column] = output[column].fillna("").astype(str).str.strip()

    output["KEY"] = (
        output["SHAPE"]
        + output["SIZE GROUP"]
        + output["COLOR"]
        + output["CLARITY"]
    )

    master = master_df.copy()
    master_key_column       = find_column(master, "KEY")
    master_grid_column      = find_column(master, "GRID")
    master_available_column = find_column(master, "AVAILABLE")

    if master_key_column is None:
        raise ValueError("Master File does not contain a KEY column.")
    if master_grid_column is None:
        raise ValueError("Master File does not contain a Grid column.")
    if master_available_column is None:
        raise ValueError("Master File does not contain an Available column.")

    master_lookup = master[[master_key_column, master_grid_column, master_available_column]].copy()
    master_lookup.columns = ["MASTER_KEY", "MASTER_GRID", "MASTER_AVAILABLE"]
    master_lookup["MASTER_KEY"] = master_lookup["MASTER_KEY"].fillna("").astype(str).str.strip()
    master_lookup["MASTER_GRID"] = pd.to_numeric(master_lookup["MASTER_GRID"], errors="coerce")
    master_lookup["MASTER_AVAILABLE"] = pd.to_numeric(master_lookup["MASTER_AVAILABLE"], errors="coerce")
    master_lookup = master_lookup.drop_duplicates(subset=["MASTER_KEY"], keep="first")

    output = output.merge(master_lookup, left_on="KEY", right_on="MASTER_KEY", how="left")
    # Preserve whether the KEY was actually found; missing master data must not
    # accidentally be treated as a valid 0-grid category.
    output["_MASTER_MATCHED"] = output["MASTER_KEY"].notna() & output["MASTER_KEY"].astype(str).str.strip().ne("")
    output["GRID"] = pd.to_numeric(output["MASTER_GRID"], errors="coerce").fillna(0)
    output["AVAILABLE"] = pd.to_numeric(output["MASTER_AVAILABLE"], errors="coerce").fillna(0)

    # BUSINESS SELECTION LOGIC:
    # - If AVAILABLE >= GRID, reject every stone for that category.
    # - If AVAILABLE < GRID, the number needed is GRID - AVAILABLE.
    # - Select up to that number, preferring the lowest PER CARAT price.
    # - When prices tie (or are missing), prefer lower CTS first.
    # - Any remaining stones in that category are rejected.
    output["SAME"] = ""
    output["REMARK"] = ""

    output["_PRICE_SORT"] = pd.to_numeric(
        output["PER CARAT"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )
    output["_CTS_SORT"] = pd.to_numeric(output["CTS"], errors="coerce")

    for key, row_indices in output.groupby("KEY", sort=False).groups.items():
        if not str(key).strip():
            continue

        category_rows = list(row_indices)
        first_idx = category_rows[0]

        # if not bool(output.at[first_idx, "_MASTER_MATCHED"]):
        #     continue

        # grid_value = float(output.at[first_idx, "GRID"])
        # available_value = float(output.at[first_idx, "AVAILABLE"])
        grid_value = float(output.at[first_idx, "GRID"])
        available_value = float(output.at[first_idx, "AVAILABLE"])

        # GRID = 0: Reject all stones in this category.
        if grid_value <= 0:
            output.loc[category_rows, "REMARK"] = "Rejection"
            continue

        # For positive GRID, require a matching Master Report KEY.
        if not bool(output.at[first_idx, "_MASTER_MATCHED"]):
            continue

        # Grid must be a positive count for a meaningful selection decision.
        # GRID = 0: Reject all stones in this category.
        if grid_value <= 0:
            output.loc[category_rows, "REMARK"] = "Rejection"
            continue

        if available_value >= grid_value:
            output.loc[category_rows, "REMARK"] = "Rejection"
            continue

        needed = max(0, int(round(grid_value - available_value)))
        sorted_indices = (
            output.loc[category_rows]
            .sort_values(
                by=["_PRICE_SORT", "_CTS_SORT"],
                ascending=[True, True],
                na_position="last",
                kind="stable"
            )
            .index
            .tolist()
        )

        selected_indices = set(sorted_indices[:needed])
        output.loc[category_rows, "REMARK"] = "Rejection"
        if selected_indices:
            output.loc[list(selected_indices), "REMARK"] = "Selection"

    output.drop(
        columns=[
            "MASTER_KEY", "MASTER_GRID", "MASTER_AVAILABLE",
            "_MASTER_MATCHED", "_PRICE_SORT", "_CTS_SORT"
        ],
        inplace=True,
        errors="ignore"
    )

    for column in ["TOTAL AMT", "VDB AMOUNT INDIA", "VDB AMOUNT USA",
                   "WITH TARIFF COST", "WITH TARIFF AMOUNT", "IND%", "USA%", "AFTER TARIFF DIFF$"]:
        output[column] = ""

    for column in COMPANY_COLUMNS:
        if column not in output.columns:
            output[column] = ""

    output = output[COMPANY_COLUMNS].reset_index(drop=True)
    return output


# ============================================================
# CREATE DOWNLOAD EXCEL  (unchanged logic)
# ============================================================

def create_download_excel(df):
    output = BytesIO()
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    for column in COMPANY_COLUMNS:
        if str(column).strip() not in df.columns:
            df[str(column).strip()] = ""

    df = df[[str(c).strip() for c in COMPANY_COLUMNS]]

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Final File")
        workbook  = writer.book
        worksheet = writer.sheets["Final File"]

        header_format = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True})

        header_size_grid_same = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#fcba03"})
        header_per_carat_total = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#5aa6c7"})
        header_india = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#b592d6"})
        header_usa = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#6aba95"})
        header_tariff = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#c27676"})
        header_difference = workbook.add_format({"bold": True, "border": 1, "align": "center", "valign": "vcenter", "text_wrap": True, "bg_color": "#f8fc03"})

        normal_format  = workbook.add_format({"border": 1, "valign": "vcenter"})
        remark_select_format = workbook.add_format({
            "border": 1, "valign": "vcenter", "bg_color": "#C6EFCE",
            "font_color": "#006100", "bold": True
        })
        remark_reject_format = workbook.add_format({
            "border": 1, "valign": "vcenter", "bg_color": "#FFC7CE",
            "font_color": "#9C0006", "bold": True
        })
        number_format  = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "0.00"})
        integer_format = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "0"})
        date_format    = workbook.add_format({"border": 1, "valign": "vcenter", "num_format": "dd-mm-yyyy"})

        size_grid_same_format  = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#fcba03"})
        per_carat_total_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#5aa6c7", "num_format": "0.00"})
        india_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#b592d6", "num_format": "0.00"})
        usa_format   = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#6aba95", "num_format": "0.00"})
        tariff_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#c27676", "num_format": "0.00"})

        same_formula_format       = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#fcba03", "num_format": "0"})
        total_formula_format      = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#5aa6c7", "num_format": "0.00"})
        vdb_india_formula_format  = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#b592d6", "num_format": "0.00"})
        vdb_usa_formula_format    = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#6aba95", "num_format": "0.00"})
        tariff_formula_format     = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#c27676", "num_format": "0.00"})
        difference_formula_format = workbook.add_format({"border": 1, "valign": "vcenter", "bg_color": "#f8fc03", "num_format": "0.00"})

        column_numbers = {str(c).strip(): i for i, c in enumerate(df.columns)}

        formula_columns = [
            "KEY", "SAME", "TOTAL AMT", "VDB AMOUNT INDIA", "VDB AMOUNT USA",
            "WITH TARIFF COST", "WITH TARIFF AMOUNT", "IND%", "USA%", "AFTER TARIFF DIFF$"
        ]

        for col_number, column in enumerate(df.columns):
            column_name = str(column).strip()
            if column_name in ["SIZE GROUP", "GRID", "AVAILABLE", "SAME"]:
                fmt = header_size_grid_same
            elif column_name in ["PER CARAT", "TOTAL AMT"]:
                fmt = header_per_carat_total
            elif column_name in ["VDB PRICE INDIA", "VDB AMOUNT INDIA"]:
                fmt = header_india
            elif column_name in ["VDB PRICE USA", "VDB AMOUNT USA"]:
                fmt = header_usa
            elif column_name in ["WITH TARIFF COST", "WITH TARIFF AMOUNT"]:
                fmt = header_tariff
            elif column_name in ["IND%", "USA%", "AFTER TARIFF DIFF$"]:
                fmt = header_difference
            else:
                fmt = header_format
            worksheet.write(0, col_number, column_name, fmt)

        for row_number in range(len(df)):
            for col_number, column in enumerate(df.columns):
                column_name = str(column).strip()
                if column_name in formula_columns:
                    continue
                value = df.iloc[row_number, col_number]
                if pd.isna(value):
                    value = ""
                if column_name == "DATE":
                    worksheet.write(row_number + 1, col_number, value, date_format)
                elif column_name == "REMARK" and str(value).strip().upper() == "SELECTION":
                    worksheet.write(row_number + 1, col_number, value, remark_select_format)
                elif column_name == "REMARK" and str(value).strip().upper() == "REJECTION":
                    worksheet.write(row_number + 1, col_number, value, remark_reject_format)
                elif column_name == "SIZE GROUP":
                    worksheet.write(row_number + 1, col_number, value, size_grid_same_format)
                elif column_name in ["GRID", "AVAILABLE"]:
                    worksheet.write(row_number + 1, col_number, value, size_grid_same_format)
                elif column_name == "PER CARAT":
                    worksheet.write(row_number + 1, col_number, value, per_carat_total_format)
                elif column_name == "VDB PRICE INDIA":
                    worksheet.write(row_number + 1, col_number, value, india_format)
                elif column_name == "VDB PRICE USA":
                    worksheet.write(row_number + 1, col_number, value, usa_format)
                elif column_name in ["WITH TARIFF COST"]:
                    worksheet.write(row_number + 1, col_number, value, tariff_format)
                else:
                    worksheet.write(row_number + 1, col_number, value, normal_format)

        for row_number in range(len(df)):
            excel_row = row_number + 2
            worksheet.write_formula(row_number + 1, column_numbers["KEY"],
                f'=CONCATENATE(J{excel_row},L{excel_row},M{excel_row},N{excel_row})', normal_format)
            worksheet.write_formula(row_number + 1, column_numbers["SAME"],
                f'=COUNTIF(O:O,O{excel_row})', same_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["TOTAL AMT"],
                f'=ROUND((T{excel_row}*K{excel_row}),2)', total_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["VDB AMOUNT INDIA"],
                f'=ROUND((V{excel_row}*K{excel_row}),2)', vdb_india_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["VDB AMOUNT USA"],
                f'=ROUND((X{excel_row}*K{excel_row}),2)', vdb_usa_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["WITH TARIFF COST"],
                f'=ROUND((T{excel_row}*1.08),2)', tariff_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["WITH TARIFF AMOUNT"],
                f'=ROUND((Z{excel_row}*K{excel_row}),2)', tariff_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["IND%"],
                f'=IFERROR(ROUND((100-(T{excel_row}*100)/V{excel_row}),2),"")', difference_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["USA%"],
                f'=IFERROR(ROUND((100-(Z{excel_row}*100)/X{excel_row}),2),"")', difference_formula_format)
            worksheet.write_formula(row_number + 1, column_numbers["AFTER TARIFF DIFF$"],
                f'=X{excel_row}-Z{excel_row}', difference_formula_format)

        for col_number, column in enumerate(df.columns):
            max_length = len(str(column))
            if len(df) > 0:
                for value in df[column].head(100):
                    if pd.notna(value):
                        max_length = max(max_length, len(str(value)))
            worksheet.set_column(col_number, col_number, min(max(max_length + 2, 12), 35))

        worksheet.freeze_panes(1, 0)
        if len(df.columns) > 0:
            worksheet.autofilter(0, 0, len(df), len(df.columns) - 1)
        workbook.set_calc_mode("auto")

    output.seek(0)
    return output


# ============================================================
# HERO BANNER
# ============================================================

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">◆ Diamond Format Converter</div>
    <div class="hero-subtitle">
        Transform any Party Excel file into Company Standard Format — with Master pricing, tariff calculations, and formula-ready output
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# STEP INDICATOR
# ============================================================

files_uploaded  = False
files_converted = bool(st.session_state.converted_files)

st.markdown("""
<div class="step-row">
    <div class="step-item active">
        <div class="step-num">1</div>
        Upload Files
    </div>
    <div class="step-item">
        <div class="step-num">2</div>
        Map &amp; Convert Party Files
    </div>
    <div class="step-item">
        <div class="step-num">3</div>
        Download Final File
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# STEP 1 — UPLOAD FILES
# ============================================================

st.markdown("""
<div class="section-header">
    <span class="section-badge">Step 1</span>
    <span class="section-title">Upload Files</span>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="col-group-label">Company &amp; Master Files</div>', unsafe_allow_html=True)
    company_file = st.file_uploader(
        "Company Standard Format",
        type=["xlsx", "xls"],
        key="company_file",
        help="Upload your company's standard Excel template"
    )
    master_file = st.file_uploader(
        "Master Report",
        type=["xlsx", "xls"],
        key="master_file",
        help="Upload the master pricing report with KEY, GRID & AVAILABLE columns"
    )

with col2:
    st.markdown('<div class="col-group-label">Party Files (multiple allowed)</div>', unsafe_allow_html=True)
    party_files = st.file_uploader(
        "Party Files",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        key="party_files",
        help="Upload one or more party Excel files to convert"
    )


# ── Upload Status ──────────────────────────────────────────

status_html = '<div style="display:flex; flex-wrap:wrap; gap:0.5rem; margin:1rem 0;">'
status_html += f'<span class="chip {"chip-success" if company_file else "chip-warn"}">{"✓" if company_file else "○"} Company Format</span>'
status_html += f'<span class="chip {"chip-success" if master_file else "chip-warn"}">{"✓" if master_file else "○"} Master Report</span>'
status_html += f'<span class="chip {"chip-success" if party_files else "chip-warn"}">{"✓" if party_files else "○"} Party Files ({len(party_files) if party_files else 0} uploaded)</span>'
status_html += '</div>'
st.markdown(status_html, unsafe_allow_html=True)

if company_file is None:
    st.info("⬆️  Upload your Company Standard Format file to continue.")
    st.stop()

if master_file is None:
    st.info("⬆️  Upload the Master Report file to continue.")
    st.stop()

if not party_files:
    st.info("⬆️  Upload at least one Party File to convert.")
    st.stop()


# ── Read & Validate ────────────────────────────────────────

try:
    company_df = read_excel(company_file)
except Exception as e:
    st.error(f"Cannot read Company Standard Format: {e}")
    st.stop()

missing_cols = validate_company_format(company_df.columns)
if missing_cols:
    st.error("Company Standard Format is missing required columns:")
    for c in missing_cols:
        st.write(f"  ❌ {c}")
    st.stop()

try:
    master_df = read_excel(master_file)
except Exception as e:
    st.error(f"Cannot read Master Report: {e}")
    st.stop()

master_key_column       = find_column(master_df, "KEY")
master_grid_column      = find_column(master_df, "GRID")
master_available_column = find_column(master_df, "AVAILABLE")

if not master_key_column:
    st.error("❌ Master Report is missing the KEY column.")
    st.stop()
if not master_grid_column:
    st.error("❌ Master Report is missing the GRID column.")
    st.stop()
if not master_available_column:
    st.error("❌ Master Report is missing the AVAILABLE column.")
    st.stop()


# ── File Preview Cards ─────────────────────────────────────

preview_col1, preview_col2 = st.columns(2)

with preview_col1:
    with st.expander("👁  Company Standard Format — Preview", expanded=False):
        st.markdown(f'<span class="chip chip-success">✓ {len(company_df.columns)} columns validated</span>', unsafe_allow_html=True)
        st.dataframe(company_df.head(10), use_container_width=True)

with preview_col2:
    with st.expander("📊 Master Report — Preview", expanded=False):
        st.markdown(
            f'<span class="chip chip-info">KEY: {master_key_column}</span>'
            f'<span class="chip chip-info">GRID: {master_grid_column}</span>'
            f'<span class="chip chip-info">AVAIL: {master_available_column}</span>'
            f'<span class="chip chip-success">{len(master_df):,} rows</span>',
            unsafe_allow_html=True
        )
        st.dataframe(master_df.head(15), use_container_width=True)


# ============================================================
# STEP 2 — PARTY FILE CONVERSION
# ============================================================

st.markdown("""
<div class="section-header">
    <span class="section-badge">Step 2</span>
    <span class="section-title">Map &amp; Convert Party Files</span>
</div>
""", unsafe_allow_html=True)

for file_index, party_file in enumerate(party_files):

    st.markdown(f"""
    <div class="party-card">
        <div class="party-card-title">◇ {party_file.name}</div>
        <div class="party-card-meta">Party File {file_index + 1} of {len(party_files)}</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        party_df = read_excel(party_file)
    except Exception as e:
        st.error(f"Cannot read {party_file.name}: {e}")
        continue

    party_columns = list(party_df.columns)

    # ── File Information ──────────────────────────────────
    st.markdown('<div class="col-group-label" style="margin-top:0.5rem;">File Information</div>', unsafe_allow_html=True)

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:
        selection_done_by = st.text_input(
            "Selection Done By",
            placeholder="Person name",
            key=f"selection_done_by_{file_index}"
        )
        india_price_filled_by = st.text_input(
            "India Price Filled By",
            placeholder="Person name",
            key=f"india_price_filled_by_{file_index}"
        )

    with info_col2:
        usa_price_filled_by = st.text_input(
            "USA Price Filled By",
            placeholder="Person name",
            key=f"usa_price_filled_by_{file_index}"
        )
        final_file_by = st.text_input(
            "Final File By",
            placeholder="Person name",
            key=f"final_file_by_{file_index}"
        )

    with info_col3:
        party_name = st.text_input(
            "Party Name",
            placeholder="Enter party name",
            key=f"party_name_{file_index}"
        )
        selected_date = st.date_input(
            "Date",
            value=date.today(),
            key=f"selected_date_{file_index}"
        )

    # ── Party Preview ─────────────────────────────────────
    with st.expander(f"👁  Preview — {party_file.name}", expanded=False):
        st.markdown(
            f'<span class="chip chip-info">{len(party_df):,} rows</span>'
            f'<span class="chip chip-info">{len(party_columns)} columns</span>',
            unsafe_allow_html=True
        )
        st.dataframe(party_df.head(15), use_container_width=True)

    # ── Column Mapping ────────────────────────────────────
    st.markdown('<div class="col-group-label" style="margin-top:1.25rem;">Column Mapping — Match party columns to company fields</div>', unsafe_allow_html=True)

    mapping = {}
    cols = st.columns(2)

    for field_index, field in enumerate(PARTY_FIELDS):
        container = cols[field_index % 2]
        with container:
            mapping[field] = st.selectbox(
                field,
                options=["-- Select Party Column --"] + party_columns,
                key=f"mapping_{file_index}_{field_index}"
            )

    missing_mapping = [
        f for f, c in mapping.items()
        if c == "-- Select Party Column --"
    ]

    if missing_mapping:
        st.markdown(
            f'<div style="margin-top:0.5rem;"><span class="chip chip-warn">⚠ {len(missing_mapping)} field(s) unmapped</span></div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div style="margin-top:0.5rem;"><span class="chip chip-success">✓ All columns mapped</span></div>',
            unsafe_allow_html=True
        )

    st.write("")
    convert_button = st.button(
        f"◆  Convert  {party_file.name}",
        key=f"convert_{file_index}",
        type="primary"
    )

    if convert_button:
        errors = []
        if not selection_done_by.strip():   errors.append("Selection Done By is required.")
        if not india_price_filled_by.strip(): errors.append("India Price Filled By is required.")
        if not usa_price_filled_by.strip():  errors.append("USA Price Filled By is required.")
        if not final_file_by.strip():        errors.append("Final File By is required.")
        if not party_name.strip():           errors.append("Party Name is required.")
        if missing_mapping:                  errors.append("All party columns must be mapped.")

        selected_vals = [c for c in mapping.values() if c != "-- Select Party Column --"]
        if len(selected_vals) != len(set(selected_vals)):
            errors.append("Each party column should be mapped only once.")

        if errors:
            st.error("Fix the following before converting:")
            for err in errors:
                st.write(f"  ❌ {err}")
            continue

        try:
            output_df = convert_party_file(
                party_df=party_df,
                master_df=master_df,
                mapping=mapping,
                party_name=party_name,
                selection_done_by=selection_done_by,
                india_price_filled_by=india_price_filled_by,
                usa_price_filled_by=usa_price_filled_by,
                final_file_by=final_file_by,
                selected_date=selected_date
            )
        except Exception as e:
            st.error(f"Conversion failed: {e}")
            continue

        st.session_state.converted_files[file_index] = {
            "file_name": party_file.name,
            "party_name": party_name,
            "data": output_df
        }

        st.success(f"✓ {party_file.name} converted — {len(output_df):,} rows ready.")

        with st.expander("📊 Converted Data Preview", expanded=True):
            st.dataframe(output_df.head(20), use_container_width=True)

    st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)


# ============================================================
# STEP 3 — FINAL FILE
# ============================================================

if st.session_state.converted_files:

    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Step 3</span>
        <span class="section-title">Final Company Standard File</span>
    </div>
    """, unsafe_allow_html=True)

    converted_data = [item["data"] for item in st.session_state.converted_files.values()]
    final_df = pd.concat(converted_data, ignore_index=True)

    for column in COMPANY_COLUMNS:
        if column not in final_df.columns:
            final_df[column] = ""
    final_df = final_df[COMPANY_COLUMNS]

    # ── Summary Metrics ───────────────────────────────────
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(converted_data)}</div>
            <div class="metric-label">Party Files Converted</div>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(final_df):,}</div>
            <div class="metric-label">Total Stones</div>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(COMPANY_COLUMNS)}</div>
            <div class="metric-label">Output Columns</div>
        </div>""", unsafe_allow_html=True)

    st.write("")

    # ── Final Preview ─────────────────────────────────────
    st.markdown('<div class="col-group-label">Final Data Preview</div>', unsafe_allow_html=True)
    st.dataframe(final_df, use_container_width=True, height=460)

    st.write("")

    # ── Download ──────────────────────────────────────────
    excel_data = create_download_excel(final_df)

    st.download_button(
        label="⬇  Download Company Standard File  (.xlsx)",
        data=excel_data,
        file_name="Company_Standard_Final.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True
    )

    st.markdown("""
    <div style="text-align:center; margin-top:1rem; font-size:0.78rem; color:#4A6070;">
        Excel formulas, color-coded columns, freeze panes, and auto-filter are included in the downloaded file.
    </div>
    """, unsafe_allow_html=True)