import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, 'tr_TR')
pd.set_option('future.no_silent_downcasting', True)

def sales_by_cities_df(start_year=2013, end_year=2024):
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

    city_codes = {
    "yıl": "", "ay": "", 'total': "",
    'adana': 1,
    'ADıYAMAN': 2,
    'AFYONKARAHiSAR': 3,
    'AĞRı': 4,
    'AMASYA': 5,
    'ANKARA': 6,
    'ANTALYA': 7,
    'ARTViN': 8,
    'AYDıN': 9,
    'BALıKESiR': 10,
    'BiLECiK': 11,
    'BiNGÖL': 12,
    'BiTLiS': 13,
    'BOLU': 14,
    'BURDUR': 15,
    'BURSA': 16,
    'ÇANAKKALE': 17,
    'ÇANKıRı': 18,
    'ÇORUM': 19,
    'DENiZLi': 20,
    'DiYARBAKıR': 21,
    'EDiRNE': 22,
    'ELAZıĞ': 23,
    'ERZiNCAN': 24,
    'ERZURUM': 25,
    'ESKiŞEHiR': 26,
    'GAZiANTEP': 27,
    'GiRESUN': 28,
    'GÜMÜŞHANE': 29,
    'HAKKARi': 30,
    'HATAY': 31,
    'iSPARTA': 32,
    'MERSiN': 33,
    'İSTANBUL': 34,
    'İZMiR': 35,
    'KARS': 36,
    'KASTAMONU': 37,
    'KAYSERi': 38,
    'kırklareli': 39,
    'KıRŞEHiR': 40,
    'KOCAELi': 41,
    'KONYA': 42,
    'KÜTAHYA': 43,
    'MALATYA': 44,
    'MANiSA': 45,
    'KAHRAMANMARAŞ': 46,
    'MARDiN': 47,
    'MUĞLA': 48,
    'MUŞ': 49,
    'NEVŞEHiR': 50,
    'NiĞDE': 51,
    'ORDU': 52,
    'RiZE': 53,
    'SAKARYA': 54,
    'SAMSUN': 55,
    'SiiRT': 56,
    'SiNOP': 57,
    'SiVAS': 58,
    'TEKiRDAĞ': 59,
    'TOKAT': 60,
    'TRABZON': 61,
    'TUNCELi': 62,
    'ŞANLıURFA': 63,
    'UŞAK': 64,
    'VAN': 65,
    'YOZGAT': 66,
    'ZONGULDAK': 67,
    'AKSARAY': 68,
    'BAYBURT': 69,
    'KARAMAN': 70,
    'KıRıKKALE': 71,
    'BATMAN': 72,
    'ŞıRNAK': 73,
    'BARTıN': 74,
    'ARDAHAN': 75,
    'iĞDıR': 76,
    'YALOVA': 77,
    'KARABÜK': 78,
    'KiLiS': 79,
    'OSMANiYE': 80,
    'DÜZCE': 81}
    df = pd.read_excel("./datasets/İllere göre konut satış sayısı.xls")
    df.rename(columns={df.columns[0]: "Yıl", df.columns[1]: "Ay", df.columns[2]: "Total"}, inplace=True)
    df.ffill(inplace=True)
    df['Yıl'] = df['Yıl'].astype(int)
    
    city_codes = {key.lower(): value for key, value in city_codes.items()}
    df.columns = df.columns.map(lambda x: f"{str(city_codes[x.lower()])} {x}".strip())

    breakpoint_index = 12
    df_totals_total = df.iloc[:breakpoint_index].copy()
    df_totals_total['Yıl'] = df_totals_total['Yıl'].astype(str)
    df_totals_total.at[breakpoint_index - 1, "Ay"] = df_totals_total.at[breakpoint_index - 1, "Ay"].split(" - ")[0]
    df_totals_total.at[0, "Ay"] = "Ocak-Aralık"
    df_totals_total.ffill(inplace=True)
    df_totals_total['Yıl/Ay'] = df_totals_total[['Yıl', 'Ay']].agg('/'.join, axis=1)

    df_totals_total = df_totals_total[["Yıl/Ay", "Total"]]
    df_totals_cities = df.drop(columns=["Total", "Ay"]).iloc[:breakpoint_index].copy()
    df_totals_cities.set_index("Yıl", inplace=True)

    df_granular = df.iloc[breakpoint_index:].copy()

    # Aggregating Yıl and Ay
    month_mapping = {
        'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4, 'Mayıs': 5, 'Haziran': 6,
        'Temmuz': 7, 'Ağustos': 8, 'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12
    }

    # Convert 'Yıl' and 'Ay' to datetime format
    df_granular['Tarih'] = df_granular.apply(lambda row: pd.Timestamp(int(row['Yıl']), month_mapping[row['Ay'].split(" - ")[0]], 28), axis=1)
    df_granular.drop(columns=['Yıl', 'Ay'], inplace=True)
    df_granular.set_index("Tarih", inplace=True)
    df_granular.sort_values(by='Tarih', inplace=True)

    df_granular = df_granular[(df_granular.index.year <= end_year) & (df_granular.index.year >= start_year)]

    df_granular_cities = df_granular.drop("Total", axis=1)

    return df_totals_total, df_totals_cities, df_granular, df_granular_cities

def sales_by_cities_foreigners_df(start_year=2013, end_year=2024):
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

    df_f = pd.read_excel("./datasets/İllere göre yabancılara konut satış sayısı.xls")
    df_f.rename(columns={'Unnamed: 1': 'Şehir'}, inplace=True)
    df_f_total = df_f[df_f['Şehir'] == "Toplam - Total"].drop(["Şehir", "Toplam"], axis=1)#.set_index("Yıl")
    df_f_total["Yıl"] = df_f_total["Yıl"].astype(int)
    df_f["Yıl"] = df_f["Yıl"].ffill().astype(int)
    df_f.drop("Toplam", axis=1, inplace=True)

    df_long = df_f_total.melt(id_vars=['Yıl'], var_name='Ay', value_name='Total')
    df_f_total_aggregated = df_long.groupby(['Yıl', 'Ay']).sum().reset_index()
    month_mapping = {
        'Ocak': 1, 'Şubat': 2, 'Mart': 3, 'Nisan': 4, 'Mayıs': 5, 'Haziran': 6,
        'Temmuz': 7, 'Ağustos': 8, 'Eylül': 9, 'Ekim': 10, 'Kasım': 11, 'Aralık': 12
    }
    df_f_total_aggregated['Tarih'] = df_f_total_aggregated.apply(lambda row: pd.Timestamp(int(row['Yıl']), month_mapping[row['Ay']], 1), axis=1)
    df_f_total_aggregated.drop(columns=['Yıl', 'Ay'], inplace=True)
    df_f_total_aggregated = df_f_total_aggregated.sort_values(by='Tarih')
    df_f_total_aggregated.set_index("Tarih", inplace=True)
    df_f_total_aggregated["Total"] = df_f_total_aggregated["Total"].astype(int)

    df_f_cities = df_f[df_f['Şehir'] != "Toplam - Total"]
    df_long = df_f_cities.melt(id_vars=['Yıl', 'Şehir'], var_name='Ay', value_name='Total')
    df_f_cities_aggregated = df_long.groupby(['Yıl', 'Şehir', 'Ay']).sum().reset_index()
    df_f_cities_aggregated['Tarih'] = df_f_cities_aggregated.apply(lambda row: pd.Timestamp(int(row['Yıl']), month_mapping[row['Ay']], 1), axis=1)
    df_f_cities_aggregated.drop(columns=['Yıl', 'Ay'], inplace=True)
    df_f_cities_aggregated = df_f_cities_aggregated.sort_values(by='Tarih')
    df_f_cities_aggregated.set_index("Tarih", inplace=True)
    df_f_cities_aggregated["Total"] = df_f_cities_aggregated["Total"].astype(int)

    df_f_total_aggregated = df_f_total_aggregated[(df_f_total_aggregated.index.year <= end_year) & (df_f_total_aggregated.index.year >= start_year)]
    df_f_total_aggregated = df_f_total_aggregated[df_f_total_aggregated['Total'] != 0]

    df_f_cities_aggregated = df_f_cities_aggregated[(df_f_cities_aggregated.index.year <= end_year) & (df_f_cities_aggregated.index.year >= start_year)]
    df_f_cities_aggregated = df_f_cities_aggregated[df_f_cities_aggregated['Total'] != 0]


    return df_f_total_aggregated, df_f_cities_aggregated

def population_df():
    df_p = pd.read_excel("./datasets/favori_raporlar.xlsx", header=[0, 1])

    cols = ['il kayit no', 'il adi', 'toplam', 'toplam-erkek', 'toplam-kadin',
        'il ve ilçe merkezleri-toplam', 'il ve ilçe merkezleri-erkek',
        'il ve ilçe merkezleri-kadin', 'belde ve köyler-toplam',
        'belde ve köyler-erkek', 'belde ve köyler-kadin']
    # df_p.columns = ['-'.join(col).strip().lower() if i >= 3 else col[0].strip().lower() for i, col in enumerate(df_p.columns.values)]
    df_p.columns = cols
    df_p.iloc[0,0] = 0
    df_p.iloc[0,1] = "ÜLKE"
    df_p.drop("il kayit no", axis=1,inplace=True)
    return df_p

