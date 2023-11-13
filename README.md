# NOI-Hackathon-SFSCON-Edition
## NET-A-FOSS TEAM
![squarai-logo](assets/squarai-logo.png)
## Overview
This project is developed for the NOI Hackathon SFSCON Edition. It focuses on creating an ecosystem that collects data from various sensors located inside company offices, processes this data, and uses it to forecast power consumption. The primary aim is to increase user awareness about energy consumption and encourage efficient energy usage.

## Components

### 1. Sensor Data Collection
- **Devices**: The project uses squareAI devices, which are essentially Arduino-based sensors, to measure various environmental parameters.
- **Parameters Measured**: These devices collect data on air quality, temperature, CO2 levels, and power consumption.
- **Hub**: A Raspberry Pi hub aggregates data from all squareAI devices.

### 2. Data API (main.py)
- **Framework**: Developed using FastAPI.
- **Functionality**: This API is responsible for receiving data from the Raspberry Pi hub and storing it in a PostgreSQL database.
- **Database Integration**: The data is stored in a PostgreSQL database for further processing and analysis.

### 3. Data Processing and AI Model (PowerConsumptionPrediction.ipynb)
- **AI Model**: A machine learning model is trained using historical data and weather forecasts.
- **Objective**: The model aims to predict the power consumption of the offices.
- **Tools Used**: Jupyter Notebook is used for training and evaluating the model.

### 4. Weather Forecast Data
- **Integration**: Weather forecasting data is also stored in the PostgreSQL database.
- **Usage**: This data is used along with the sensor data to enhance the accuracy of the power consumption prediction model.

### 5. Orchestrator (orchestrator.py)
- **Role**: Manages the flow of data from the sensors to the API and ensures seamless data transmission and processing.

## Goals
- **Awareness**: Provide users with insights into their energy consumption patterns.
- **Energy Efficiency**: Encourage efficient use of heating and other energy resources in office environments.
