import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from time import sleep


@st.cache_data
def get_data(input_loc):
    url = f"http://api.weatherapi.com/v1/forecast.json?key=93366c8655fd4a248f0200040231101&q={input_loc}&days=3aqi=no&alerts=no"
    response = requests.get(url)
    response_data = response.json()
    return response_data


API_KEY = st.secrets["WEATHERAPI"]

st.set_page_config(
    page_title="Weather Forecasts",
    layout="wide"
)

st.markdown("# :cloud: Tom's :blue[Weather Forecasts] :sunny:")
st.markdown("---")
st.subheader("Enter three locations from anywhere in the world to receive their 3 day forecast")
col1, col2, col3 = st.columns(3)
with col1:
    location = st.text_input("Enter a location")
with col2:
    location2 = st.text_input("Enter a second location")
with col3:
    location3 = st.text_input("Enter a third location")

if location and location2 and location3:
    data = [get_data(location), get_data(location2), get_data(location3)]
    clean_data = []

    for locations in data:
        place = locations["location"]["name"]
        for weather in locations["forecast"]["forecastday"]:
            for hour in weather["hour"]:
                dict_temp = {
                    "location": place.title(),
                    "datetime": hour['time'],
                    "temperature": hour['temp_c'],
                    "text": hour['condition']['text'],
                    "chance_of_rain": hour['chance_of_rain'],
                    "chance_of_snow": hour['chance_of_snow']
                }
                clean_data.append(dict_temp)

    df = pd.DataFrame(clean_data)
    df["datetime"] = pd.to_datetime(df["datetime"])
    with st.spinner("Loading..."):
        sleep(1)
    st.markdown("---")
    selection = st.selectbox("What Datapoint Do You Want To Show?", ["Choose an Option...", "Temperature", "Chance of Rain", "Chance of Snow"])
    if selection == "Choose an Option...":
        st.stop()
    elif selection == 'Chance of Rain':
        figure = px.area(df,
                         x="datetime",
                         y=selection.replace(" ", "_").lower(),
                         color="location",
                         facet_col="location",
                         color_discrete_sequence=["#86BBD8", "#E65F5C", "#B5D99C"],
                         title="Forecasted Rainfall Over the Next 3 Days by Hour")
        figure.update_layout(showlegend=False)
        st.plotly_chart(figure, use_container_width=True)

    elif selection == 'Chance of Snow':
        figure = px.area(df,
                         x="datetime",
                         y=selection.replace(" ", "_").lower(),
                         color="location",
                         facet_col="location",
                         color_discrete_sequence=["#86BBD8", "#E65F5C", "#B5D99C"],
                         title="Forecasted Snowfall Over the Next 3 Days by Hour")
        figure.update_layout(showlegend=False)
        st.plotly_chart(figure, use_container_width=True)

    elif selection == 'Temperature':
        figure = px.area(df,
                         x="datetime",
                         y=selection.replace(" ", "_").lower(),
                         color="location",
                         facet_col="location",
                         color_discrete_sequence=["#86BBD8", "#E65F5C", "#B5D99C"],
                         title="Forecasted Temperature Over the Next 3 Days by Hour")
        figure.update_layout(showlegend=False)
        st.plotly_chart(figure, use_container_width=True)

    st.markdown("---")
    st.markdown("### :blue[Raw Data]")
    st.dataframe(df, use_container_width=True)
