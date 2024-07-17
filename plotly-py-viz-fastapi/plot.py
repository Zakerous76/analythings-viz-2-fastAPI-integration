import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import scipy.stats as stats
import numpy as np

font_family = "Verdana"
label_font_size = 25
line_width = 5
marker_size = 12
color_sequence = px.colors.qualitative.Set3


teal_like = "#233d4d"
orange_like = "orange"

design = dict(
    title_font=dict(size=30, family=font_family, weight="bold", color="black"),
    xaxis=dict(
        tickangle=-45,
        tickfont=dict(family=font_family, size=12),
        showgrid=True,
        gridcolor="lightgray",
    ),
    yaxis=dict(
        tickfont=dict(family=font_family, size=12),
        tickformat=",",
        showgrid=True,
        gridcolor="lightgray",
    ),
    xaxis_title_font=dict(size=20, family=font_family, color="black", weight="bold"),
    yaxis_title_font=dict(size=20, family=font_family, color="black", weight="bold"),
    plot_bgcolor="#f3f4f6",
    margin=dict(l=110, r=20, t=100, b=110),
    title_x=0.5,
    title_xanchor="center",
    # paper_bgcolor="rgb(0,0,0,0)",
)


def design_animate(x_min, x_max, y_min, y_max):
    return dict(
        title_font=dict(size=30, family=font_family, weight="bold", color="black"),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(family=font_family, size=12),
            showgrid=True,
            range=[x_min, x_max],
            gridcolor="lightgray",
        ),
        yaxis=dict(
            tickfont=dict(family=font_family, size=12),
            tickformat=",",
            showgrid=True,
            range=[y_min, y_max],
            gridcolor="lightgray",
        ),
        xaxis_title_font=dict(
            size=20, family=font_family, color="black", weight="bold"
        ),
        yaxis_title_font=dict(
            size=20, family=font_family, color="black", weight="bold"
        ),
        plot_bgcolor="#f3f4f6",
        margin=dict(l=110, r=20, t=100, b=110),
        hovermode="x",
        legend=dict(
            font=dict(family=font_family, size=12),
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
        ),
        title_x=0.5,
        title_xanchor="center",
    )


city_code_map = {
    0: "ÜLKE",
    1: "ADANA",
    2: "ADIYAMAN",
    3: "AFYONKARAHİSAR",
    4: "AĞRI",
    5: "AMASYA",
    6: "ANKARA",
    7: "ANTALYA",
    8: "ARTVİN",
    9: "AYDIN",
    10: "BALIKESİR",
    11: "BİLECİK",
    12: "BİNGÖL",
    13: "BİTLİS",
    14: "BOLU",
    15: "BURDUR",
    16: "BURSA",
    17: "ÇANAKKALE",
    18: "ÇANKIRI",
    19: "ÇORUM",
    20: "DENİZLİ",
    21: "DİYARBAKIR",
    22: "EDİRNE",
    23: "ELAZIĞ",
    24: "ERZİNCAN",
    25: "ERZURUM",
    26: "ESKİŞEHİR",
    27: "GAZİANTEP",
    28: "GİRESUN",
    29: "GÜMÜŞHANE",
    30: "HAKKARİ",
    31: "HATAY",
    32: "ISPARTA",
    33: "MERSİN",
    34: "İSTANBUL",
    35: "İZMİR",
    36: "KARS",
    37: "KASTAMONU",
    38: "KAYSERİ",
    39: "KIRKLARELİ",
    40: "KIRŞEHİR",
    41: "KOCAELİ",
    42: "KONYA",
    43: "KÜTAHYA",
    44: "MALATYA",
    45: "MANİSA",
    46: "KAHRAMANMARAŞ",
    47: "MARDİN",
    48: "MUĞLA",
    49: "MUŞ",
    50: "NEVŞEHİR",
    51: "NİĞDE",
    52: "ORDU",
    53: "RİZE",
    54: "SAKARYA",
    55: "SAMSUN",
    56: "SİİRT",
    57: "SİNOP",
    58: "SİVAS",
    59: "TEKİRDAĞ",
    60: "TOKAT",
    61: "TRABZON",
    62: "TUNCELİ",
    63: "ŞANLIURFA",
    64: "UŞAK",
    65: "VAN",
    66: "YOZGAT",
    67: "ZONGULDAK",
    68: "AKSARAY",
    69: "BAYBURT",
    70: "KARAMAN",
    71: "KIRIKKALE",
    72: "BATMAN",
    73: "ŞIRNAK",
    74: "BARTIN",
    75: "ARDAHAN",
    76: "IĞDIR",
    77: "YALOVA",
    78: "KARABÜK",
    79: "KİLİS",
    80: "OSMANİYE",
    81: "DÜZCE",
    99: "Diğer iller - Other Provinces",
}
city_code_f = [48, 33, 35, 16, 99, 9, 7, 54, 6, 34, 77, 61, 55, 41]


def total_sales_animate(df_granular, width=None, height=800):

    # df_granular is your DataFrame and has the necessary data
    # Calculate the min and max values for the x and y axis
    x_min = df_granular.index.min() - pd.Timedelta(days=2)
    x_max = df_granular.index.max() + pd.Timedelta(days=20)
    y_min = 0
    y_max = df_granular["Total"].max() * 1.2

    fig = go.Figure(layout=dict(height=height, width=width))

    # Initial empty plot
    fig.add_trace(
        go.Scatter(
            x=df_granular.index,
            y=[None] * len(df_granular),
            mode="lines+markers",
            line=dict(color=orange_like, width=line_width),
            marker=dict(color=teal_like, size=marker_size),
            name="Ülkede Toplam Konut Satış",
        )
    )

    # Define frames for animation
    frames = [
        go.Frame(
            data=[
                go.Scatter(
                    x=df_granular.index[: k + 1], y=df_granular["Total"][: k + 1]
                )
            ],
            name=str(k),
        )
        for k in range(len(df_granular))
    ]

    fig.frames = frames

    # Add play and pause buttons
    updatemenus = [
        {
            "buttons": [
                {
                    "args": [
                        None,
                        {
                            "frame": {"duration": 50, "redraw": True},
                            "fromcurrent": True,
                            "mode": "immediate",
                        },
                    ],
                    "label": "Play",
                    "method": "animate",
                },
                {
                    "args": [
                        [None],
                        {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"},
                    ],
                    "label": "Pause",
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top",
        }
    ]

    # Update layout with buttons and animation settings
    fig.update_layout(
        title=f"Ülkede Toplam Konut Satış ({df_granular.index.min().year}-{df_granular.index.max().year})",
        xaxis_title="Tarih",
        yaxis_title="Toplam",
        updatemenus=updatemenus,
        sliders=[
            {
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Tarih:",
                    "visible": True,
                    "xanchor": "right",
                },
                "transition": {"duration": 50, "easing": "linear"},
                "pad": {"b": 10, "t": 100},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [
                            [str(k)],
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "mode": "immediate",
                            },
                        ],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k in range(len(df_granular))
                ],
            }
        ],
    )
    fig.update_layout(
        design_animate(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
    )

    return fig


def total_sales_plot(df_granular, width=None, height=800):

    # Calculate the min and max values for the x and y axis
    x_min = df_granular.index.min() - pd.Timedelta(days=2)
    x_max = df_granular.index.max() + pd.Timedelta(days=20)

    y_min = 0
    y_max = df_granular["Total"].max() * 1.2

    # Create figure
    fig = go.Figure(layout=dict(height=height, width=width))

    # Initial empty plot
    fig.add_trace(
        go.Scatter(
            x=df_granular.index,
            y=df_granular["Total"],
            mode="lines+markers",
            line=dict(color=orange_like, width=line_width),
            marker=dict(color=teal_like, size=marker_size),
            # line=dict(color=teal_like, width=line_width), marker=dict(color="orange", size=10),
            name="Ülkede Toplam Konut Satış",
        )
    )

    # Update layout with buttons and animation settings
    fig.update_layout(
        title=f"Ülkede Toplam Konut Satış ({df_granular.index.min().year}-{df_granular.index.max().year})",
        xaxis_title="Tarih",
        yaxis_title="Toplam",
    )
    fig.update_layout(
        design_animate(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
    )

    return fig


def total_sales_yearly_plot(df_totals_cities, city_code=0, width=None, height=800):
    if city_code == 0:
        fig = go.Figure(
            data=[
                go.Scatter(
                    name=city_code_map[city].capitalize(),
                    x=df_totals_cities.index,
                    y=df_totals_cities[city],
                    line=dict(width=line_width),
                )
                for city in df_totals_cities.columns
            ],
            layout=dict(height=height, width=width),
        )
        fig.update_layout(
            title="İllere Göre Konut Satışı (Yıl Bazında)",
            xaxis_title="Yıl",
            yaxis_title="Toplam Konut Satışı",
            barmode="stack",
        )
        fig.update_xaxes(tickmode="linear")
    else:
        fig = go.Figure(
            data=[
                go.Scatter(
                    name=city_code_map[city_code].capitalize(),
                    x=df_totals_cities.index,
                    y=df_totals_cities[city_code],
                    mode="lines+markers",
                    line=dict(color=orange_like, width=line_width),
                    marker=dict(color=teal_like, size=10),
                )
            ],
            layout=dict(height=height, width=width),
        )
        fig.update_layout(
            title=f"Konut Satışı (Yıl Bazında): {city_code_map[city_code].capitalize()}",
            xaxis_title="Yıl",
            yaxis_title="Toplam Konut Satışı",
            barmode="stack",
        )
        fig.update_xaxes(tickmode="linear")

    fig.update_layout(design)

    return fig


def total_sales_monthly_plot(df_granular_cities, city_code=0, width=None, height=800):
    if city_code == 0:
        fig = go.Figure(
            data=[
                go.Scatter(
                    name=city_code_map[city].capitalize(),
                    x=df_granular_cities.index,
                    y=df_granular_cities[city],
                    line=dict(width=line_width),
                )
                for city in df_granular_cities.columns
            ],
            layout=dict(height=height, width=width),
        )
        fig.update_layout(
            title="İllere Göre Konut Satışı (Ay bazında)",
            xaxis_title="Yıl",
            yaxis_title="Toplam Konut Satışı",
            barmode="stack",
        )
    else:
        fig = go.Figure(
            data=[
                go.Scatter(
                    name=city_code_map[city_code].capitalize(),
                    x=df_granular_cities.index,
                    y=df_granular_cities[city_code],
                    line=dict(width=line_width),
                )
            ],
            layout=dict(height=height, width=width),
        )
        fig.update_layout(
            title=f"Konut Satışı (Ay Bazında): {city_code_map[city_code].capitalize()}",
            yaxis_title="Toplam Konut Satışı",
            barmode="stack",
        )

    fig.update_layout(design)

    return fig


def total_sales_foreigners_animate(df_f_total_aggregated, width=None, height=800):

    # df_F_total_aggregated is your DataFrame and has the necessary data
    # Calculate the min and max values for the x and y axis
    x_min = df_f_total_aggregated.index.min() - pd.Timedelta(days=2)
    x_max = df_f_total_aggregated.index.max() + pd.Timedelta(days=20)
    y_min = 0
    y_max = df_f_total_aggregated["Total"].max() * 1.2

    # Create figure
    fig = go.Figure(layout=dict(height=height, width=width))

    # Initial empty plot
    fig.add_trace(
        go.Scatter(
            x=df_f_total_aggregated.index,
            y=[None] * len(df_f_total_aggregated),
            mode="lines+markers",
            line=dict(color=orange_like, width=line_width),
            marker=dict(color=teal_like, size=marker_size),
            name="Ülkede Yabancılara Toplam Konut Satış",
        )
    )

    # Define frames for animation
    frames = [
        go.Frame(
            data=[
                go.Scatter(
                    x=df_f_total_aggregated.index[: k + 1],
                    y=df_f_total_aggregated["Total"][: k + 1],
                )
            ],
            name=str(k),
        )
        for k in range(len(df_f_total_aggregated))
    ]

    fig.frames = frames

    # Add play and pause buttons
    updatemenus = [
        {
            "buttons": [
                {
                    "args": [
                        None,
                        {
                            "frame": {"duration": 50, "redraw": True},
                            "fromcurrent": True,
                            "mode": "immediate",
                        },
                    ],
                    "label": "Play",
                    "method": "animate",
                },
                {
                    "args": [
                        [None],
                        {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"},
                    ],
                    "label": "Pause",
                    "method": "animate",
                },
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top",
        }
    ]

    # Update layout with buttons and animation settings
    fig.update_layout(
        title=f"Ülkede Yabancılara Toplam Konut Satış ({df_f_total_aggregated.index.min().year}-{df_f_total_aggregated.index.max().year})",
        xaxis_title="Tarih",
        yaxis_title="Toplam",
        # paper_bgcolor="rgb(0,0,0,0)",
        updatemenus=updatemenus,
        sliders=[
            {
                "yanchor": "top",
                "xanchor": "left",
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Tarih:",
                    "visible": True,
                    "xanchor": "right",
                },
                "transition": {"duration": 50, "easing": "linear"},
                "pad": {"b": 10, "t": 100},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [
                    {
                        "args": [
                            [str(k)],
                            {
                                "frame": {"duration": 50, "redraw": True},
                                "mode": "immediate",
                            },
                        ],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k in range(len(df_f_total_aggregated))
                ],
            }
        ],
    )
    fig.update_layout(
        design_animate(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
    )
    return fig


def total_sales_foreigners_plot(df_f_total_aggregated, width=None, height=800):

    # Calculate the min and max values for the x and y axis
    x_min = df_f_total_aggregated.index.min() - pd.Timedelta(days=2)
    x_max = df_f_total_aggregated.index.max() + pd.Timedelta(days=20)

    y_min = 0
    y_max = df_f_total_aggregated["Total"].max() * 1.2

    # Create figure
    fig = go.Figure(layout=dict(height=height, width=width))

    fig.add_trace(
        go.Scatter(
            x=df_f_total_aggregated.index,
            y=df_f_total_aggregated["Total"],
            mode="lines+markers",
            line=dict(color=orange_like, width=line_width),
            marker=dict(color=teal_like, size=marker_size),
            name="Ülkede Yabancılara Toplam Konut Satış",
        )
    )

    fig.update_layout(
        title=f"Ülkede Yabancılara Toplam Konut Satış ({df_f_total_aggregated.index.min().year}-{df_f_total_aggregated.index.max().year})",
        xaxis_title="Tarih",
        yaxis_title="Toplam",
    )
    fig.update_layout(
        design_animate(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max)
    )

    return fig


def total_sales_monthly_foreigners_plot(
    df_f_cities_aggregated, city_code, width=None, height=800
):
    """ """
    fig = go.Figure()
    try:
        if city_code == 0:
            for city in df_f_cities_aggregated["Şehir"].unique():
                city_data = df_f_cities_aggregated[
                    df_f_cities_aggregated["Şehir"] == city
                ]
                fig.add_trace(
                    go.Scatter(
                        x=city_data.index,
                        y=city_data["Total"],
                        mode="lines",
                        name=str(city_code_map.get(city)).capitalize(),
                        line=dict(width=line_width),
                    )
                )
            fig.update_layout(title="İllere Göre Yabancılara Konut Satışı (Ay Bazında)")
        else:
            p_city_code = city_code
            if city_code not in city_code_f:
                city_code = 99
            dff = df_f_cities_aggregated[df_f_cities_aggregated["Şehir"] == city_code]
            city_name = city_code_map.get(p_city_code, "Diğer Şehirler")

            fig.add_trace(
                go.Scatter(
                    x=dff.index,
                    y=dff["Total"],
                    mode="lines",
                    name=city_name,
                    line=dict(
                        width=line_width, color="blue"
                    ),  # You can customize the color as needed
                )
            )
            fig.update_layout(
                title=f"Yabancılara Konut Satışı (Ay Bazında): {city_name.capitalize()}",
                showlegend=False,
            )

        fig.update_layout(
            width=width,
            height=height,
            xaxis_title="Tarih",
            yaxis_title="Toplam",
        )

        # Apply additional design settings if needed
        fig.update_layout(design)

        return fig
    except Exception as e:
        print(f"Error in plot function: {e}")
        raise


def population_mah_plot(
    df_p, city_code=0, town_code=0, quarter_code=0, width=None, height=800
):
    # Create the figure with subplots
    labels = ["Erkek", "Kadın"]
    colors = ["skyblue", "salmon"]
    title = ""
    fig = go.Figure()

    if city_code == 0 and town_code == 0 and quarter_code == 0:
        title = "Bütün Ülke"
        values1 = df_p[["erkek", "kadin"]].sum().to_list()

    elif city_code != 0 and (town_code == 0 and quarter_code == 0):
        city_name = (
            df_p[df_p["il kayit no"] == city_code]["il adi"].iloc[0].capitalize()
        )
        title = f"{city_name}"

    elif city_code != 0 and (town_code != 0 and quarter_code == 0):
        city_name = (
            df_p[df_p["il kayit no"] == city_code]["il adi"].iloc[0].capitalize()
        )
        town_name = (
            df_p[df_p["ilçe kayit no"] == town_code]["ilçe adi"].iloc[0].capitalize()
        )
        title = f"{city_name}, {town_name}"
        values1 = df_p[
            (df_p["il kayit no"] == city_code) & (df_p["ilçe kayit no"] == town_code)
        ]
        values1 = values1[["erkek", "kadin"]].sum().to_list()

    elif city_code != 0 and (town_code != 0 and quarter_code != 0):
        city_name = (
            df_p[df_p["il kayit no"] == city_code]["il adi"].iloc[0].capitalize()
        )
        town_name = (
            df_p[df_p["ilçe kayit no"] == town_code]["ilçe adi"].iloc[0].capitalize()
        )
        quarter_name = (
            df_p[df_p["mahalle kayit no"] == quarter_code]["mahalle adi"]
            .iloc[0]
            .capitalize()
        )
        title = f"{city_name}, {town_name}, {quarter_name} Mh."
        values1 = df_p[
            (df_p["il kayit no"] == city_code)
            & (df_p["ilçe kayit no"] == town_code)
            & (df_p["mahalle kayit no"] == quarter_code)
        ]
        values1 = values1[["erkek", "kadin"]].sum().to_list()

    else:
        fig.add_annotation(
            text="Please enter either: Only city name, City name and Town name, or all three",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(family=font_family, size=20, color="black"),
        )

        # Update layout to remove axes
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
        )
        return fig

    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values1,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            textfont=dict(
                size=label_font_size,
                family=font_family,
                weight="bold",
            ),  # Adjust text size and color
            textinfo="label+percent",  # Show labels and percentages
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Cinsiyet Dağılımları: {title}",
        width=width,
        height=height,
        showlegend=False,
    )
    fig.update_layout(design)

    for annotation in fig["layout"]["annotations"]:
        annotation["y"] = 0.95  # Adjust this value for more/less padding

    # Add the text annotation below the plots
    fig.add_annotation(
        text=f"Toplam Nüfus: <b>{sum(values1):,}</b>",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.1,
        showarrow=False,
        font=dict(size=18, family=font_family, color="black"),
        align="center",
    )
    return fig


def population_plot(df_p, city_code=0, width=None, height=500):
    # Create the figure with subplots
    fig = make_subplots(
        rows=1,
        cols=3,
        specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
        subplot_titles=(
            df_p.iloc[city_code, 0].capitalize(),
            "İl ve İlçe Merkezleri",
            "Belde ve Köyler",
        ),
    )

    # Define the data for each pie chart
    values1 = [df_p.iloc[city_code, 2], df_p.iloc[city_code, 3]]
    values2 = [df_p.iloc[city_code, 5], df_p.iloc[city_code, 6]]
    values3 = [df_p.iloc[city_code, 8], df_p.iloc[city_code, 9]]
    labels = ["Erkek", "Kadın"]
    colors = ["skyblue", "salmon"]

    # Add the first pie chart
    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values1,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            pull=[0, 0],
            textfont=dict(
                size=label_font_size, family=font_family, color="black"
            ),  # Adjust text size and color
            textinfo="label+percent",  # Show labels and percentages
        ),
        row=1,
        col=1,
    )

    # Add the second pie chart
    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values2,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            pull=[0, 0],
            textfont=dict(
                size=label_font_size, family=font_family, color="black"
            ),  # Adjust text size and color
            textinfo="label+percent",  # Show labels and percentages
        ),
        row=1,
        col=2,
    )

    # Add the third pie chart
    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values3,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            pull=[0, 0],
            textfont=dict(
                size=label_font_size, family=font_family, color="black"
            ),  # Adjust text size and color
            textinfo="label+percent",  # Show labels and percentages
        ),
        row=1,
        col=3,
    )

    # Update layout
    fig.update_layout(
        title="Cinsiyet Dağılımları",
        width=width,
        height=height,
        title_font=dict(
            size=30,
            family=font_family,
        ),  # Adjust title font
        title_pad_b=10,
        font=dict(
            family=font_family,  # Adjust default font family for labels
            size=14,  # Adjust default font size for labels
            color="black",  # Adjust default font color for labels
        ),
        legend=dict(
            title_font=dict(size=18, family=font_family),  # Adjust legend title font
            font=dict(
                size=label_font_size, family=font_family
            ),  # Adjust legend item font
        ),
    )

    fig.update_layout(
        width=width,
        height=height,
        title_font=dict(size=30, family=font_family),
        xaxis=dict(
            tickangle=-45,
            tickfont=dict(family=font_family, size=12),
            showgrid=True,
            gridcolor="lightgray",
        ),
        yaxis=dict(
            tickfont=dict(family=font_family, size=12),
            tickformat=",",
            showgrid=True,
            gridcolor="lightgray",
        ),
        plot_bgcolor="#f3f4f6",
        xaxis_title_font=dict(
            size=20, family=font_family, color="black", weight="bold"
        ),
        yaxis_title_font=dict(
            size=20, family=font_family, color="black", weight="bold"
        ),
    )

    # Update subplot titles font and style

    for annotation in fig["layout"]["annotations"]:
        annotation["y"] = 0.95  # Adjust this value for more/less padding

        # Add the text annotation below the plots
    fig.add_annotation(
        text=f"Toplam Nüfus: <b>{df_p.iloc[city_code, 1]}</b>",
        xref="paper",
        yref="paper",
        x=0.5,
        y=-0.2,
        showarrow=False,
        font=dict(size=18, family=font_family, color="black"),
        align="center",
    )
    return fig


def price_age_plot(
    result: dict, data: list, width=None, height_age=700, height_price=500
):
    # Calculate min, max, median, and average prices from the result
    real_estate_prices = [item["price"] for item in data]
    min_price = result["min_price"]
    max_price = result["max_price"]
    avg_price = result["avg_price"]

    # Create the histogram
    hist_data = go.Histogram(x=real_estate_prices, nbinsx=30, name="", opacity=0.7)

    # Calculate the bell curve (normal distribution)
    mean = avg_price
    std_dev = np.std(real_estate_prices)
    x = np.linspace(min_price, max_price, 1000)
    y = (
        stats.norm.pdf(x, mean, std_dev) * len(real_estate_prices) * (x[1] - x[0]) * 30
    )  # scale y to match histogram

    # Create the normal distribution curve
    bell_curve = go.Scatter(
        x=x,
        y=y,
        mode="lines",
        name="Normal Dağılım",
        hovertemplate="%{x:,.0f} TL",
        line=dict(width=line_width),  # Increase the width of the line
    )

    # Create the vertical lines for lowest, average, and maximum prices
    lowest_line = go.Scatter(
        x=[min_price, min_price],
        y=[0, max(y)],
        mode="lines",
        name="Minimum Fiyat",
        line=dict(color="green", dash="dash"),
    )
    average_line = go.Scatter(
        x=[avg_price, avg_price],
        y=[0, max(y)],
        mode="lines",
        name="Ortalama Fiyat",
        line=dict(color="black", dash="dash"),
    )
    highest_line = go.Scatter(
        x=[max_price, max_price],
        y=[0, max(y)],
        mode="lines",
        name="Maksimum Fiyat",
        line=dict(color="red", dash="dash"),
    )

    # Create the figure and add the histogram, bell curve, and vertical lines
    fig_price = go.Figure(data=[bell_curve, lowest_line, average_line, highest_line])
    annotation_font_dict = dict(size=12, color="black")
    # Add annotations for the lowest, average, and maximum prices
    fig_price.add_annotation(
        x=min_price,
        y=max(y),
        text=f"Minimum Fiyat: <b>{min_price:,.0f} TL",
        showarrow=True,
        arrowhead=1,
        font=annotation_font_dict,
    )
    fig_price.add_annotation(
        x=avg_price,
        y=max(y),
        text=f"Ortalama Fiyat: <b>{avg_price:,.0f} TL",
        showarrow=True,
        arrowhead=1,
        font=annotation_font_dict,
    )
    fig_price.add_annotation(
        x=max_price,
        y=max(y),
        text=f"Maksimum Fiyat: <b>{max_price:,.0f} TL",
        showarrow=True,
        arrowhead=1,
        font=annotation_font_dict,
    )

    # Update layout for the price figure
    fig_price.update_layout(
        title_text="Fiyat İstatistiği",
        xaxis_title="Fiyat (TL)",
        yaxis=dict(
            showticklabels=False, showgrid=False
        ),  # Hide the y-axis ticks and labels
        width=width,
        height=height_price,
        bargap=0.2,  # Gap between bars
        legend=dict(orientation="h", yanchor="bottom", y=1.00, xanchor="right", x=1),
    )

    fig_price.update_layout(design)

    # Extract ages from the data field
    ages = [item["age"] for item in data]
    ages = sorted(ages)

    # Define age groups
    age_groups = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        "6-10": 0,
        "11-15": 0,
        "16-20": 0,
        "21-25": 0,
        "26-30": 0,
        "31+": 0,
    }

    # Categorize ages
    for age in ages:
        if age < 6:
            age_groups[age] += 1
        elif 6 <= age <= 10:
            age_groups["6-10"] += 1
        elif 11 <= age <= 15:
            age_groups["11-15"] += 1
        elif 16 <= age <= 20:
            age_groups["16-20"] += 1
        elif 21 <= age <= 25:
            age_groups["21-25"] += 1
        elif 26 <= age <= 30:
            age_groups["26-30"] += 1
        else:
            age_groups["31+"] += 1

    total_ages = len(ages)
    age_group_percentages = {
        group: count / total_ages * 100
        for group, count in age_groups.items()
        if count > 0
    }

    # Create the age distribution pie chart
    labels = list(age_group_percentages.keys())
    values = list(age_group_percentages.values())

    fig_age = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                hovertemplate="Bina Yaşı: %{label}<br>Yüzdelik: %{value:.1f}%<extra></extra>",
                sort=False,
                textfont=dict(
                    size=18,
                    family=font_family,
                    color="white",
                    weight="bold",
                ),
            )
        ]
    )

    # Update layout for the age figure
    fig_age.update_layout(
        title_text="Bina Yaşı Dağılımı",
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        width=width,
        height=height_age,
        title_x=0.5,
        title_xanchor="center",
    )
    fig_age.update_layout(design)

    return fig_price, fig_age


def population_marital_plot(
    df_married, df_never_married, df_divorced, df_widowed, city_code, height=600, width=None
):
    fig = make_subplots(
        rows=1,
        cols=4,
        specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}, {"type": "pie"}]],
        subplot_titles=(
            "Evli",
            "Hiç Evlenmedi",
            "Boşandı",
            "Eşi Vefat Etti",
        ),
    )

    # Define the data for each pie chart
    values1 = [df_married.iloc[city_code, 1], df_married.iloc[city_code, 2]]
    values2 = [df_never_married.iloc[city_code, 1], df_never_married.iloc[city_code, 2]]
    values3 = [df_divorced.iloc[city_code, 1], df_divorced.iloc[city_code, 2]]
    values4 = [df_widowed.iloc[city_code, 1], df_widowed.iloc[city_code, 2]]
    labels = ["Erkek", "Kadın"]
    colors = ["skyblue", "salmon"]

    # Add the first pie chart
    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values1,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            pull=[0, 0],
            textfont=dict(
                size=16,
                family=font_family,
                color="black",
                weight="bold",
            ),
            textinfo="label+percent",  # Show labels and percentages
        ),
        row=1,
        col=1,
    )

    # Add the second pie chart
    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values2,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            pull=[0, 0],
            textfont=dict(
                size=16,
                family=font_family,
                color="black",
                weight="bold",
            ),
            textinfo="label+percent",  # Show labels and percentages
        ),
        row=1,
        col=2,
    )

    # Add the third pie chart
    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values3,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            pull=[0, 0],
            textfont=dict(
                size=16,
                family=font_family,
                color="black",
                weight="bold",
            ),
            textinfo="label+percent",  # Show labels and percentages
        ),
        row=1,
        col=3,
    )
    fig.add_trace(
        go.Pie(
            name="",
            labels=labels,
            values=values4,
            marker=dict(colors=colors),
            hovertemplate="<b>%{label}</b><br>%{value}",
            pull=[0, 0],
            # Adjust text size and color
            textfont=dict(
                size=16,
                family=font_family,
                color="black",
                weight="bold",
            ),
            textinfo="label+percent",  # Show labels and percentages
        ),
        row=1,
        col=4,
    )

    fig.update_layout(
        title=f"Evlilik Durumuna Göre Nüfus: {city_code_map.get(city_code, "Şehir Bulunamadı").capitalize()}",
        width=width,
        height=height,
        title_pad_b=10,
        showlegend=False,
    )

    fig.update_layout(design)

    return fig

def population_origin_city_plot(df_origin_city, city_code=1, height=800, width=None):
    labels = [city_code_map.get(i).capitalize() for i in df_origin_city.columns[1:] if i!=city_code]
    values = df_origin_city.loc[city_code][1:]

    # Group smaller categories into "Other"
    threshold = 0.01 * sum(values)
    labels_grouped = []
    values_grouped = []
    other_value = 0

    for label, value in zip(labels, values):
        if value < threshold:
            other_value += value
        else:
            labels_grouped.append(label)
            values_grouped.append(value)

    if other_value > 0:
        labels_grouped.append('Diğer')
        values_grouped.append(other_value)

    fig = go.Figure(
        data=[
            go.Pie(
                name="",
                labels=labels_grouped,
                values=values_grouped,
                hovertemplate="<b>%{label}</b><br>%{value} = %{percent}",
                textfont=dict(
                    size=18,
                    family=font_family,
                    weight="bold",
                ),
                textinfo="label",  # Show labels and percentages
                marker=dict(colors=color_sequence),
                sort=True,
            )
        ]
    )

    # Update layout for the age figure
    fig.update_layout(
        title_text=f"İkamet Edilen İle göre Nüfus Kütüğüne Kayıtlı Olunan İl: {city_code_map.get(city_code, "Şehir Bulunamadı").capitalize()}",
        height=height,  # Increase height to give more space
        width=width,   # Increase width to give more space
        margin=dict(t=100, b=100, l=100, r=100),  # Adjust margins
        showlegend=False,
    )

    fig.update_layout(design)
    return fig


def population_trend_plot(df_trend, city_code=1, height=800, width=None):
    # Sample data
    df_filtered = df_trend[df_trend["il kayit no"]==city_code]
    colors = ['lightgreen' if x > 0 else 'tomato' for x in df_filtered['artis']]

    # Create the bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                name="Population Change",
                x=df_filtered['ilçe original'],
                y=df_filtered['artis'],
                text=df_filtered['artis'],
                textposition='auto',
                marker=dict(color=colors),
            )
        ]
    )

    # Update layout for the bar chart
    fig.update_layout(
        title_text=f"Nüfus Değişimi: {city_code_map.get(city_code).capitalize()}",
        height=height,
        width=width,
        margin=dict(t=100, b=200, l=100, r=100),
        xaxis_title="İlçe",
        yaxis_title="Değişim (%)",
    )
    fig.update_layout(design)

    return fig
