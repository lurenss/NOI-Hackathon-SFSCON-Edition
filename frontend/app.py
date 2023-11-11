import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd

# Set up the page
st.set_page_config(page_title="Environmental and Forecasting Dashboard", layout="wide")

# Define custom styles for the containers
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Apply the custom styles defined in the 'style.css' file
local_css('style.css')

# Sidebar for file upload
with st.sidebar:
    st.title("Data Upload")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            # Try to read the CSV file
            df_uploaded = pd.read_csv(uploaded_file)
            # Check if the dataframe is empty
            if df_uploaded.empty:
                st.error("The uploaded file is empty. Please upload a valid CSV file.")
            else:
                # If the file is read successfully and is not empty, show the data
                st.success("Successfully uploaded to database!")
                st.dataframe(df_uploaded)
        except pd.errors.EmptyDataError:
            # Handle the case where the CSV is empty or has no columns
            st.error("The uploaded CSV file is empty or invalid.")
        except Exception as e:
            # Handle any other exceptions
            st.error("An error occurred while processing the file.")

# Generate placeholder data
dates = pd.date_range(start="2023-01-01", periods=30, freq="D")
temperature = np.random.normal(loc=20, scale=3, size=len(dates))  # Simulate temperature data
humidity = np.random.uniform(low=30, high=70, size=len(dates))  # Simulate humidity data
co2_levels = np.random.uniform(low=350, high=450, size=len(dates))  # Simulate CO2 levels
air_quality = np.random.uniform(low=0, high=100, size=len(dates))  # Simulate air quality index
power_consumption = np.random.normal(loc=500, scale=50, size=len(dates))  # Simulate power consumption
weather_forecast = np.random.uniform(low=10, high=30, size=len(dates))  # Simulate weather temperatures

# Define a color scale for air quality - green for high quality, red for low
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

# Main container for Machine Learning Forecasting
with st.container():
    st.subheader("Machine Learning Forecasting")
    col5, col6 = st.columns(2)
    
    # Create a line chart for Daily Power Consumption with Forecasting
    with col5:
        fig5 = go.Figure()
        # Actual Power Consumption
        fig5.add_trace(go.Scatter(x=dates, y=power_consumption, mode='lines+markers', name='Actual',
                                  line=dict(color='blue')))
        # Forecasted Power Consumption
        fig5.add_trace(go.Scatter(x=dates, y=power_consumption + np.random.normal(scale=20, size=len(dates)), mode='lines', name='Forecast',
                                  line=dict(color='orange')))
        fig5.update_layout(title='Daily Power Consumption Forecast', xaxis_title='Date', yaxis_title='Power (kW)', template="plotly_white")
        st.plotly_chart(fig5, use_container_width=True)
    
    # Create a line chart for Weather Forecasting
    with col6:
        fig6 = go.Figure()
        fig6.add_trace(go.Scatter(x=dates, y=weather_forecast, mode='lines', name='Forecast',
                                  fill='tozeroy', line=dict(color='skyblue')))
        fig6.update_layout(title='Weather Forecast', xaxis_title='Date', yaxis_title='Temperature (°C)', template="plotly_white")
        st.plotly_chart(fig6, use_container_width=True)
