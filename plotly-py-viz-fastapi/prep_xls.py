import pandas as pd
import json

pd.set_option("future.no_silent_downcasting", True)

city_codes = {
    "yıl": "Yıl",
    "ay": "Ay",
    "total": "Total",
    "toplam - total": "toplam - total",
    "il": "il",
    "toplam": "toplam",
    "toplam-total": "toplam",
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


# Helper function to find the IDs from the reference data
def find_ids(reference_data, city_name, town_name=None, quarter_name=None):
    city_id, town_id, quarter_id = None, None, None
    for city in reference_data:
        if city["name"] == city_name:
            city_id = city["id"]

            for town in city["towns"]:
                if town["name"] == town_name:
                    town_id = town["id"]

                    for quarter in town["quarters"]:
                        if quarter["name"] == quarter_name:
                            quarter_id = quarter["id"]
                            return city_id, town_id, quarter_id
    return city_id, town_id, quarter_id


turkish_to_english = {
    "ç": "c",
    "ğ": "g",
    "ı": "i",
    "ö": "o",
    "ş": "s",
    "ü": "u",
    "i̇": "i",
    "Ç": "C",
    "Ğ": "G",
    "İ": "I",
    "Ö": "O",
    "Ş": "S",
    "Ü": "U",
    ".": "",
}


def replace_turkish_chars(text):
    text = text.lower()
    for turkish_char, english_char in turkish_to_english.items():
        text = text.replace(turkish_char, english_char)
    return text


def sales_cities():
    """
    This function cleans the "İllere göre konut satış sayısı.xls" data and creates a new excel file.

    params:


    Excel file saved at [excel_file_path] with the following sheets:
        df_totals_total (pandas_df): Total number of real estates sold in the country
        df_totals_cities (pandas_df): Total number of real estates sold in each city
        df_granular (pandas_df): Number of real estates sold in the country in total a between [start_year, end_year] and in each city
            in each month (monthly granularity)
        df_granular_cities (pandas_df): df_granular without the "Total" column
    """
    input_file_path = "./datasets/İllere göre konut satış sayısı.xls"
    output_file_path = "./datasets/sales_data.xlsx"

    df = pd.read_excel(input_file_path)
    df.rename(
        columns={df.columns[0]: "Yıl", df.columns[1]: "Ay", df.columns[2]: "Total"},
        inplace=True,
    )
    df.ffill(inplace=True)
    df["Yıl"] = df["Yıl"].astype(int)

    df.columns = df.columns.map(lambda x: city_codes[x.lower()])

    breakpoint_index = 12
    df_totals_total = df.iloc[:breakpoint_index].copy()
    df_totals_total["Yıl"] = df_totals_total["Yıl"].astype(str)
    df_totals_total.at[breakpoint_index - 1, "Ay"] = df_totals_total.at[
        breakpoint_index - 1, "Ay"
    ].split(" - ")[0]
    df_totals_total.at[0, "Ay"] = "Ocak-Aralık"
    df_totals_total.ffill(inplace=True)
    df_totals_total["Yıl/Ay"] = df_totals_total[["Yıl", "Ay"]].agg("/".join, axis=1)

    df_totals_total = df_totals_total[["Yıl/Ay", "Total"]]
    df_totals_cities = df.drop(columns=["Total", "Ay"]).iloc[:breakpoint_index].copy()
    df_totals_cities.set_index("Yıl", inplace=True)

    df_granular = df.iloc[breakpoint_index:].copy()

    # Aggregating Yıl and Ay
    month_mapping = {
        "Ocak": 1,
        "Şubat": 2,
        "Mart": 3,
        "Nisan": 4,
        "Mayıs": 5,
        "Haziran": 6,
        "Temmuz": 7,
        "Ağustos": 8,
        "Eylül": 9,
        "Ekim": 10,
        "Kasım": 11,
        "Aralık": 12,
    }

    # Convert 'Yıl' and 'Ay' to datetime format
    df_granular["Tarih"] = df_granular.apply(
        lambda row: pd.Timestamp(
            int(row["Yıl"]), month_mapping[row["Ay"].split(" - ")[0]], 28
        ),
        axis=1,
    )
    df_granular.drop(columns=["Yıl", "Ay"], inplace=True)
    df_granular.set_index("Tarih", inplace=True)
    df_granular.sort_values(by="Tarih", inplace=True)

    df_granular_cities = df_granular.drop("Total", axis=1)

    # Save DataFrames to Excel
    with pd.ExcelWriter(output_file_path) as writer:
        df_totals_total.to_excel(writer, sheet_name="totals_total")
        df_totals_cities.to_excel(writer, sheet_name="totals_cities")
        df_granular.to_excel(writer, sheet_name="granular")
        df_granular_cities.to_excel(writer, sheet_name="granular_cities")


def sales_cities_foreigners():
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
    input_file_path = "./datasets/İllere göre yabancılara konut satış sayısı.xls"
    output_file_path = "./datasets/sales_foreigners_data.xlsx"

    df_f = pd.read_excel(input_file_path)
    df_f.rename(columns={"Unnamed: 1": "Şehir"}, inplace=True)
    df_f_total = df_f[df_f["Şehir"] == "Toplam - Total"].drop(
        ["Şehir", "Toplam"], axis=1
    )  # .set_index("Yıl")
    df_f_total["Yıl"] = df_f_total["Yıl"].astype(int)
    df_f["Yıl"] = df_f["Yıl"].ffill().astype(int)
    df_f.drop("Toplam", axis=1, inplace=True)

    df_f["Şehir"] = df_f["Şehir"].map(lambda x: city_codes[x.lower()])

    df_long = df_f_total.melt(id_vars=["Yıl"], var_name="Ay", value_name="Total")
    df_f_total_aggregated = df_long.groupby(["Yıl", "Ay"]).sum().reset_index()
    month_mapping = {
        "Ocak": 1,
        "Şubat": 2,
        "Mart": 3,
        "Nisan": 4,
        "Mayıs": 5,
        "Haziran": 6,
        "Temmuz": 7,
        "Ağustos": 8,
        "Eylül": 9,
        "Ekim": 10,
        "Kasım": 11,
        "Aralık": 12,
    }
    df_f_total_aggregated["Tarih"] = df_f_total_aggregated.apply(
        lambda row: pd.Timestamp(int(row["Yıl"]), month_mapping[row["Ay"]], 1), axis=1
    )
    df_f_total_aggregated.drop(columns=["Yıl", "Ay"], inplace=True)
    df_f_total_aggregated = df_f_total_aggregated.sort_values(by="Tarih")
    df_f_total_aggregated.set_index("Tarih", inplace=True)
    df_f_total_aggregated["Total"] = df_f_total_aggregated["Total"].astype(int)

    df_f_cities = df_f[df_f["Şehir"] != "toplam - total"]
    df_long = df_f_cities.melt(
        id_vars=["Yıl", "Şehir"], var_name="Ay", value_name="Total"
    )
    df_f_cities_aggregated = df_long.groupby(["Yıl", "Şehir", "Ay"]).sum().reset_index()
    df_f_cities_aggregated["Tarih"] = df_f_cities_aggregated.apply(
        lambda row: pd.Timestamp(int(row["Yıl"]), month_mapping[row["Ay"]], 1), axis=1
    )
    df_f_cities_aggregated.drop(columns=["Yıl", "Ay"], inplace=True)
    df_f_cities_aggregated = df_f_cities_aggregated.sort_values(by="Tarih")
    df_f_cities_aggregated.set_index("Tarih", inplace=True)
    df_f_cities_aggregated["Total"] = df_f_cities_aggregated["Total"].astype(int)

    with pd.ExcelWriter(output_file_path) as writer:
        df_f_total_aggregated.to_excel(writer, sheet_name="df_f_total_aggregated")
        df_f_cities_aggregated.to_excel(writer, sheet_name="df_f_cities_aggregated")


def population():
    input_file_path = "./datasets/nüfus.xlsx"
    output_file_path = "./datasets/population_data.xlsx"

    df_p = pd.read_excel(input_file_path, sheet_name="MAHALLE NÜFUSU", index_col=0)
    cols = [
        "il kayit no",
        "ilçe kayit no",
        "belde/köy kayit no",
        "mahalle kayit no",
        "il adi",
        "ilçe adi",
        "belediye adi",
        "mahalle adi",
        "mahallenin bağli olduğu belediyenin niteliği",
        "toplam",
        "erkek",
        "kadin",
    ]
    df_p.columns = cols

    df_p = df_p[
        [
            "il kayit no",
            "ilçe kayit no",
            "mahalle kayit no",
            "il adi",
            "ilçe adi",
            "mahalle adi",
            "erkek",
            "kadin",
        ]
    ]
    df_p.erkek = df_p.erkek.replace("C", "0").astype(int)
    df_p.kadin = df_p.kadin.replace("C", "0")
    df_p.kadin = df_p.kadin.replace("-", "0").astype(int)
    for col in ["il adi", "ilçe adi", "mahalle adi"]:
        df_p[col + " cleaned"] = df_p[col].apply(
            lambda x: replace_turkish_chars(str(x))
        )

    df_p = (
        df_p.groupby(
            [
                "il kayit no",
                "ilçe kayit no",
                "mahalle kayit no",
                "il adi",
                "ilçe adi",
                "mahalle adi",
                "il adi cleaned",
                "ilçe adi cleaned",
                "mahalle adi cleaned",
            ]
        )[["erkek", "kadin"]]
        .sum()
        .reset_index()
    )

    with open("./cities.json", "r", encoding="utf-8") as file:
        json_data = file.read()
    reference_data = json.loads(json_data)

    for city in reference_data:
        city["name"] = replace_turkish_chars(city["name"])
        for town in city["towns"]:
            town["name"] = replace_turkish_chars(town["name"])

            for quarter in town["quarters"]:
                quarter["name"] = replace_turkish_chars(quarter["name"])
                if (
                    ("mh" in quarter["name"])
                    or ("mah" in quarter["name"])
                    or ("mahalle" in quarter["name"])
                    or ("bld" in quarter["name"])
                ):
                    quarter["name"] = " ".join(quarter["name"].split()[:-1])

    # Update the DataFrame with IDs
    for idx, row in df_p.iterrows():
        city_name = row["il adi cleaned"]
        town_name = row["ilçe adi cleaned"]
        quarter_name = row["mahalle adi cleaned"]
        city_id, town_id, quarter_id = find_ids(
            reference_data, city_name, town_name, quarter_name
        )
        df_p.at[idx, "il kayit no"] = -1 if city_id is None else city_id
        df_p.at[idx, "ilçe kayit no"] = -2 if town_id is None else town_id
        df_p.at[idx, "mahalle kayit no"] = -3 if quarter_id is None else quarter_id

    with pd.ExcelWriter(output_file_path) as writer:
        df_p.to_excel(writer, sheet_name="df_p")


def population_marital():
    input_file_path = "./datasets/il medeni durum ve cinsiyete gore nufus.xls"  # Replace with the correct file path
    output_file_path = "./datasets/population_marital_data.xlsx"

    df_origin_city = pd.read_excel(input_file_path, header=[0, 1])

    df_origin_city.set_index(("İl-Provinces", "Unnamed: 0_level_1"), inplace=True)
    df_origin_city.index.rename("İl", inplace=True)
    df_origin_city.index = df_origin_city.index.map(lambda x: city_codes[x.lower()])
    new_index = df_origin_city.index.to_list()  # Convert the index to a list
    new_index[0] = 0  # Change the first index value
    df_origin_city.index = new_index

    df_never_married = df_origin_city["Hiç evlenmedi-Never married"].drop(
        "Kadın\nFemale.1", axis=1
    )
    df_never_married.rename(
        columns={
            "Toplam\nTotal": "toplam",
            "Erkek\nMale": "erkek",
            "Kadın\nFemale": "kadın",
        },
        inplace=True,
    )

    df_married = df_origin_city["Evli-Married"].drop("Kadın\nFemale.1", axis=1)
    df_married.rename(
        columns={
            "Toplam\nTotal": "toplam",
            "Erkek\nMale": "erkek",
            "Kadın\nFemale": "kadın",
        },
        inplace=True,
    )

    df_divorced = df_origin_city["Boşandı-Divorced"].drop("Kadın\nFemale.1", axis=1)
    df_divorced.rename(
        columns={
            "Toplam\nTotal": "toplam",
            "Erkek\nMale": "erkek",
            "Kadın\nFemale": "kadın",
        },
        inplace=True,
    )

    df_widowed = df_origin_city["Eşi öldü-Widowed"]
    df_widowed.rename(
        columns={
            "Toplam\nTotal": "toplam",
            "Erkek\nMale": "erkek",
            "Kadın\nFemale": "kadın",
        },
        inplace=True,
    )

    with pd.ExcelWriter(output_file_path) as writer:
        df_never_married.to_excel(writer, sheet_name="df_never_married")
        df_married.to_excel(writer, sheet_name="df_married")
        df_divorced.to_excel(writer, sheet_name="df_divorced")
        df_widowed.to_excel(writer, sheet_name="df_widowed")


def population_origin_city():
    input_file_path = (
        "./datasets/ikamet edilen ile gore nufus kutugune kayitli olunan il.xls"
    )
    output_file_path = "./datasets/population_based_on_origin_city.xlsx"
    df_origin_city = pd.read_excel(input_file_path)
    df_origin_city.rename(
        columns={"Unnamed: 0": "il", "Toplam\nTotal": "toplam"}, inplace=True
    )
    df_origin_city.columns = df_origin_city.columns.map(lambda x: city_codes[x.lower()])
    df_origin_city.il = df_origin_city.il.map(lambda x: city_codes[x.lower()])
    df_origin_city.set_index("il", inplace=True)
    with pd.ExcelWriter(output_file_path) as writer:
        df_origin_city.to_excel(writer, sheet_name="df_origin_city")


from prep_data import population_df
import openpyxl


def population_trend():
    input_file_path = "./datasets/nüfus artisi.XLSX"
    output_file_path = "./datasets/population_trend.xlsx"

    df_trend = pd.read_excel(input_file_path)
    df_trend.rename(
        columns={
            "İl ve ilçe\nProvince and district": "il ve ilçe",
            "Nüfus(1)\nPopulation(1)": "toplam",
            df_trend.columns[2]: "artis",
        },
        inplace=True,
    )
    df_trend.drop("il ve ilçe", axis=1, inplace=True)

    wb = openpyxl.load_workbook(input_file_path)
    ws = wb.active
    province = None
    # First row to keep the first element
    data = [["toplam", "toplam"]]
    # Iterate over each row in the worksheet
    for row in ws.iter_rows(values_only=False):
        cell = row[0]
        # Check if the font is bold to identify a province
        if cell.font.bold:
            province = cell.value
        if province:
            data.append([province, cell.value])
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=["il", "ilçe"])
    df_trend = pd.concat([df, df_trend], axis=1)
    for index, row in df_trend.iterrows():
        df_trend.iat[index, 0] = replace_turkish_chars(row["il"])
        df_trend.iat[index, 1] = replace_turkish_chars(row["ilçe"])

    df_p = population_df()
    df_lookup = (
        df_p.groupby(
            ["il kayit no", "ilçe kayit no", "il adi cleaned", "ilçe adi cleaned"]
        )[["erkek", "kadin"]]
        .sum()
        .reset_index()
        .drop(["erkek", "kadin"], axis=1)
    )
    # Make sure the column names match for merging
    df_lookup = df_lookup.rename(
        columns={"il adi cleaned": "il", "ilçe adi cleaned": "ilçe"}
    )
    # Merge the DataFrames
    merged_df = pd.merge(
        df_trend, df_lookup, how="left", left_on=["il", "ilçe"], right_on=["il", "ilçe"]
    )
    # Fill missing IDs with -2
    merged_df["il kayit no"] = merged_df["il kayit no"].fillna(-1).astype(int)
    merged_df["ilçe kayit no"] = merged_df["ilçe kayit no"].fillna(-2).astype(int)
    # Select and reorder the columns as needed
    result_df = merged_df[
        ["il kayit no", "ilçe kayit no", "il", "ilçe", "toplam", "artis"]
    ]
    first_row = result_df.iloc[[0]]
    # Exclude the first row
    remaining_df = result_df.iloc[1:]
    # Drop rows where 'il' and 'ilçe' are the same in the remaining DataFrame
    filtered_df = remaining_df[remaining_df["il"] != remaining_df["ilçe"]]
    # Concatenate the first row back to the filtered DataFrame
    df_trend = pd.concat([first_row, filtered_df], ignore_index=True)
    df_trend.iat[0, 0] = 0
    df_trend.iat[0, 1] = 0
    with pd.ExcelWriter(output_file_path) as writer:
        df_trend.to_excel(writer, sheet_name="df_trend")


import os


def secim():
    # Path to the folder containing your Excel files
    folder_path = "./datasets/secim/"

    output_file_path = "./datasets/secim.xlsx"
    # List to store all dataframes
    dfs_list = []

    # Iterate over each file in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".xls"):
            file_path = os.path.join(folder_path, filename)

            # Read the Excel file
            dfs = pd.read_html(file_path)

            # Assume the first table in the HTML is the one you want
            df = dfs[0]

            # Clean and transform the dataframe as you did before
            df.drop(["Belde Adı"], axis=1, inplace=True)
            df.dropna(inplace=True)
            df = df[df["İlçe Adı"] != "Oy Oranı"].reset_index()
            df.drop("index", axis=1, inplace=True)

            columns_to_transform = df.columns[2:5].to_list()
            df[columns_to_transform] = df[columns_to_transform].apply(
                lambda x: (x * 1000).astype(int)
            )

            object_columns_to_transform = df.columns[5:].to_list()
            df[object_columns_to_transform] = df[object_columns_to_transform].apply(
                lambda x: x.str.replace(".", "").astype(int)
            )

            numeric_columns = df.select_dtypes(include="number").columns.tolist()
            # Group by "İlçe Id", keeping the first instance of "İlçe Adı" and summing up the numeric columns
            df = df.groupby("İlçe Id", as_index=False).agg(
                {**{"İlçe Adı": "first"}, **{col: "sum" for col in numeric_columns}}
            )
            df.drop("İlçe Id", axis=1, inplace=True)
            # Add a new column "İl Adı" with the province name
            province_name = filename.split(".")[
                0
            ]  # Assuming filename is like "BAYBURT.xls"
            if province_name == "AFYON":
                province_name = "AFYONKARAHİSAR"
            df.insert(0, "İl Adı", province_name)

            # Fill NaN values with 0

            # Append the modified dataframe to the list
            dfs_list.append(df)

    # Concatenate all dataframes into a single dataframe
    combined_df = pd.concat(dfs_list, ignore_index=True)
    combined_df.fillna(0, inplace=True)
    combined_df["İlçe Adı"] = combined_df["İlçe Adı"].apply(
        lambda x: "".join(x.split()[-1])
    )
    combined_df.insert(1, "il adi cleaned", combined_df["İl Adı"])
    combined_df.insert(3, "ilçe adi cleaned", combined_df["İlçe Adı"])

    for index, row in combined_df.iterrows():
        combined_df.iat[index, 1] = replace_turkish_chars(row["il adi cleaned"])
        combined_df.iat[index, 3] = replace_turkish_chars(row["ilçe adi cleaned"])

    df_p = population_df()
    df_lookup = (
        df_p.groupby(
            ["il kayit no", "ilçe kayit no", "il adi cleaned", "ilçe adi cleaned"]
        )[["erkek", "kadin"]]
        .sum()
        .reset_index()
        .drop(["erkek", "kadin"], axis=1)
    )
    # Merge the DataFrames
    merged_df = pd.merge(
        combined_df,
        df_lookup,
        how="left",
        left_on=["il adi cleaned", "ilçe adi cleaned"],
        right_on=["il adi cleaned", "ilçe adi cleaned"],
    )
    with pd.ExcelWriter(output_file_path) as writer:
        merged_df.to_excel(writer, sheet_name="df_secim")


if __name__ == "__main__":
    sales_cities()
    sales_cities_foreigners()
    population()
    population_marital()
    population_origin_city()
    population_trend()
