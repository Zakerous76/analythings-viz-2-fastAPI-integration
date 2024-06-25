from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn
from prep_data import sales_by_cities
from plot import animate
import plotly.io as pio
import plotly.graph_objs as go

app = FastAPI()
df_totals_total, df_totals_cities, df_totals_total_granular = sales_by_cities() 

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

# TODO: Fix this
@app.get("/total_sales")
async def get_total_sales():
    fig = go.Figure(data=go.Bar(x=df_totals_total['Yıl/Ay'], y=df_totals_total['Total']))
    fig.update_layout(title="Total Sales by Year/Month", xaxis_title="Year/Month", yaxis_title="Total Sales")
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")


@app.get("/total_sales_animate")
async def get_total_sales_animate():
    fig = animate(df_totals_total_granular)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

# TODO: Fix this
@app.get("/sales_by_cities")
async def get_sales_by_cities():
    fig = go.Figure(data=[go.Bar(name=city, x=df_totals_total['Yıl/Ay'], y=df_totals_cities[city]) for city in df_totals_cities.columns])
    fig.update_layout(title="Sales by Cities", xaxis_title="Year/Month", yaxis_title="Total Sales", barmode='stack')
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

# TODO: Fix this
@app.get("/sales_by_cities_animate")
async def get_sales_by_cities_animate():
    fig = animate(df_totals_total_granular)
    graph_html = pio.to_html(fig, full_html=False)
    return HTMLResponse(content=f"<html><body>{graph_html}</body></html>")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)