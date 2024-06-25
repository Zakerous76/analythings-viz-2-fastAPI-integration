import pandas as pd

def sales_by_cities(start_year=2013, end_year=2024):
    """
        This function return the number of real estates sold according to cities (İl)

        params:
            start_year (int): the starting year for the Total number of real estates sold in the country
            end_year (int): the ending year for the Total number of real estates sold in the country

        returns:
            df_totals_total (pandas_df): Total number of real estates sold in the country
            df_totals_cities (pandas_df): Total number of real estates sold in each city
            df_totals_total_granular (pandas_df): Total number of real estates sold in the country from a between [start_year, end_year]
    """
    df = pd.read_excel("./datasets/İllere göre satış sayısı.xls")
    df.ffill(inplace=True)
    breakpoint_index = 12
    df_totals = df[:breakpoint_index]
    df_totals['Yıl'] = df_totals['Yıl'].astype(str)
    df_totals.at[breakpoint_index-1,"Ay"] = df_totals.at[breakpoint_index-1,"Ay"].split(" - ")[0]
    df_totals.at[0,"Ay"] = "Ocak-Aralık"
    df_totals = df_totals.ffill()
    df_totals['Yıl/Ay'] = df_totals[['Yıl', 'Ay']].agg('/'.join, axis=1)
    df_totals_total = df_totals[["Yıl/Ay", "Total"]]
    df_totals_cities = df_totals.drop(columns=["Total", "Yıl", "Ay"])
    df_totals_total_granular = df[breakpoint_index:]
    df_totals_total_granular = df_totals_total_granular[df_totals_total_granular.index.year <= start_year and df_totals_total_granular.index.year >= end_year]
    return df_totals_total, df_totals_cities, df_totals_total_granular