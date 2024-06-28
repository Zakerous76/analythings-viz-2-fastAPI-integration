from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse
import uvicorn
from prep_data import *
from plot import *
import plotly.io as pio
import plotly.graph_objs as go

app = FastAPI()
df_totals_total, df_totals_cities, df_granular, df_granular_cities = sales_by_cities_df() 
df_f_total_aggregated, df_f_cities_aggregated = sales_by_cities_foreigners_df()
df_p = population_df()

def create_html_button(label, link):
    return f'<button onclick="window.location.href=\'{link}\'">{label}</button>'


# Create an endpoint
@app.get("/", response_class=HTMLResponse)
async def get_home():
    html_content = """
    <html>
        <head>
            <title>Real Estate Sales Dashboard</title>
        </head>
        <body>
            <h1>Real Estate Sales Dashboard</h1>
            <div>
                {buttons}
            </div>
        </body>
    </html>
    """
    buttons = [
        create_html_button("Total Sales", "/total_sales"),
        create_html_button("Total Sales (Animate)", "/total_sales_animate"),
        create_html_button("Sales by Cities", "/sales_by_cities"),
        create_html_button("Sales by Cities (Animate)", "/sales_by_cities_animate")
    ]
    return HTMLResponse(content=html_content.format(buttons=" ".join(buttons)))


@app.get("/total_sales")
async def get_total_sales():
    fig = total_sales_plot(df_granular)
    graph_html = pio.to_html(fig, full_html=False) # will return a single <div> element
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

@app.get("/total_sales_animate")
async def get_total_sales_animate():
    fig = total_sales_animate(df_granular)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

@app.get("/total_sales_yearly/") # city_name is optional. if not provided, will return for all cities
async def get_total_sales_yearly(city_name: str = None):
    fig = total_sales_yearly_plot(df_totals_cities, city_name)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

@app.get("/total_sales_monthly/{city_name}") # city_name is optional. if not provided, will return for all cities
async def get_total_sales_yearly(city_name: str = None):
    fig = total_sales_monthly_plot(df_granular_cities, city_name)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

# # TODO: Fix this
# @app.get("/sales_by_cities_animate")
# async def get_sales_by_cities_animate():
#     fig = total_sales_animate(df_granular)
#     graph_html = pio.to_html(fig, full_html=False)
#     return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")


# ------------------------------------------------------------------------------------------------
# Dashboard Visualizations

@app.get("/total_sales_to_foreigners_animate")
async def get_total_sales_to_foreigners_animate():
    fig = total_sales_foreigners_animate(df_f_total_aggregated)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")


@app.get("/total_sales_monthly_foreigners/") # if city name not in list, return for others
async def get_total_sales_monthly_foreigners(city_name: str = None):
    fig = total_sales_monthly_foreigners_plot(df_f_total_aggregated, city_name)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

@app.get("/population_plot") # with gender
async def get_population_plot(city_code: int = 0):
    fig = population_plot(df_p, city_code)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")


@app.get("/population_map") # with gender
async def get_population_map():
    pass


# ------------------------------------------------------------------------------------------------
# Report

# TODO: population by age group
# TODO: population by gender
# TODO: population of foreigners
# TODO: population by marital status
# TODO: Yaş Grubu ve Cinsiyete Göre İl/İlçe Merkezi ve Belde / Köy Nüfusu
# TODO: Education Level



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)