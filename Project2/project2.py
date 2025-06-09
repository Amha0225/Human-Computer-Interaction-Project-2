import streamlit as st
import pandas as pd
import requests
import dotenv
import os
import json
import plotly.express as px

st.title("Local Event Planner")

st.subheader("Ready to plan your events!")
location = st.text_input("Enter your location to begin")
st.info("Type a city name or ZIP code")

dotenv.load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

url = (f"http://api.weatherstack.com/forecast?access_key={api_key}&query={location}")
response = requests.get(url).json()

def write_json(events, new_data, filename = "json_files/planned_events.json"):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        file_data[events].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4, default=convert_dates)

def convert_dates(obj):
    if isinstance(obj, date):
        return obj.isoformat()
    raise TypeError("Object is not a date")

tab1, tab2, tab3 = st.tabs(["Events", "Weather Forecast", "Map"])

with tab1:
    st.subheader("Plan Events")

    name = st.text_input("Enter event name")
    date = st.date_input("Date of event")
    time = st.time_input("Time of event (In military time)")
    place = st.text_input("Where will the event occur?")

    submit = st.button("Submit")
    if submit:
        st.success("Submitted")
        event_info={
            "name": name,
            "date": str(date),
            "time": str(time),
            "place": place
        }
        write_json("planned_events", event_info)

    st.divider()
    st.subheader("Planned Events")

    with(open("json_files/planned_events.json", "r")) as read_file:
        file_data = json.load(read_file)
        if len(file_data["planned_events"]) > 0:
            idx = []
            for i in range (len(file_data["planned_events"])):
                idx.append(str(i))
                df = pd.DataFrame(file_data["planned_events"], index=idx)
                st.dataframe(df)


with tab2:
    st.subheader("Weather Forecast")
    forecast_days = st.slider("How many days you want to see?", min_value=1, max_value=14, step=1)

    hourly = st.checkbox("Would you forecast in hours?")
    if hourly:
        hours = st.selectbox("How many hours do you want to see?", options=[1, 3, 6, 12, 24])
        querystring = {"forecast_days": forecast_days,"hours": hours}
    else:
        querystring = {"forecast_days": forecast_days}

    response = requests.get(url, params=querystring)

    col1, col2 = st.columns([2,5])
    with col1:
        parameter = st.selectbox("Choose a parameter",options=[
            "Temperature",
            "Humidity",
            "Wind Speed",
            "Chance of Rain",
            "Chance of Snow"
        ])

    with col2:
        data = response.json()
        forecast = data.get("forecast", {})
        df_list = []

        for day_key in list(forecast.keys())[:forecast_days]:
            day_data = forecast[day_key]
            date = day_data.get("date", day_key)
            for hour_data in day_data.get("hourly", [])[:hours if hourly else 24]:
                df_list.append({
                    "Date": date,
                    "Time": hour_data.get("time"),
                    "Temperature": hour_data.get("temperature", None),
                    "Humidity": hour_data.get("humidity", None),
                    "Wind Speed": hour_data.get("wind_speed", None),
                    "Chance of Rain": hour_data.get("chanceofrain", None),
                    "Chance of Snow": hour_data.get("chanceofsnow", None)
                })

        df = pd.DataFrame(df_list)
        df["Time"] = df["Time"].astype(str).str.zfill(4)
        df["DateTime"] = pd.to_datetime(df["Date"] + " " + df["Time"],format="%Y-%m-%d %H%M",errors="coerce")
        df = df.dropna(subset=["DateTime", parameter])
        df = df.sort_values("DateTime")

        if not df.empty and "DateTime" in df.columns and parameter in df.columns:
            forecast_chart = st.line_chart(
                data = df,
                x= "DateTime",
                y= parameter
            )
        else:
            st.warning("No data found")
        st.plotly_chart(forecast_chart)


with tab3:
    st.subheader("Map")

    df = pd.DataFrame({
        'lat' : float(response["location"]["lat"]),
        'lon' : float(response["location"]["lon"]),
        'location' :[location]

    })
    location_map = px.scatter_mapbox(
        data_frame= df,
        lat = "lat",
        lon = "lon",
        hover_name="location",
        zoom = 11,
        mapbox_style= "open-street-map"
    )
    st.plotly_chart(location_map)




