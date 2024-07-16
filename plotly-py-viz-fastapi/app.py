from fastapi import FastAPI, Path, HTTPException, Request, Query
from fastapi.responses import HTMLResponse
import uvicorn
from pydantic import BaseModel
import plotly.io as pio
import plotly.graph_objs as go
from prep_data import *
from plot import *
app = FastAPI()
df_totals_total, df_totals_cities, df_granular, df_granular_cities = sales_cities_df() 
df_f_total_aggregated, df_f_cities_aggregated = sales_cities_foreigners_df()
df_p = population_df()


class PlotRequest(BaseModel):
    plot_type: str
    data: dict

class PriceAgePlotRequest(BaseModel):
    result: dict
    data: list

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

def create_html_form_pop(label, action, input_names):
    input_fields = ""
    for name in input_names:
        input_fields += f'<label for="{name}">{name.capitalize()}:</label>'
        input_fields += f'<input type="text" id="{name}" name="{name}">'
    form_html = f"""
    <h3>{label.split()[0]}</h3>
    <form action="{action}" method="get">
        {input_fields}
        <input type="submit" value="Submit">
    </form>
    """
    return form_html

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
        create_html_button("DISPLAY ALL", "/all"),
        create_html_button("Total Sales (Animate)", "/total_sales_animate"),
        create_html_button("Sales by Cities (Animate)", "/sales_by_cities_animate"),
        create_html_button("Total Sales to Foreigners (Animate)", "/total_sales_to_foreigners_animate"),
    ]
    forms = [
        create_html_form("Total Sales (start_year end_year)", "/total_sales", "interval"),
        create_html_form("Total Sales Yearly (city_code)", "/total_sales_yearly", "city_code"),
        create_html_form("Total Sales Monthly (city_code)", "/total_sales_monthly", "city_code"),
        create_html_form("Total Sales Monthly Foreigners (city_code)", "/total_sales_monthly_foreigners", "city_code"),
        create_html_form_pop("Population (city_code, town_code, quarter_code)", "/population_mah_plot", ["city_code", "town_code", "quarter_code"])
    ]
    return HTMLResponse(content=html_content.format(buttons=" ".join(buttons), forms=" ".join(forms)))



@app.get("/total_sales")
async def get_total_sales(interval: str = Query(None, title="Interval", description="Write the interval (ex: 2015 2021)")):
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
async def get_total_sales_yearly(city_code: int = Query(0, title="City Code", description="Enter the city code (ex: Ankara is 6)")):
    fig = total_sales_yearly_plot(df_totals_cities, city_code)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")

@app.get("/total_sales_monthly/")
async def get_total_sales_monthly(city_code: int = Query(0, title="City Code", description="Enter the city code (ex: Ankara is 6)")):
    fig = total_sales_monthly_plot(df_granular_cities, city_code)
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
async def get_total_sales_monthly_foreigners(city_code: int = Query(0, title="City Code", description="Enter the city code (ex: Ankara is 6)")):
    try:
        fig = total_sales_monthly_foreigners_plot(df_f_cities_aggregated, city_code)
        graph_html = pio.to_html(fig, full_html=False)
        return HTMLResponse(content=f"{graph_html}")
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the plot.")


# how to get more than parameters
@app.get("/population_mah_plot")
async def get_population_mah_plot(city_code: int = Query(0, title="City Code", description="Code of the city"),
                                  town_code: int = Query(0, title="Town Code", description="Code of the town"),
                                  quarter_code: int = Query(0, title="Quarter code", description="Code of the quarter")):
    fig = population_mah_plot(df_p, city_code, town_code, quarter_code)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"{graph_html}")


@app.get("/population_map") # with gender
async def get_population_map():
    pass

@app.post("/price_age_plot", response_class=HTMLResponse)
async def get_price_age_plot(plot_request: PriceAgePlotRequest):
    try:
        fig_price, fig_age = price_age_plot(plot_request.result, plot_request.data)
        price_html = pio.to_html(fig_price, full_html=False)
        age_html = pio.to_html(fig_age, full_html=False)
        return HTMLResponse(content=f"{price_html}{age_html}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating plots: {str(e)}")


@app.get("/all") # with gender
async def display_all():
    return HTMLResponse(content=f"""
        {pio.to_html(total_sales_animate(df_granular), full_html=False)}<br>
        {pio.to_html(total_sales_plot(df_granular), full_html=False)}<br>
        {pio.to_html(total_sales_yearly_plot(df_totals_cities), full_html=False)}<br>
        {pio.to_html(total_sales_monthly_plot(df_granular_cities), full_html=False)}<br>
        {pio.to_html(total_sales_foreigners_animate(df_f_total_aggregated), full_html=False)}<br>
        {pio.to_html(total_sales_foreigners_plot(df_f_total_aggregated), full_html=False)}<br>
        {pio.to_html(total_sales_monthly_foreigners_plot(df_f_cities_aggregated, city_code=0), full_html=False)}<br>
        il kayit no	ilçe kayit no	mahalle kayit no	erkek	kadin<br>
        81	957	51224	DÜZCE	KAYNAŞLI	KARAÇALI	1030	1054<br>
        {pio.to_html(population_mah_plot(df_p, city_code=81, town_code=957, quarter_code=51224, width=None, height=800), full_html=False)}<br>
        {pio.to_html(price_plot_demo()[0], full_html=False)}<br>
        {pio.to_html(price_plot_demo()[1], full_html=False)}<br>


        """
        )

# ------------------------------------------------------------------------------------------------
# Report

# TODO: population by age group
# TODO: population by gender
# TODO: population of foreigners
# TODO: population by marital status
# TODO: Yaş Grubu ve Cinsiyete Göre İl/İlçe Merkezi ve Belde / Köy Nüfusu
# TODO: Education Level

def price_plot_demo():
    import json
    # Read the JSON file (replace with your JSON file path)
    with open('./curl-res.json', 'r') as file:
        json_data = file.read()

    # Parse the JSON data
    m = json.loads(json_data)

    fig1, fig2 = price_age_plot(m["result"], m["data"])
    return fig1, fig2


if __name__ == "__main__":
    uvicorn.run(app, port=8000)