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

url = (f"http://api.weatherstack.com/current?access_key={api_key}&query={location}")
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

tab1, tab2, tab3 = st.tabs(["Events", "Weather", "Map"])

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
        if "planned_events" in file_data and len(file_data["planned_events"]) > 0:
            df = pd.DataFrame(file_data["planned_events"])
            st.dataframe(df)
        else:
            st.warning("No planned events found")


with tab2:
    st.subheader(f"Today's Weather in {location}")

    col1, col2 = st.columns([2,5])
    with col1:
        weather_desc = response["current"]["weather_descriptions"]
        st.write(f"The weather is: {weather_desc}")
        st.image(response["current"]["weather_icons"])

    with col2:
        def bar_chart(data):
            long_df = data.melt(var_name="Weather Condition", value_name="Value")
            fig = px.bar(long_df, x="Weather Condition", y="Value", title=f"Current Weather", color="Weather Condition")
            return fig

        data = pd.DataFrame({
            "Temperature": [float(response["current"]["temperature"])],
            "Humidity": [float(response["current"]["humidity"])],
            "Wind Speed": [float(response["current"]["wind_speed"])],
            "Wind Pressure": [float(response["current"]["pressure"])],
            "Cloud Cover": [float(response["current"]["cloudcover"])]
        })
        weather_chart = bar_chart(data)

        st.plotly_chart(weather_chart)


with tab3:
    st.subheader(f"Map of {location}")

    zoom_in = st.slider("Zoom in", min_value= 0, max_value=20, value=11)
    d = pd.DataFrame({
        'lat' : float(response["location"]["lat"]),
        'lon' : float(response["location"]["lon"]),
        'location' :[location],

    })
    location_map = px.scatter_map(
        data_frame= d,
        lat = "lat",
        lon = "lon",
        hover_name="location",
        zoom = zoom_in,
        map_style= "open-street-map"
    )
    st.plotly_chart(location_map)




