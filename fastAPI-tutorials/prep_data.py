import pandas as pd
import locale
locale.setlocale(locale.LC_TIME, 'tr_TR')
pd.set_option('future.no_silent_downcasting', True)

def sales_by_cities(start_year=2013, end_year=2024):
    """
        This function returns the number of real estates sold according to cities (İl)

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

    df = pd.read_excel("./datasets/İllere göre satış sayısı.xls")
    df.rename(columns={df.columns[0]: "Yıl", df.columns[1]: "Ay", df.columns[2]: "Total"}, inplace=True)
    df.ffill(inplace=True)
    df['Yıl'] = df['Yıl'].astype(int)

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
