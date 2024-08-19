"""
This is a FASTAPI application that provides endpoints for retrieving sales data, population data, and weather data in JSON format.
The JSON data is then converted to plots at the other end, which is the back-end for the web application.
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import uvicorn
from pydantic import BaseModel
import plotly.io as pio
from scripts_dir.prep_data import *
from scripts_dir.plot import *
import json

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to allow specific methods
    allow_headers=["*"],  # Adjust this to allow specific headers
)

# These are for caching
df_totals_total, df_totals_cities, df_granular, df_granular_cities = sales_cities_df()
df_f_total_aggregated, df_f_cities_aggregated = sales_cities_foreigners_df()
df_p = population_df()
dfs_p_marital = population_marital_df()
df_trend = population_trend_df()
df_election = election_df()
df_origin_city = population_origin_city_df()
df_weather = weather_df()

plots = {}


class PlotRequest(BaseModel):
    plot_type: str
    data: dict


class PriceAgePlotRequest(BaseModel):
    result: dict
    data: list


def create_html_button(label, link):
    return f"<button onclick=\"window.location.href='{link}'\">{label}</button>"


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


# To create and cache plots
@app.on_event("startup")
async def startup():
    global plots
    plots["total_sales"] = pio.to_json(
        total_sales_plot(df_granular),
        engine="json",
    )
    plots["total_sales_animate"] = pio.to_json(
        total_sales_animate(df_granular),
        engine="json",
    )
    plots["total_sales_animate"] = pio.to_json(
        total_sales_animate(df_granular),
        engine="json",
    )

    plots["total_sales_foreigners_animate"] = pio.to_json(
        total_sales_foreigners_animate(df_f_total_aggregated),
        engine="json",
    )

    # total_sales_montly (per city)
    # total_sales_montly_foreigners (per city)
    # population_origin_city_plot (per city)
    # population_marital_plot (per city)
    # population_trend_plot (per city)

    plots["total_sales_monthly"] = []
    for i in range(0, 82):
        plots["total_sales_monthly"].append(
            pio.to_json(
                total_sales_monthly_plot(df_granular_cities, city_code=i), engine="json"
            )
        )

    plots["total_sales_monthly_foreigners"] = []
    for i in range(0, 82):
        plots["total_sales_monthly_foreigners"].append(
            pio.to_json(
                total_sales_monthly_foreigners_plot(
                    df_f_cities_aggregated, city_code=i
                ),
                engine="json",
            )
        )
    plots["population_origin_city_plot"] = []
    for i in range(0, 82):
        plots["population_origin_city_plot"].append(
            pio.to_json(
                population_origin_city_plot(df_origin_city, city_code=i), engine="json"
            )
        )
    plots["population_marital_plot"] = []
    for i in range(0, 82):
        plots["population_marital_plot"].append(
            pio.to_json(
                population_marital_plot(*dfs_p_marital, city_code=i), engine="json"
            )
        )
    plots["population_trend_plot"] = []
    for i in range(0, 82):
        plots["population_trend_plot"].append(
            pio.to_json(population_trend_plot(df_trend, city_code=i), engine="json")
        )


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
        create_html_button(
            "Total Sales to Foreigners (Animate)", "/total_sales_to_foreigners_animate"
        ),
    ]
    forms = [
        create_html_form(
            "Total Sales (start_year end_year)", "/total_sales", "interval"
        ),
        create_html_form(
            "Total Sales Yearly (city_code)", "/total_sales_yearly", "city_code"
        ),
        create_html_form(
            "Total Sales Monthly (city_code)", "/total_sales_monthly", "city_code"
        ),
        create_html_form(
            "Total Sales Monthly Foreigners (city_code)",
            "/total_sales_monthly_foreigners",
            "city_code",
        ),
        create_html_form_pop(
            "Population (city_code, town_code, quarter_code)",
            "/population_mah_plot",
            ["city_code", "town_code", "quarter_code"],
        ),
    ]
    return HTMLResponse(
        content=html_content.format(buttons=" ".join(buttons), forms=" ".join(forms))
    )


@app.get("/total_sales", response_class=JSONResponse)
async def get_total_sales(
    # interval: str = Query(None, title="Interval", description="Write the interval (ex: 2015 2021)"),
    # height: int = Query(800, description="height of the plot"),
):
    try:
        return JSONResponse(content=plots["total_sales"])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the total_sales plot.",
        )


@app.get("/total_sales_animate", response_class=JSONResponse)
async def get_total_sales_animate():
    try:
        return JSONResponse(content=plots["total_sales_animate"])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the total_sales_animate plot.",
        )


@app.get("/total_sales_yearly/", response_class=JSONResponse)
async def get_total_sales_yearly(
    city_code: int = Query(
        0, title="City Code", description="Enter the city code (ex: Ankara is 6)"
    )
):
    try:
        fig = total_sales_yearly_plot(df_totals_cities, city_code)
        graph_html = pio.to_json(fig)
        return JSONResponse(content=graph_html)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the total_sales_yearly plot.",
        )


@app.get("/total_sales_monthly/", response_class=JSONResponse)
async def get_total_sales_monthly(
    city_code: int = Query(
        0, title="City Code", description="Enter the city code (ex: Ankara is 6)"
    )
):
    try:
        return JSONResponse(content=plots["total_sales_monthly"][city_code])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the total_sales_monthly plot.",
        )


@app.get("/total_sales_to_foreigners_animate", response_class=JSONResponse)
async def get_total_sales_to_foreigners_animate():
    try:
        return JSONResponse(content=plots["total_sales_foreigners_animate"])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the total_sales_to_foreigners_animate plot.",
        )


@app.get("/total_sales_monthly_foreigners/", response_class=JSONResponse)
async def get_total_sales_monthly_foreigners(
    city_code: int = Query(
        0, title="City Code", description="Enter the city code (ex: Ankara is 6)"
    )
):
    try:
        return JSONResponse(content=plots["total_sales_monthly_foreigners"][city_code])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the total_sales_monthly_foreigners plot.",
        )


# how to get more than parameters
@app.get("/population_mah_plot", response_class=JSONResponse)
async def get_population_mah_plot(
    city_code: int = Query(0, title="City Code", description="Code of the city"),
    town_code: int = Query(0, title="Town Code", description="Code of the town"),
    quarter_code: int = Query(
        0, title="Quarter code", description="Code of the quarter"
    ),
):
    try:
        fig = population_mah_plot(df_p, city_code, town_code, quarter_code)
        graph_html = pio.to_json(fig)
        return JSONResponse(content=graph_html)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the population_mah_plot plot.",
        )


@app.get("/population_marital_status_plot", response_class=JSONResponse)
async def get_population_marital_plot(
    city_code: int = Query(1, title="City Code", description="Code of the city"),
):
    try:
        return JSONResponse(content=plots["population_marital_plot"][city_code])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the population_marital_status_plot plot.",
        )


@app.get("/population_origin_city_plot", response_class=JSONResponse)
async def get_population_origin_city_plot(
    city_code: int = Query(1, title="City Code", description="Code of the city"),
    height: int = Query(
        800, title="Plot Height in Px", description="Height of the plot"
    ),
):
    try:
        return JSONResponse(content=plots["population_origin_city_plot"][city_code])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the population_origin_city_plot plot.",
        )


@app.get("/population_trend_plot", response_class=JSONResponse)
async def get_population_trend_plot(
    city_code: int = Query(1, title="City Code", description="Code of the city"),
    height: int = Query(
        800, title="Plot Height in Px", description="Height of the plot"
    ),
):
    try:
        return JSONResponse(content=plots["population_trend_plot"][city_code])
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the population_trend_plot plot.",
        )


@app.get("/population_election_plot", response_class=JSONResponse)
async def get_population_election_plot(
    city_code: int = Query(1, title="City Code", description="Code of the city"),
    district_code: int = Query(None, title="City Code", description="Code of the city"),
    height: int = Query(
        800, title="Plot Height in Px", description="Height of the plot"
    ),
):
    try:
        fig = population_election_plot(
            df_election, city_code, district_code=district_code, height=height
        )
        graph_html = pio.to_json(fig)
        return JSONResponse(content=graph_html)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the population_election_plot plot.",
        )


@app.get("/weather_plot", response_class=JSONResponse)
async def get_weather_plot(
    city_code: int = Query(1, title="City Code", description="Code of the city"),
):
    try:
        fig = weather_plot(
            df_election, city_code, district_code=district_code, height=height
        )
        graph_html = pio.to_json(fig)
        return JSONResponse(content=graph_html)
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while generating the weather_plot plot.",
        )


@app.post("/price_age_plot", response_class=JSONResponse)
async def get_price_age_plot(plot_request: PriceAgePlotRequest):
    try:
        fig_price, fig_age = price_age_plot(plot_request.result, plot_request.data)
        price_html = pio.to_json(fig_price)
        age_html = pio.to_json(fig_age)
        return JSONResponse(content={"price_plot": price_html, "age_plot": age_html})
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating price_age_plot plots: {str(e)}"
        )


@app.get("/all")  # with gender
async def display_all():
    return HTMLResponse(
        content=f"""
        <script charset="utf-8" src="https://cdn.plot.ly/plotly-2.32.0.min.js"></script> 
        {plots['total_sales_foreigners_animate']}<br>
        {plots['total_sales']}<br>
        {plots['total_sales_animate']}<br>
        {plots['total_sales_monthly'][1]}<br>
        {plots['total_sales_monthly_foreigners'][1]}<br>
        {plots['population_marital_plot'][1]}<br>
        {plots['population_origin_city_plot'][1]}<br>
        {plots['population_trend_plot'][1]}<br>
        il kayit no	    ilçe kayit no	mahalle kayit no	il adı  ilçe adı    mahalle adı erkek	kadin<br>
        81	            957	            51224	            DÜZCE	KAYNAŞLI	KARAÇALI	1030	1054<br>
        {pio.to_html(population_mah_plot(df_p, city_code=81, town_code=957, quarter_code=51224, width=None, height=800), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(price_plot_demo()[0], full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(population_election_plot(df_election, city_code=1), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(price_plot_demo()[1], full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_json(price_plot_demo()[1])}<br>

        """
    )
    return HTMLResponse(
        content=f"""
        {pio.to_json(total_sales_animate(df_granular), full_html=False, include_plotlyjs="cdn", include_mathjax=False)}<br>
        {pio.to_html(total_sales_plot(df_granular), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(total_sales_yearly_plot(df_totals_cities), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(total_sales_monthly_plot(df_granular_cities), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(total_sales_foreigners_animate(df_f_total_aggregated), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(total_sales_foreigners_plot(df_f_total_aggregated), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(total_sales_monthly_foreigners_plot(df_f_cities_aggregated, city_code=0), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        il kayit no	    ilçe kayit no	mahalle kayit no	il adı  ilçe adı    mahalle adı erkek	kadin<br>
        81	            957	            51224	            DÜZCE	KAYNAŞLI	KARAÇALI	1030	1054<br>
        {pio.to_html(population_mah_plot(df_p, city_code=81, town_code=957, quarter_code=51224, width=None, height=800), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(price_plot_demo()[0], full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(price_plot_demo()[1], full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(population_marital_plot(*dfs_p_marital, city_code=1), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(population_origin_city_plot(df_origin_city, city_code=1), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(population_election_plot(df_election, city_code=1), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>
        {pio.to_html(population_trend_plot(df_trend, city_code=1), full_html=False, include_plotlyjs=False, include_mathjax=False)}<br>


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
    with open("./curl-res.json", "r") as file:
        json_data = file.read()

    # Parse the JSON data
    m = json.loads(json_data)

    fig1, fig2 = price_age_plot(m["result"], m["data"])
    return fig1, fig2


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
