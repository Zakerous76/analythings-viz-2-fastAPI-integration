from fastapi import FastAPI, Path, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
import plotly.io as pio
import plotly.graph_objs as go
from prep_data import *
from plot import *
app = FastAPI()
df_totals_total, df_totals_cities, df_granular, df_granular_cities = sales_by_cities_df() 
df_f_total_aggregated, df_f_cities_aggregated = sales_by_cities_foreigners_df()
df_p = population_df()


class PlotRequest(BaseModel):
    plot_type: str
    data: dict

def create_html_button(label, link):
    return f'<button onclick="window.location.href=\'{link}\'">{label}</button>'

def create_html_form(label, action, input_name):
    return f"""
    <form action="{action}" method="get">
        <label for="{input_name}">{label}:</label>
        <input type="text" id="{input_name}" name="{input_name}">
        <input type="submit" value="Submit">
    </form>
    """

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
                {forms}
            </div>
        </body>
    </html>
    """
    buttons = [
        create_html_button("Total Sales (Animate)", "/total_sales_animate"),
        create_html_button("Sales by Cities (Animate)", "/sales_by_cities_animate"),
        create_html_button("Total Sales to Foreigners (Animate)", "/total_sales_to_foreigners_animate"),
        create_html_button("Population Plot", "/population_plot")
    ]
    forms = [
        create_html_form("Total Sales (start_year end_year)", "/total_sales", "interval"),
        create_html_form("Total Sales Yearly (city_name)", "/total_sales_yearly", "city_name"),
        create_html_form("Total Sales Monthly (city_name)", "/total_sales_monthly", "city_name"),
        create_html_form("Total Sales Monthly Foreigners (city_name)", "/total_sales_monthly_foreigners", "city_name")
    ]
    return HTMLResponse(content=html_content.format(buttons=" ".join(buttons), forms=" ".join(forms)))



@app.get("/total_sales")
async def get_total_sales(interval: str = Query(None, title="City Name", description="Name of the city")):
    start_year, end_year = int(interval.split()[0]), int(interval.split()[1])
    fig = total_sales_plot(df_granular[(df_granular.index.year <= end_year) & (df_granular.index.year >= start_year)])
    graph_html = pio.to_html(fig, full_html=False) # will return a single <div> element
    return HTMLResponse(content=f"{graph_html}")

@app.get("/total_sales_animate")
async def get_total_sales_animate():
    fig = total_sales_animate(df_granular)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")

@app.get("/total_sales_yearly/")
async def get_total_sales_yearly(city_name: int = Query(None, title="City Name", description="Name of the city")):
    fig = total_sales_yearly_plot(df_totals_cities, city_name)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")

@app.get("/total_sales_monthly/")
async def get_total_sales_monthly(city_name: str = Query(None, title="City Name", description="Name of the city")):
    fig = total_sales_monthly_plot(df_granular_cities, city_name)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")

@app.post("/create-plot/", response_class=HTMLResponse)
async def create_plot(plot_request: PlotRequest):
    plot_type = plot_request.plot_type
    data = plot_request.data

    # Create a plot based on the plot_type
    if plot_type == "bar":
        fig = go.Figure(data=[go.Bar(x=data['x'], y=data['y'])])
    elif plot_type == "line":
        fig = go.Figure(data=[go.Scatter(x=data['x'], y=data['y'], mode='lines')])
    else:
        raise HTTPException(status_code=400, detail="Invalid plot type")

    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")

@app.get("/total_sales_to_foreigners_animate")
async def get_total_sales_to_foreigners_animate():
    fig = total_sales_foreigners_animate(df_f_total_aggregated)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")

@app.get("/total_sales_monthly_foreigners/")
async def get_total_sales_monthly_foreigners(city_name: str = Query(None, title="City Name", description="Name of the city")):
    try:
        fig = total_sales_monthly_foreigners_plot(df_f_total_aggregated, city_name)
        graph_html = pio.to_html(fig, full_html=False)
        return HTMLResponse(content=f"{graph_html}")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the plot.")


@app.get("/population_plot")
async def get_population_plot(city_code: int = Query(0, title="City Code", description="Code of the city")):
    fig = population_plot(df_p, city_code)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")


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