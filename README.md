# Weather App Project  

## Screenshots  
![App Screenshot](images/ss.jpg)  
## Overview  
This project is a Weather App built using **Streamlit** that allows users to:  
- Fetch current weather details and a 12-hour forecast for any city using the **OpenWeatherMap API**.  
- Perform CRUD (Create, Read, Update, Delete) operations on weather records stored in an **SQLite database**.  

The project consists of two main components:  
1. **Assessment 1: Weather App**  
   - Fetches and displays:  
     - Current weather details (temperature, description, humidity, and wind speed).  
     - A 12-hour forecast split into 3-hour intervals.  
   - Real-time data is fetched using the **OpenWeatherMap API**.  

2. **Assessment 2: Weather App with Database Integration**  
   - Provides a tabbed interface to:  
     - Add weather records to an SQLite database.  
     - View, update, or delete saved records.  

---

## Features  

### Current Weather and Forecast  
- Input a city name to fetch real-time weather data.  
- Displays:  
  - Temperature  
  - Weather conditions  
  - Humidity and wind speed  
  - 12-hour forecast in 3-hour intervals  

### Database Integration  
- Add weather data along with a date range to the database.  
- View all stored records with detailed information.  
- Update or delete existing records directly through the app.  

### Streamlit UI  
- Clean and intuitive interface.  
- Sidebar with relevant information and inputs.  
- Tabbed interface for database operations.  

---

## Tech Stack  
- **Frontend**: Streamlit  
- **Backend**: Python  
- **Database**: SQLite  
- **API**: OpenWeatherMap  

---

## How to Run  

1. Clone this repository:  
   ```bash
   git clone <repository_url>
2. streamlit run app.py
   ```bash
   streamlit run app.py

