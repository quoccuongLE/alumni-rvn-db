import pandas as pd

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
    "full_name": ["full_name", "name", "rdv_user_name"],
    "university": ["university", "rdv_uni"],
    "department": ["department", "rdv_dept"],
    "email": ["email", "rdv_email"],
    "phone": ["phone", "rdv_phone"],
}

input_files = [
    {
        "file_name": "data/ds-hbvallet-2011-2018.xlsx",
        "sheet_names": ["2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018"],
        "attributes": [],
    }
]

df = pd.DataFrame(
    columns=[
        "full_name",
        "university",
        "department",
        "university_year",
        "email",
        "phone",
        "year_of_receipt",
    ],
    dtype=str
)


def _clean_marked_lines(dataframe: pd.DataFrame) -> pd.DataFrame:
    for invalid_value in _INVALID_VALUES:
        for column in list(dataframe.columns):
            dataframe = dataframe.drop(
                dataframe[dataframe[column] == invalid_value].index
            )

    return dataframe


def _trim_phone_number(dataframe: pd.DataFrame, column: str):
    dataframe[column] = dataframe[column].map(
        lambda x: int(x.replace(".", "").replace(" ", "")) if not isinstance(x, int) else  x
    )


for input_file in input_files:
    for sheet_name in input_file["sheet_names"]:
        df1 = pd.read_excel("data/ds-hbvallet-2011-2018.xlsx", sheet_name=sheet_name)
        df1 = _clean_marked_lines(dataframe=df1)
        df1 = _trim_phone_number(dataframe=df1, column="rdv_phone")
        print(df1.shape)
