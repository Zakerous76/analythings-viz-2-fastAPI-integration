import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

city_code_map = {0: 'ÜLKE',
 1: 'ADANA',
 2: 'ADIYAMAN',
 3: 'AFYONKARAHİSAR',
 4: 'AĞRI',
 5: 'AMASYA',
 6: 'ANKARA',
 7: 'ANTALYA',
 8: 'ARTVİN',
 9: 'AYDIN',
 10: 'BALIKESİR',
 11: 'BİLECİK',
 12: 'BİNGÖL',
 13: 'BİTLİS',
 14: 'BOLU',
 15: 'BURDUR',
 16: 'BURSA',
 17: 'ÇANAKKALE',
 18: 'ÇANKIRI',
 19: 'ÇORUM',
 20: 'DENİZLİ',
 21: 'DİYARBAKIR',
 22: 'EDİRNE',
 23: 'ELAZIĞ',
 24: 'ERZİNCAN',
 25: 'ERZURUM',
 26: 'ESKİŞEHİR',
 27: 'GAZİANTEP',
 28: 'GİRESUN',
 29: 'GÜMÜŞHANE',
 30: 'HAKKARİ',
 31: 'HATAY',
 32: 'ISPARTA',
 33: 'MERSİN',
 34: 'İSTANBUL',
 35: 'İZMİR',
 36: 'KARS',
 37: 'KASTAMONU',
 38: 'KAYSERİ',
 39: 'KIRKLARELİ',
 40: 'KIRŞEHİR',
 41: 'KOCAELİ',
 42: 'KONYA',
 43: 'KÜTAHYA',
 44: 'MALATYA',
 45: 'MANİSA',
 46: 'KAHRAMANMARAŞ',
 47: 'MARDİN',
 48: 'MUĞLA',
 49: 'MUŞ',
 50: 'NEVŞEHİR',
 51: 'NİĞDE',
 52: 'ORDU',
 53: 'RİZE',
 54: 'SAKARYA',
 55: 'SAMSUN',
 56: 'SİİRT',
 57: 'SİNOP',
 58: 'SİVAS',
 59: 'TEKİRDAĞ',
 60: 'TOKAT',
 61: 'TRABZON',
 62: 'TUNCELİ',
 63: 'ŞANLIURFA',
 64: 'UŞAK',
 65: 'VAN',
 66: 'YOZGAT',
 67: 'ZONGULDAK',
 68: 'AKSARAY',
 69: 'BAYBURT',
 70: 'KARAMAN',
 71: 'KIRIKKALE',
 72: 'BATMAN',
 73: 'ŞIRNAK',
 74: 'BARTIN',
 75: 'ARDAHAN',
 76: 'IĞDIR',
 77: 'YALOVA',
 78: 'KARABÜK',
 79: 'KİLİS',
 80: 'OSMANİYE',
 81: 'DÜZCE',
 99: 'Diğer iller - Other Provinces'}
city_code_f = [48, 33, 35, 16, 99,  9,  7, 54,  6, 34, 77, 61, 55, 41]

def total_sales_animate(df_granular):

    # df_granular is your DataFrame and has the necessary data
    # Calculate the min and max values for the x and y axis
    x_min = df_granular.index.min() - pd.Timedelta(days=2)
    x_max = df_granular.index.max() + pd.Timedelta(days=20)
    y_min = 0
    y_max = df_granular['Total'].max()*1.2

    # Create figure
    fig = go.Figure(layout=dict(height=800, width=1800))

    # Initial empty plot
    fig.add_trace(go.Scatter(x=df_granular.index, y=[None]*len(df_granular), mode="lines+markers", line=dict(color='orange'), marker=dict(color="teal"), name='Ülkede Toplam Konut Satış'))

    # Define frames for animation
    frames = [go.Frame(data=[go.Scatter(x=df_granular.index[:k+1], y=df_granular['Total'][:k+1])], name=str(k)) for k in range(len(df_granular))]

    fig.frames = frames

    # Add play and pause buttons
    updatemenus = [
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]

    # Update layout with buttons and animation settings
    fig.update_layout(
        title=f'Ülkede Toplam Konut Satış ({df_granular.index.min().year}-{df_granular.index.max().year})',
        xaxis_title='Tarih',
        yaxis_title='Toplam',
        title_font=dict(size=30, family="Roboto"),
        xaxis=dict(tickangle=-45, tickfont=dict(family="Roboto", size=12), showgrid=True, range=[x_min, x_max]),
        yaxis=dict(tickfont=dict(family="Roboto", size=12), tickformat=',', showgrid=True, range=[y_min, y_max]),
        margin=dict(l=110, r=20, t=100, b=110),
        hovermode='x',
        legend=dict(font=dict(family="Roboto", size=12), yanchor="top", y=0.99, xanchor="right", x=0.99),
        xaxis_title_font=dict(size=20, family="Roboto", color='black', weight='bold'),
        yaxis_title_font=dict(size=20, color='black', weight='bold'),
        updatemenus=updatemenus,
        sliders=[{
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Tarih:',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 50, 'easing': 'linear'},
            'pad': {'b': 10, 't': 100},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': [{'args': [[str(k)], {'frame': {'duration': 50, 'redraw': True}, 'mode': 'immediate'}],
                    'label': str(k),
                    'method': 'animate'} for k in range(len(df_granular))]
        }]
    )

    return fig

def total_sales_plot(df_granular):

    # Calculate the min and max values for the x and y axis
    x_min = df_granular.index.min() - pd.Timedelta(days=2)
    x_max = df_granular.index.max() + pd.Timedelta(days=20)
    
    y_min = 0
    y_max = df_granular['Total'].max()*1.2

    # Create figure
    fig = go.Figure(layout=dict(height=800, width=1800))

    # Initial empty plot
    fig.add_trace(go.Scatter(x=df_granular.index, y=df_granular["Total"], mode="lines+markers", line=dict(color='orange'), marker=dict(color="teal"), name='Ülkede Toplam Konut Satış'))

    # Update layout with buttons and animation settings
    fig.update_layout(
        title=f'Ülkede Toplam Konut Satış ({df_granular.index.min().year}-{df_granular.index.max().year})',
        xaxis_title='Tarih',
        yaxis_title='Toplam',
        title_font=dict(size=30, family="Roboto"),
        xaxis=dict(tickangle=-45, tickfont=dict(family="Roboto", size=12), showgrid=True, range=[x_min, x_max]),
        yaxis=dict(tickfont=dict(family="Roboto", size=12), tickformat=',', showgrid=True, range=[y_min, y_max]),
        margin=dict(l=110, r=20, t=100, b=110),
        hovermode='x',
        legend=dict(font=dict(family="Roboto", size=12), yanchor="top", y=0.99, xanchor="right", x=0.99),
        xaxis_title_font=dict(size=20, family="Roboto", color='black', weight='bold'),
        yaxis_title_font=dict(size=20, color='black', weight='bold'),
    )

    return fig

def total_sales_yearly_plot(df_totals_cities, city_code=0):
    """
        City must be spelled properly
    """
    if city_code == 0:
        fig = go.Figure(data=[go.Scatter(name=city_code_map[city], x=df_totals_cities.index, y=df_totals_cities[city]) for city in df_totals_cities.columns], 
                    layout=dict(height=800, width=1800))
        fig.update_layout(title="İllere Göre Konut Satışı (Yıl Bazında)", xaxis_title="Yıl", yaxis_title="Toplam Konut Satışı", barmode='stack')
        fig.update_xaxes(tickmode='linear')    
    else:
        fig = go.Figure(data=[go.Scatter(name=city_code_map[city_code], x=df_totals_cities.index, y=df_totals_cities[city_code])], layout=dict(height=800, width=1800))
        fig.update_layout(title=f"Konut Satışı (Yıl Bazında): {city_code_map[city_code].capitalize()}", xaxis_title="Yıl", yaxis_title="Toplam Konut Satışı", barmode='stack')
        fig.update_xaxes(tickmode='linear') 
    return fig

# city => cities
def total_sales_monthly_plot(df_granular_cities, city_code=0):
    """
        City must be spelled properly
    """
    if city_code == 0:
        fig = go.Figure(data=[go.Scatter(name=city_code_map[city], x=df_granular_cities.index, y=df_granular_cities[city]) for city in df_granular_cities.columns], 
                layout=dict(height=800, width=1800))
        fig.update_layout(title="İllere Göre Konut Satışı (Ay bazında)", xaxis_title="Yıl", yaxis_title="Toplam Konut Satışı", barmode='stack')
  
    else:
        fig = go.Figure(data=[go.Scatter(name=city_code_map[city_code], x=df_granular_cities.index, y=df_granular_cities[city_code])], layout=dict(height=800, width=1800))
        fig.update_layout(title=f"Konut Satışı (Ay Bazında): {city_code_map[city_code].capitalize()}", yaxis_title="Toplam Konut Satışı", barmode='stack')

    return fig


def total_sales_foreigners_animate(df_f_total_aggregated):

    # df_F_total_aggregated is your DataFrame and has the necessary data
    # Calculate the min and max values for the x and y axis
    x_min = df_f_total_aggregated.index.min() - pd.Timedelta(days=2)
    x_max = df_f_total_aggregated.index.max() + pd.Timedelta(days=20)
    y_min = 0
    y_max = df_f_total_aggregated['Total'].max()*1.2

    # Create figure
    fig = go.Figure(layout=dict(height=800, width=1800))

    # Initial empty plot
    fig.add_trace(go.Scatter(x=df_f_total_aggregated.index, y=[None]*len(df_f_total_aggregated), mode="lines+markers", line=dict(color='orange'), marker=dict(color="teal"), name='Ülkede Yabancılara Toplam Konut Satış'))

    # Define frames for animation
    frames = [go.Frame(data=[go.Scatter(x=df_f_total_aggregated.index[:k+1], y=df_f_total_aggregated['Total'][:k+1])], name=str(k)) for k in range(len(df_f_total_aggregated))]

    fig.frames = frames

    # Add play and pause buttons
    updatemenus = [
        {
            'buttons': [
                {
                    'args': [None, {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True, 'mode': 'immediate'}],
                    'label': 'Play',
                    'method': 'animate'
                },
                {
                    'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate'}],
                    'label': 'Pause',
                    'method': 'animate'
                }
            ],
            'direction': 'left',
            'pad': {'r': 10, 't': 87},
            'showactive': False,
            'type': 'buttons',
            'x': 0.1,
            'xanchor': 'right',
            'y': 0,
            'yanchor': 'top'
        }
    ]

    # Update layout with buttons and animation settings
    fig.update_layout(
        title=f'Ülkede Yabancılara Toplam Konut Satış ({df_f_total_aggregated.index.min().year}-{df_f_total_aggregated.index.max().year})',
        xaxis_title='Tarih',
        yaxis_title='Toplam',
        title_font=dict(size=30, family="Roboto"),
        xaxis=dict(tickangle=-45, tickfont=dict(family="Roboto", size=12), showgrid=True, range=[x_min, x_max]),
        yaxis=dict(tickfont=dict(family="Roboto", size=12), tickformat=',', showgrid=True, range=[y_min, y_max]),
        margin=dict(l=110, r=20, t=100, b=110),
        hovermode='x',
        legend=dict(font=dict(family="Roboto", size=12), yanchor="top", y=0.99, xanchor="right", x=0.99),
        xaxis_title_font=dict(size=20, family="Roboto", color='black', weight='bold'),
        yaxis_title_font=dict(size=20, color='black', weight='bold'),
        updatemenus=updatemenus,
        sliders=[{
            'yanchor': 'top',
            'xanchor': 'left',
            'currentvalue': {
                'font': {'size': 20},
                'prefix': 'Tarih:',
                'visible': True,
                'xanchor': 'right'
            },
            'transition': {'duration': 50, 'easing': 'linear'},
            'pad': {'b': 10, 't': 100},
            'len': 0.9,
            'x': 0.1,
            'y': 0,
            'steps': [{'args': [[str(k)], {'frame': {'duration': 50, 'redraw': True}, 'mode': 'immediate'}],
                    'label': str(k),
                    'method': 'animate'} for k in range(len(df_f_total_aggregated))]
        }]
    )

    return fig

def total_sales_foreigners_plot(df_f_total_aggregated):

    # Calculate the min and max values for the x and y axis
    x_min = df_f_total_aggregated.index.min() - pd.Timedelta(days=2)
    x_max = df_f_total_aggregated.index.max() + pd.Timedelta(days=20)
    
    y_min = 0
    y_max = df_f_total_aggregated['Total'].max()*1.2

    # Create figure
    fig = go.Figure(layout=dict(height=800, width=1800))

    # Initial empty plot
    fig.add_trace(go.Scatter(x=df_f_total_aggregated.index, y=df_f_total_aggregated["Total"], mode="lines+markers", line=dict(color='orange'), marker=dict(color="teal"), name='Ülkede Yabancılara Toplam Konut Satış'))

    # Update layout with buttons and animation settings
    fig.update_layout(
        title=f'Ülkede Yabancılara Toplam Konut Satış ({df_f_total_aggregated.index.min().year}-{df_f_total_aggregated.index.max().year})',
        xaxis_title='Tarih',
        yaxis_title='Toplam',
        title_font=dict(size=30, family="Roboto"),
        xaxis=dict(tickangle=-45, tickfont=dict(family="Roboto", size=12), showgrid=True, range=[x_min, x_max]),
        yaxis=dict(tickfont=dict(family="Roboto", size=12), tickformat=',', showgrid=True, range=[y_min, y_max]),
        margin=dict(l=110, r=20, t=100, b=110),
        hovermode='x',
        legend=dict(font=dict(family="Roboto", size=12), yanchor="top", y=0.99, xanchor="right", x=0.99),
        xaxis_title_font=dict(size=20, family="Roboto", color='black', weight='bold'),
        yaxis_title_font=dict(size=20, color='black', weight='bold'),
    )

    return fig

def total_sales_monthly_foreigners_plot(df_f_cities_aggregated, city_code=0):
    """

    """
    fig = go.Figure()
    try:
        if city_code == 0:
            fig = px.line(df_f_cities_aggregated, x=df_f_cities_aggregated.index, 
                            y='Total', color='Şehir', title='İllere Göre Yabancılara Konut Satışı (Ay Bazında)')
        else:
            p_city_code = city_code
            if city_code not in city_code_f:
                city_code = 99
            dff = df_f_cities_aggregated[df_f_cities_aggregated['Şehir'] == city_code]
            
            fig = px.line(dff, x=dff.index, y='Total', color='Şehir', title=f'Yabancılara Konut Satışı (Ay Bazında): {city_code_map[p_city_code].capitalize()}',
                            color_discrete_sequence=px.colors.qualitative.Vivid)
            fig.update_layout(showlegend=False)
        fig.update_layout(width=1800, height=800)
        return fig
    except Exception as e:
        print(f"Error in plot function: {e}")
        raise

def population_map():
    pass

def population_mah_plot(df_p, city_name=None, town_name=None, district_name=None):
    # Create the figure with subplots
    labels = ['Erkek', 'Kadın']
    colors = ['skyblue', 'salmon']
    title = ""
    fig = go.Figure()

    if city_name=="" and town_name=="" and district_name=="":
        title = "Bütün Ülke"
        values1 = df_p[["erkek", "kadin"]].sum().to_list()
        fig.add_trace(go.Pie(
            name="",
            labels=labels,
            values=values1,
            marker=dict(colors=colors),
            hovertemplate='<b>%{label}</b><br>%{value}',
            pull=[0, 0],
            textfont=dict(size=16, family="Balto", color="black"),  # Adjust text size and color
            textinfo='label+percent',  # Show labels and percentages
        ))
    
    elif city_name!="" and (town_name=="" and district_name==""):
        title = city_name.capitalize()
        values1 = df_p[df_p["il adi"]==city_name.upper()]
        values1 = values1[["erkek", "kadin"]].sum().to_list()
        fig.add_trace(go.Pie(
            name="",
            labels=labels,
            values=values1,
            marker=dict(colors=colors),
            hovertemplate='<b>%{label}</b><br>%{value}',
            pull=[0, 0],
            textfont=dict(size=16, family="Balto", color="black"),  # Adjust text size and color
            textinfo='label+percent',  # Show labels and percentages
        ))
    
    elif city_name!="" and (town_name!="" and district_name==""):
        title = f"{city_name.capitalize()}, {town_name.capitalize()}"
        values1 = df_p[(df_p["il adi"]==city_name.upper()) & (df_p["ilçe adi"]==town_name.upper())]
        values1 = values1[["erkek", "kadin"]].sum().to_list()
        fig.add_trace(go.Pie(
            name="",
            labels=labels,
            values=values1,
            marker=dict(colors=colors),
            hovertemplate='<b>%{label}</b><br>%{value}',
            pull=[0, 0],
            textfont=dict(size=16, family="Balto", color="black"),  # Adjust text size and color
            textinfo='label+percent',  # Show labels and percentages
        ))
    
    elif city_name!="" and (town_name!="" and district_name!=""):
        title = f"{city_name.capitalize()}, {town_name.capitalize()}, {district_name.capitalize()} Mh."
        if len(district_name.split()) > 1:
            district_name = district_name + " Mh."
        values1 = df_p[(df_p["il adi"]==city_name.upper()) & (df_p["ilçe adi"]==town_name.upper()) & (df_p["mahalle adi"]==" ".join(district_name.split()[:-1]).upper())] # assuming that every mahalle ends with MH.
        values1 = values1[["erkek", "kadin"]].sum().to_list()
        fig.add_trace(go.Pie(
            name="",
            labels=labels,
            values=values1,
            marker=dict(colors=colors),
            hovertemplate='<b>%{label}</b><br>%{value}',
            pull=[0, 0],
            textfont=dict(size=16, family="Balto", color="black"),  # Adjust text size and color
            textinfo='label+percent',  # Show labels and percentages
        ))
    else:
        fig.add_annotation(
        text="Please enter either: Only city name, City name and Town name, or all three",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(
            family="Balto, Arial, sans-serif",
            size=20,
            color="black"
            )
        )

        # Update layout to remove axes
        fig.update_layout(
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0, r=0, t=0, b=0)
        )
        return fig

    # Update layout
    fig.update_layout(
        title=f'Cinsiyet Dağılımları: {title}',
        width=900,
        height=500,
        title_font=dict(size=30, family="Balto", ),  # Adjust title font
        title_pad_b=10,
        font=dict(
            family="Balto",  # Adjust default font family for labels
            size=14,  # Adjust default font size for labels
            color="black"  # Adjust default font color for labels
        ),
        showlegend=False
    )

    for annotation in fig['layout']['annotations']:
        annotation['y'] = 0.95  # Adjust this value for more/less padding

    # Add the text annotation below the plots
    fig.add_annotation(
        text=f"Toplam Nüfus: <b>{sum(values1):,}</b>",
        xref="paper", yref="paper",
        x=0.5, y=-0.2,
        showarrow=False,
        font=dict(size=18, family="Balto", color="black"),
        align="center"
    )
    return fig

def population_plot(df_p, city_code=0):
    # Create the figure with subplots
    fig = make_subplots(rows=1, cols=3, specs=[[{'type': 'pie'}, {'type': 'pie'}, {'type': 'pie'}]], subplot_titles=(df_p.iloc[city_code, 0].capitalize(), "İl ve İlçe Merkezleri", "Belde ve Köyler"))

    # Define the data for each pie chart
    values1 = [df_p.iloc[city_code, 2], df_p.iloc[city_code, 3]]
    values2 = [df_p.iloc[city_code, 5], df_p.iloc[city_code, 6]]
    values3 = [df_p.iloc[city_code, 8], df_p.iloc[city_code, 9]]
    labels = ['Erkek', 'Kadın']
    colors = ['skyblue', 'salmon']

    # Add the first pie chart
    fig.add_trace(go.Pie(
        name="",
        labels=labels,
        values=values1,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>%{value}',
        pull=[0, 0],
        textfont=dict(size=16, family="Balto", color="black"),  # Adjust text size and color
        textinfo='label+percent',  # Show labels and percentages
    ), row=1, col=1)

    # Add the second pie chart
    fig.add_trace(go.Pie(
        name="",
        labels=labels,
        values=values2,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>%{value}',
        pull=[0, 0],
        textfont=dict(size=16, family="Balto", color="black"),  # Adjust text size and color
        textinfo='label+percent',  # Show labels and percentages
    ), row=1, col=2)

    # Add the third pie chart
    fig.add_trace(go.Pie(
        name="",
        labels=labels,
        values=values3,
        marker=dict(colors=colors),
        hovertemplate='<b>%{label}</b><br>%{value}',
        pull=[0, 0],
        textfont=dict(size=16, family="Balto", color="black"),  # Adjust text size and color
        textinfo='label+percent',  # Show labels and percentages
    ), row=1, col=3)

    # Update layout
    fig.update_layout(
        title='Cinsiyet Dağılımları',
        width=1100,
        height=500,
        title_font=dict(size=30, family="Balto", ),  # Adjust title font
        title_pad_b=10,
        font=dict(
            family="Balto",  # Adjust default font family for labels
            size=14,  # Adjust default font size for labels
            color="black"  # Adjust default font color for labels
        ),
        legend=dict(
            title_font=dict(size=18, family="Balto"),  # Adjust legend title font
            font=dict(size=16, family="Balto")  # Adjust legend item font
        )
    )

    # Update subplot titles font and style

    for annotation in fig['layout']['annotations']:
        annotation['y'] = 0.95  # Adjust this value for more/less padding

        # Add the text annotation below the plots
    fig.add_annotation(
    text=f"Toplam Nüfus: <b>{df_p.iloc[city_code, 1]}</b>",
    xref="paper", yref="paper",
    x=0.5, y=-0.2,
    showarrow=False,
    font=dict(size=18, family="Balto", color="black"),
    align="center"
)
    return fig


def sales_by_cities_stacked_plot(df_totals_cities):
    cols = df_totals_cities.columns[:-1]
    print(cols)
    fig = go.Figure(data=[go.Bar(name=city, x=df_totals_cities['Yıl/Ay'], y=df_totals_cities[city]) for city in cols])
    fig.update_layout(title="Sales by Cities", xaxis_title="Year/Month", yaxis_title="Total Sales", barmode='stack')
    # fig = px.area(df_totals_cities, x='Yıl/Ay', y=df_totals_cities, color=df_totals_cities, title='Real Estate Sold Over Time')
    return fig