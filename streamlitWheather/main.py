import streamlit as st
import requests
import sqlite3
from datetime import datetime

# Assessment 1: Weather App with Current and 12-Hour Forecast
# ----------------------------------------------------------
# OpenWeatherMap API details
API_KEY = "YOUR_API_KEY"
BASE_URL_CURRENT = "https://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
st.markdown("#### Created by Hirah Mohammadi Afroze")
# App header
st.title("🌦️ Weather App")
st.write("Enter a city to get the current weather and next 12-hour forecast.")

# Input for city name
city_name = st.text_input("Enter City Name", "")

if city_name:
    # Fetch current weather
    def get_current_weather(city):
        url = f"{BASE_URL_CURRENT}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, response.json().get("message", "Error fetching current weather.")

    # Fetch 5-day/3-hour forecast
    def get_forecast(city):
        url = f"{BASE_URL_FORECAST}?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json(), None
        else:
            return None, response.json().get("message", "Error fetching forecast.")

    # Get weather data
    current_weather, current_error = get_current_weather(city_name)
    forecast_data, forecast_error = get_forecast(city_name)

    # Display current weather
    if current_weather:
        st.subheader(f"🌍 Weather in {city_name.title()}")
        st.write(f"**Temperature:** {current_weather['main']['temp']}°C")
        st.write(f"**Description:** {current_weather['weather'][0]['description'].capitalize()}")
        st.write(f"**Humidity:** {current_weather['main']['humidity']}%")
        st.write(f"**Wind Speed:** {current_weather['wind']['speed']} m/s")
    else:
        st.error(f"Error fetching current weather: {current_error}")

    # Display next 12-hour forecast
    if forecast_data:
        st.subheader(f"🔮 Next 12-Hour Forecast for {city_name.title()}")
        hourly_forecast = forecast_data["list"][:4]  # Next 12 hours = 4 intervals (3-hour steps)
        for forecast in hourly_forecast:
            time = forecast["dt_txt"]
            temp = forecast["main"]["temp"]
            description = forecast["weather"][0]["description"].capitalize()
            st.write(f"**{time}:** {temp}°C, {description}")
    else:
        st.error(f"Error fetching forecast: {forecast_error}")

# Assessment 2: Weather App with Database Integration
# ---------------------------------------------------
# Initialize SQLite Database
DB_NAME = "weather.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS weather (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT NOT NULL,
                        date_range TEXT NOT NULL,
                        weather_data TEXT
                    )''')
    conn.commit()
    conn.close()

def add_record(location, date_range, weather_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO weather (location, date_range, weather_data) VALUES (?, ?, ?)",
                   (location, date_range, weather_data))
    conn.commit()
    conn.close()

def get_records():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weather")
    records = cursor.fetchall()
    conn.close()
    return records

def update_record(record_id, location, date_range):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE weather SET location = ?, date_range = ? WHERE id = ?",
                   (location, date_range, record_id))
    conn.commit()
    conn.close()

def delete_record(record_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM weather WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()



# Info Section
st.sidebar.info("**PM Accelerator**\nThis weather app is created as part of a technical assessment for the PM Accelerator program.\n\n[Learn more about PM Accelerator on LinkedIn](https://www.linkedin.com/company/product-manager-accelerator/)")

# Initialize Database
init_db()

# Tabs for functionality
tabs = st.tabs(["Add Record", "View Records", "Update Record", "Delete Record"])

# Tab 1: Add Record
def fetch_weather(location):
    params = {"q": location, "appid": API_KEY, "units": "metric"}
    response = requests.get(BASE_URL_CURRENT, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

with tabs[0]:
    st.header("Add a Weather Record")
    location = st.text_input("Enter Location:")
    start_date = st.date_input("Start Date:", min_value=datetime.today())
    end_date = st.date_input("End Date:", min_value=start_date)

    if st.button("Add Record"):
        if location:
            weather_data = fetch_weather(location)
            if weather_data:
                date_range = f"{start_date} to {end_date}"
                weather_description = weather_data['weather'][0]['description']
                temp = weather_data['main']['temp']
                formatted_weather = f"{weather_description}, {temp}°C"
                add_record(location, date_range, formatted_weather)
                st.success("Record added successfully!")
            else:
                st.error("Could not fetch weather data. Please check the location.")
        else:
            st.error("Location is required.")

# Tab 2: View Records
with tabs[1]:
    st.header("View All Records")
    records = get_records()
    if records:
        for record in records:
            st.write(f"ID: {record[0]} | Location: {record[1]} | Date Range: {record[2]} | Weather Data: {record[3]}")
    else:
        st.info("No records found.")

# Tab 3: Update Record
with tabs[2]:
    st.header("Update a Record")
    record_id = st.number_input("Enter Record ID to Update:", min_value=1, step=1)
    new_location = st.text_input("New Location:")
    new_start_date = st.date_input("New Start Date:", min_value=datetime.today())
    new_end_date = st.date_input("New End Date:", min_value=new_start_date)

    if st.button("Update Record"):
        if new_location:
            new_date_range = f"{new_start_date} to {new_end_date}"
            update_record(record_id, new_location, new_date_range)
            st.success("Record updated successfully!")
        else:
            st.error("Location is required.")

# Tab 4: Delete Record
with tabs[3]:
    st.header("Delete a Record")
    record_id_to_delete = st.number_input("Enter Record ID to Delete:", min_value=1, step=1)

    if st.button("Delete Record"):
        delete_record(record_id_to_delete)
        st.success("Record deleted successfully!")
