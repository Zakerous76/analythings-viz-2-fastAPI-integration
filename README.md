
# 🏠 Real Estate Dashboard Plot API (FastAPI + Plotly)

This project is a **FastAPI web application** that provides **interactive Plotly charts** for real estate sales, population statistics, and weather data.
All charts are served as **self-contained HTML**, allowing them to be viewed directly in the browser without any additional frontend setup.
Optionally, the application can be easily adapted to serve **JSON data** for integration with custom frontend frameworks or dashboards.

---

![project-9](https://github.com/user-attachments/assets/f4144d0e-2758-453d-8965-bc87f0a3fc57)


## ✨ Features

* 📊 **Real Estate Sales**

  * Total sales over time
  * Sales animations
  * Sales by city (monthly & yearly)
  * Sales to foreigners

* 👥 **Population Insights**

  * Population by neighborhood (mahalle)
  * Marital status
  * Origin city distributions
  * Trends over time
  * Election results (population by vote data)

* 🌦️ **Weather Data**

  * City-level weather plots

* 💰🏗️ **Price vs Age Plots**

  * Compare housing prices and building ages

* 🖥️ **Web Dashboard**

  * A main page (`/`) with buttons & forms so users can try plots directly

---

## ⚡ Tech Stack

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge\&logo=python\&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge\&logo=plotly\&logoColor=white)](https://plotly.com/python/)
[![Uvicorn](https://img.shields.io/badge/Uvicorn-262261?style=for-the-badge\&logo=uvicorn\&logoColor=white)](https://www.uvicorn.org/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge\&logo=pandas\&logoColor=white)](https://pandas.pydata.org/)
[![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge\&logo=numpy\&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-8CA0D7?style=for-the-badge&logo=scipy&logoColor=white)](https://www.scipy.org/)  
[![Requests](https://img.shields.io/badge/Requests-008ABC?style=for-the-badge&logo=requests&logoColor=white)](https://docs.python-requests.org/)  
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-FF9900?style=for-the-badge&logo=beautifulsoup&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/)



## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Zakerous76/analythings-viz-2-fastAPI-integration.git
cd analythings-viz-2-fastAPI-integration
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
uvicorn app:app --reload --port 8000
```

### 5. Open in browser

Go to:
👉 [http://localhost:8000/](http://localhost:8000/)

---

## 🔗 Endpoints Overview

### Main Page

* `/` — Dashboard homepage with buttons & forms

### Sales

* `/total_sales`
* `/total_sales_animate`
* `/total_sales_yearly?city_code=6`
* `/total_sales_monthly?city_code=6`
* `/total_sales_monthly_foreigners?city_code=6`
* `/total_sales_to_foreigners_animate`

### Population

* `/population_mah_plot?city_code=1&town_code=1&quarter_code=1`
* `/population_marital_status_plot?city_code=1`
* `/population_origin_city_plot?city_code=1`
* `/population_trend_plot?city_code=1`
* `/population_election_plot?city_code=1&district_code=2`

### Weather

* `/weather_plot?city_code=1`

### Price vs Age (POST)

* `/price_age_plot` — accepts JSON body with `result` and `data`

---

## 🛠️ Development Notes

* All plots are generated with `plotly.io.to_html()` → no frontend Plotly setup required
* Query parameters allow dynamic filtering (e.g., city codes, district codes, etc.)
* Add your datasets in `scripts_dir/prep_data.py`

---

## 📜 License

MIT License. Feel free to use and adapt.


