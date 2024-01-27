import pandas as pd
from typing import Union, Sequence
import logging
import fire


_INVALID_VALUES = [
    "rdv_user_name",
    "rdv_uni",
    "rdv_dept",
    "rdv_nien_khoa",
    "rdv_member_in",
    "rdv_email",
    "rdv_phone",
]

_SYNONYMS = {
    "full_name": ["full_name", "name", "rdv_user_name", "first_name"],
    "university": ["university", "rdv_uni", "ten_truong", "school"],
    "department": ["department", "rdv_dept", "dept", "khoa"],
    "major": ["major", "nganh_hoc"],
    "email": ["email", "rdv_email"],
    "phone": ["phone", "rdv_phone"],
    "university_year": ["university_year", "rdv_nien_khoa"],
    "alumni": ["alumni", "rdv_member_in"],
    "institution": ["institution", "khoi", "reg_group"],
}

input_files = [
    {
        "file_name": "data/ds-hbvallet-2011-2018.xlsx",
        "sheet_names": ["2011", "2012", "2013", "2014", "2016", "2017", "2018"],
        "attributes": [],
    }
]


def _clean_marked_lines(dataframe: pd.DataFrame) -> pd.DataFrame:
    for invalid_value in _INVALID_VALUES:
        for column in list(dataframe.columns):
            dataframe = dataframe.drop(
                dataframe[dataframe[column] == invalid_value].index
            )

    return dataframe


def _filter_phone_number(phone_number: Union[int, str, pd.NA]) -> int:
    if pd.isna(phone_number):
        return pd.NA
    if isinstance(phone_number, int):
        return phone_number
    if isinstance(phone_number, str):
        phone_number = phone_number.replace(".", "").replace(" ", "")
        if "(+84)" == phone_number[:5]:
            phone_number = "0" + phone_number.lstrip("(+84)")
        return str(phone_number)


def _trim_phone_number(dataframe: pd.DataFrame, column: str):
    dataframe[column] = dataframe[column].map(lambda x: _filter_phone_number(x))
    return dataframe


def _get_words_dict(key_list: Sequence[str]) -> dict[str, str]:
    synonyms_dict = dict()
    for key in key_list:
        for word, synonyms in _SYNONYMS.items():
            if key in synonyms:
                synonyms_dict.update({key: word})

    for key in key_list:
        if key not in synonyms_dict.keys():
            logging.warning(f"{key} unmatched!")

    return synonyms_dict


dfs = []
for input_file in input_files:
    for sheet_name in input_file["sheet_names"]:
        df = pd.DataFrame(
            columns=[
                "full_name",
                "university",
                "department",
                "major",
                "university_year",
                "institution",
                "alumni",
                "year_of_receipt",
                "email",
                "phone",
            ],
            dtype=str,
        )
        df1 = pd.read_excel(input_file["file_name"], sheet_name=sheet_name)
        df1 = _clean_marked_lines(dataframe=df1)
        headers = list(df1.columns)
        synonyms = _get_words_dict(key_list=headers)
        for column in headers:
            if column not in synonyms.keys():
                logging.warning(f"Column {column} not found")
                continue
            df[synonyms[column]] = df1[column]

        df["year_of_receipt"] = int(sheet_name)
        print(df.shape)
        dfs.append(df)

df_final = pd.concat(dfs, ignore_index=True)
print(df_final.shape)

# df1 = _trim_phone_number(dataframe=df1, column="phone")
