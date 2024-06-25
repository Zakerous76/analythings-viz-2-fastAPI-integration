import plotly.graph_objs as go
import pandas as pd

def animate(df_totals_total_granular):

    # df_totals_total_granular is your DataFrame and has the necessary data
    # Calculate the min and max values for the x and y axis
    x_min = df_totals_total_granular.index.min() - pd.Timedelta(days=2)
    x_max = df_totals_total_granular.index.max() + pd.Timedelta(days=20)
    y_min = 0
    y_max = df_totals_total_granular['Total'].max()*1.2

    # Create figure
    fig = go.Figure(layout=dict(height=800, width=1800))

    # Initial empty plot
    fig.add_trace(go.Scatter(x=df_totals_total_granular.index, y=[None]*len(df_totals_total_granular), mode="lines+markers", line=dict(color='orange'), marker=dict(color="teal"), name='İllere Göre Toplam Konut Satış (2013-2024)'))

    # Define frames for animation
    frames = [go.Frame(data=[go.Scatter(x=df_totals_total_granular.index[:k+1], y=df_totals_total_granular['Total'][:k+1])], name=str(k)) for k in range(len(df_totals_total_granular))]

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
        title='İllere Göre Toplam Konut Satış (2013-2024)',
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
                    'method': 'animate'} for k in range(len(df_totals_total_granular))]
        }]
    )

    return fig