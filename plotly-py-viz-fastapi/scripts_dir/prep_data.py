import pandas as pd

pd.set_option("future.no_silent_downcasting", True)


city_codes = {
    "yıl": "Yıl",
    "ay": "Ay",
    "total": "Total",
    "toplam - total": "toplam - total",
    "adana": 1,
    "ADıYAMAN": 2,
    "AFYONKARAHiSAR": 3,
    "AĞRı": 4,
    "AMASYA": 5,
    "ANKARA": 6,
    "ANTALYA": 7,
    "ARTViN": 8,
    "AYDıN": 9,
    "BALıKESiR": 10,
    "BiLECiK": 11,
    "BiNGÖL": 12,
    "BiTLiS": 13,
    "BOLU": 14,
    "BURDUR": 15,
    "BURSA": 16,
    "ÇANAKKALE": 17,
    "ÇANKıRı": 18,
    "ÇORUM": 19,
    "DENiZLi": 20,
    "DiYARBAKıR": 21,
    "EDiRNE": 22,
    "ELAZıĞ": 23,
    "ERZiNCAN": 24,
    "ERZURUM": 25,
    "ESKiŞEHiR": 26,
    "GAZiANTEP": 27,
    "GiRESUN": 28,
    "GÜMÜŞHANE": 29,
    "HAKKARi": 30,
    "HATAY": 31,
    "iSPARTA": 32,
    "MERSiN": 33,
    "İSTANBUL": 34,
    "İZMiR": 35,
    "KARS": 36,
    "KASTAMONU": 37,
    "KAYSERi": 38,
    "kırklareli": 39,
    "KıRŞEHiR": 40,
    "KOCAELi": 41,
    "KONYA": 42,
    "KÜTAHYA": 43,
    "MALATYA": 44,
    "MANiSA": 45,
    "KAHRAMANMARAŞ": 46,
    "MARDiN": 47,
    "MUĞLA": 48,
    "MUŞ": 49,
    "NEVŞEHiR": 50,
    "NiĞDE": 51,
    "ORDU": 52,
    "RiZE": 53,
    "SAKARYA": 54,
    "SAMSUN": 55,
    "SiiRT": 56,
    "SiNOP": 57,
    "SiVAS": 58,
    "TEKiRDAĞ": 59,
    "TOKAT": 60,
    "TRABZON": 61,
    "TUNCELi": 62,
    "ŞANLıURFA": 63,
    "UŞAK": 64,
    "VAN": 65,
    "YOZGAT": 66,
    "ZONGULDAK": 67,
    "AKSARAY": 68,
    "BAYBURT": 69,
    "KARAMAN": 70,
    "KıRıKKALE": 71,
    "BATMAN": 72,
    "ŞıRNAK": 73,
    "BARTıN": 74,
    "ARDAHAN": 75,
    "iĞDıR": 76,
    "YALOVA": 77,
    "KARABÜK": 78,
    "KiLiS": 79,
    "OSMANiYE": 80,
    "DÜZCE": 81,
    "Diğer iller - Other Provinces": 99,
}
city_codes = {key.lower(): value for key, value in city_codes.items()}


def sales_cities_df(start_year=2019, end_year=2024):
    """
    This function returns the number of real estates sold according in each city (İl)

    params:
        start_year (int): the starting year for the total number of real estates sold in the country
        end_year (int): the ending year for the total number of real estates sold in the country

    returns:
        df_totals_total (pandas_df): Total number of real estates sold in the country
        df_totals_cities (pandas_df): Total number of real estates sold in each city
        df_granular (pandas_df): Number of real estates sold in the country in total a between [start_year, end_year] and in each city
            in each month (monthly granularity)
        df_granular_cities (pandas_df): df_granular without the "Total" column
    """
    excel_file_path = "../datasets/sales_data.xlsx"

    with pd.ExcelFile(excel_file_path) as xls:
        df_totals_total = pd.read_excel(xls, sheet_name="totals_total", index_col=0)
        df_totals_cities = pd.read_excel(xls, sheet_name="totals_cities", index_col=0)
        df_granular = pd.read_excel(xls, sheet_name="granular", index_col=0)
        df_granular_cities = pd.read_excel(
            xls, sheet_name="granular_cities", index_col=0
        )

    df_granular = df_granular[
        (df_granular.index.year <= end_year) & (df_granular.index.year >= start_year)
    ]

    df_granular_cities = df_granular.drop("Total", axis=1)

    return df_totals_total, df_totals_cities, df_granular, df_granular_cities


def sales_cities_foreigners_df(start_year=2019, end_year=2024):
    """
    This function returns the number of real estates sold to foreigners in each city (İl)

    params:
        start_year (int): the starting year for the total number of sales in the country
        end_year (int): the ending year for the total number of sales in the country

    returns:
        df_totals_total (pandas_df): Total number of real estates sold in the country
        df_totals_cities (pandas_df): Total number of real estates sold in each city
        df_granular (pandas_df): Number of real estates sold in the country in total a between [start_year, end_year] and in each city
            in each month (monthly granularity)
        df_granular_cities (pandas_df): df_granular without the "Total" column
    """
    excel_file_path = "../datasets/sales_foreigners_data.xlsx"
    with pd.ExcelFile(excel_file_path) as xls:
        df_f_total_aggregated = pd.read_excel(
            xls, sheet_name="df_f_total_aggregated", index_col=0
        )
        df_f_cities_aggregated = pd.read_excel(
            xls, sheet_name="df_f_cities_aggregated", index_col=0
        )

    df_f_total_aggregated = df_f_total_aggregated[
        (df_f_total_aggregated.index.year <= end_year)
        & (df_f_total_aggregated.index.year >= start_year)
    ]
    df_f_total_aggregated = df_f_total_aggregated[df_f_total_aggregated["Total"] != 0]

    df_f_cities_aggregated = df_f_cities_aggregated[
        (df_f_cities_aggregated.index.year <= end_year)
        & (df_f_cities_aggregated.index.year >= start_year)
    ]
    df_f_cities_aggregated = df_f_cities_aggregated[
        df_f_cities_aggregated["Total"] != 0
    ]

    return df_f_total_aggregated, df_f_cities_aggregated


def population_df():
    excel_file_path = "../datasets/population_data.xlsx"
    with pd.ExcelFile(excel_file_path) as xls:
        df_p = pd.read_excel(xls, sheet_name="df_p", index_col=0)

    return df_p


def population_marital_df():
    excel_file_path = "../datasets/population_marital_data.xlsx"
    with pd.ExcelFile(excel_file_path) as xls:
        df_never_married = pd.read_excel(
            xls, sheet_name="df_never_married", index_col=0
        )
        df_married = pd.read_excel(xls, sheet_name="df_married", index_col=0)
        df_divorced = pd.read_excel(xls, sheet_name="df_divorced", index_col=0)
        df_widowed = pd.read_excel(xls, sheet_name="df_widowed", index_col=0)
    return df_never_married, df_married, df_divorced, df_widowed


def population_origin_city_df():
    excel_file_path = "../datasets/population_based_on_origin_city.xlsx"
    with pd.ExcelFile(excel_file_path) as xls:
        df_origin_city = pd.read_excel(xls, sheet_name="df_origin_city", index_col=0)
    return df_origin_city


def population_trend_df():
    excel_file_path = "../datasets/population_trend.xlsx"
    with pd.ExcelFile(excel_file_path) as xls:
        df_trend = pd.read_excel(xls, sheet_name="df_trend", index_col=0)
    return df_trend


def election_df():
    excel_file_path = "../datasets/election.xlsx"
    with pd.ExcelFile(excel_file_path) as xls:
        df_election = pd.read_excel(xls, sheet_name="df_election", index_col=0)
    return df_election


def weather_df():
    file_path = "../datasets/weather_data.csv"
    weather_df = pd.read_csv(file_path)
    return weather_df
