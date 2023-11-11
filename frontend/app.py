import requests
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import time

# Set up the page
st.set_page_config(page_title="Environmental and Forecasting Dashboard", layout="wide")

# Define custom styles for the containers
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply the custom styles defined in the 'style.css' file
local_css('style.css')

def fetch_sensor_data():
    current_unix_timestamp = int(time.time()) - 3600
    url = f"http://localhost:8000/get_sensor_data/?timestamp={current_unix_timestamp}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching sensor data: {e}")
        return pd.DataFrame()

def prediction_power():
    url = f"http://localhost:8000/get_prediction"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching sensor data: {e}")
        return pd.DataFrame()

# Sidebar for file upload
with st.sidebar:
    st.title("Data Upload")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            df_uploaded = pd.read_csv(uploaded_file)
            if df_uploaded.empty:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
            else:
                st.success("Successfully uploaded to database!")
                st.dataframe(df_uploaded)
        except pd.errors.EmptyDataError:
            st.error("The uploaded CSV file is empty or invalid.")
        except Exception as e:
            st.error(f"An error occurred while processing the file: {e}")

# Placeholder for sensor data
sensor_data_placeholder = st.empty()

while True:
    # Fetch and display sensor data
    sensor_data_df = fetch_sensor_data()
    prediction_power_df = prediction_power()

    with sensor_data_placeholder.container():
        if not sensor_data_df.empty:
            dates = sensor_data_df["timestamp"]
            temperature = sensor_data_df["temperature"]
            humidity = sensor_data_df["humidity"]
            co2_levels = sensor_data_df["co2"]
            air_quality = sensor_data_df["iaq"]
            power_consumption = np.random.normal(loc=40, scale=1, size=6)  # Simulate power consumption
            prediction_power_data = prediction_power_df["kwh"]
            np.random.seed(42)  # Set the seed value
            prediction_power_data = np.random.normal(loc=40, scale=5, size=7)  # Simulate power consumption
            power_consumption =  np.random.normal(loc=40, scale=5, size=7)
            weather_data =  np.random.normal(loc=13, scale=5, size=7)
            # # Define a color scale for air quality - green for high quality, red for low
            air_quality_color_scale = [
                (0.0, "red"),   # Air quality index 0
                (0.5, "yellow"), # Air quality index 50
                (1.0, "green"),  # Air quality index 100
            ]

            # Main container for Square Modules
            with st.container():
                st.subheader("Square Modules")
                # Create two sections within the Square Modules
                with st.container():
                    st.markdown('<div class="section-container">', unsafe_allow_html=True)
                    st.markdown("#### Square Lite – Office 1")
                    col1, col2 = st.columns(2)
                    
                    # Create a line chart for Temperature in Office 1
                    with col1:
                        fig1 = go.Figure()
                        fig1.add_trace(go.Scatter(x=dates, y=temperature, mode='lines+markers', name='Temperature',
                                                line=dict(shape='spline', smoothing=1.3, color='#1f77b4')))
                        fig1.update_layout(title='Temperature', xaxis_title='Date', yaxis_title='Temperature (°C)', template="plotly_white")
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    # Create a line chart for Humidity in Office 1
                    with col2:
                        fig2 = go.Figure()
                        fig2.add_trace(go.Scatter(x=dates, y=humidity, mode='lines+markers', name='Humidity',
                                                line=dict(shape='spline', smoothing=1.3, color='#ff7f0e')))
                        fig2.update_layout(title='Humidity', xaxis_title='Date', yaxis_title='Humidity (%)', template="plotly_white")
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    st.markdown('</div>', unsafe_allow_html=True)
            with st.container():
                st.markdown('<div class="section-container">', unsafe_allow_html=True)
                st.markdown("#### Square Pro – Office 2")
                col3, col4 = st.columns(2)
                
                # Create a line chart for CO2 Level in Office 2
                with col3:
                    fig3 = go.Figure()
                    fig3.add_trace(go.Scatter(x=dates, y=co2_levels, mode='lines+markers', name='CO2 Level',
                                            line=dict(shape='spline', smoothing=1.3, color='#2ca02c')))
                    fig3.update_layout(title='CO2 Level', xaxis_title='Date', yaxis_title='CO2 (PPM)', template="plotly_white")
                    st.plotly_chart(fig3, use_container_width=True)
                
                # Create a line chart for Air Quality in Office 2 with gradient color
                with col4:
                    fig4 = go.Figure(data=go.Scatter(
                        x=dates,
                        y=air_quality,
                        mode='lines+markers',
                        name='Air Quality',
                        marker=dict(
                            size=8,
                            color=air_quality,  # Set color equal to a variable
                            colorscale=air_quality_color_scale,  # Set the colorscale
                            colorbar=dict(title='Air Quality'),
                            showscale=True
                        ),
                        line=dict(shape='spline', smoothing=1.3)
                    ))
                    fig4.update_layout(title='Air Quality', xaxis_title='Date', yaxis_title='AQI', template="plotly_white")
                    st.plotly_chart(fig4, use_container_width=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
            # # Main container for Machine Learning Forecasting
            with st.container():
                st.subheader("Machine Learning Forecasting")
                col5, col6 = st.columns(2)
                
                # Create a line chart for Daily Power Consumption with Forecasting
                with col5:
                    fig5 = go.Figure()
                    # Actual Power Consumption
                    fig5.add_trace(go.Scatter(x=[1,2,3,4,5,6], y=prediction_power_data, mode='lines+markers', name='Actual',
                                            line=dict(color='blue')))
                    # Forecasted Power Consumption
                    fig5.add_trace(go.Scatter(x=[1,2,3,4,5,6], y=power_consumption , mode='lines', name='Forecast',
                                            line=dict(color='orange')))
                    fig5.update_layout(title='Daily Power Consumption Forecast', xaxis_title='Date', yaxis_title='Power (kW)', template="plotly_white")
                    st.plotly_chart(fig5, use_container_width=True)
                
                # Create a line chart for Weather Forecasting
                with col6:
                    fig6 = go.Figure()
                    fig6.add_trace(go.Scatter(x=[1,2,3,4,5,6], y=weather_data, mode='lines', name='Forecast',
                                            fill='tozeroy', line=dict(color='skyblue')))
                    fig6.update_layout(title='Weather Forecast', xaxis_title='Date', yaxis_title='Temperature (°C)', template="plotly_white")
                    st.plotly_chart(fig6, use_container_width=True)
                

        else:
            st.write("Waiting for sensor data...")


    # Wait for 5 seconds before the next update
    time.sleep(1)


