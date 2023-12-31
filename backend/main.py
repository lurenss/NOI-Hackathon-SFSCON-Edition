"""
This module contains a FastAPI application that queries data from InfluxDB.
"""

from fastapi import FastAPI
import aiohttp
from aiohttp import ClientSession
import pandas as pd

from decouple import config
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS

from collections import defaultdict

from sqlalchemy import create_engine, Table, MetaData, Column, Integer, Float, String, insert

# Define metadata
metadata = MetaData()

# Define table (make sure this matches your actual DB schema)
sensor_data_table = Table('sensor_data', metadata,
    Column('timestamp', Integer, primary_key=True),
    Column('temperature', Float),
    Column('humidity', Float),
    Column('iaq', Float),
    Column('co2', Integer),
    Column('gas', Integer),
    Column('battery', Integer),
)



FLUXDB_URL = config("INFLUXDB_URL")
ORG = config("INFLUXDB_ORG")
BUCKET = config("INFLUXDB_BUCKET")
TOKEN = config("INFLUXDB_TOKEN")

app = FastAPI()

client = influxdb_client.InfluxDBClient(
url=FLUXDB_URL,
token=TOKEN,
org=ORG
)

query_api = client.query_api()

# create a connection to a local host postgresql database
# PostgreSQL Database connection string
postgres_connection_string = f"postgresql://{config('POSTGRES_USER')}:{config('POSTGRES_PASSWORD')}@localhost/{config('POSTGRES_DB')}"

# Create an SQLAlchemy engine
engine = create_engine(postgres_connection_string)


@app.get("/")
def read_root():
    """
    Root endpoint that returns a simple greeting message for TESTING purposes.
    """
    return {"Hello": "World"}

@app.get("/fetch_data_and_store")
async def query_fluxdb():
    """
    Queries FluxDB for sensor data and stores it in a PostgreSQL database.
    The function retrieves data from the FluxDB database, parses it, and stores it in a PostgreSQL database.
    The data is filtered by the fields temperature, humidity, iaq, co2, gas, and battery.
    The function returns a message indicating whether the data was successfully fetched and stored in the database.
    """
    print("Querying FluxDB...")

    query = 'from(bucket:"{}")\
    |> range(start: -10s)\
    |> filter(fn:(r) => r._measurement == "movement_sensor_data")\
    |> filter(fn:(r) => r._field == "temperature" or r._field == "humidity" or r._field == "iaq" or r._field == "co2" or r._field == "gas" or r._field == "battery")\
    |> keep(columns: ["_time", "_field", "_value"])'.format(BUCKET)
    
    print(query)
    
    result = query_api.query(org=ORG, query=query)
    #print("Result: {0}".format(result))

    # parse results
    paired_results = defaultdict(lambda: {'temperature': None, 'humidity': None, 'iaq': None, 'co2': None, 'gas': None, 'battery': None})
    for table in result:
        for record in table.records:
            time = record.get_time()
            if record.get_field() == 'temperature':
                paired_results[time]['temperature'] = record.get_value()
            elif record.get_field() == 'humidity':
                paired_results[time]['humidity'] = record.get_value()
            elif record.get_field() == 'iaq':
                paired_results[time]['iaq'] = record.get_value()
            elif record.get_field() == 'co2':
                paired_results[time]['co2'] = record.get_value()
            elif record.get_field() == 'gas':
                paired_results[time]['gas'] = record.get_value()
            elif record.get_field() == 'battery':
                paired_results[time]['battery'] = record.get_value()

    # Convert to desired format
    pre_df = []
    for time, values in paired_results.items():
        unix_time = int(time.timestamp())
        pre_df.append((unix_time, values['temperature'], values['humidity'], values['iaq'], values['co2'], values['gas'], values['battery']))
    
    df = pd.DataFrame(pre_df, columns=['timestamp', 'temperature', 'humidity', 'iaq', 'co2', 'gas', 'battery'])
    
    # make distinct on timestamp
    df = df.drop_duplicates(subset=['timestamp'])


    print(df.head())


    # Prepare the raw SQL for insertion 2with ON CONFLICT clause
    insert_sql = """
    INSERT INTO sensor_data (timestamp, temperature, humidity, iaq, co2, gas, battery)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (timestamp) DO NOTHING;
    """

    try:
        # Execute the SQL statement
        with engine.connect() as conn:
            for row in df.itertuples(index=False):
                conn.execute(insert_sql, row)
        print("Data inserted successfully")
        # close the connection
        conn.close()
        return {"message": "Data fetched and stored in the database."}
    except Exception as e:
        print(f"An error occurred while inserting data into the database: {e}")

    return {"message": "Data fetched and stored in the database."}

# get sensor data from  sensor_data tables in postgresdb and takes as input  from which timestamp to start
@app.get("/get_sensor_data")
def query_sensor_data_postgres(timestamp: int):
    """
    Queries the PostgreSQL database for sensor data.
    The function retrieves data from the PostgreSQL database and returns it as a JSON object.
    The data is filtered by the fields temperature, humidity, iaq, co2, gas, and battery.
    The function returns a JSON object containing the sensor data.
    """
    print("Querying PostgreSQL database...")
    # create a database connection
    conn = engine.connect()
    # create a SELECT statement
    select_sql = """
    SELECT * FROM sensor_data
    WHERE timestamp >= %s
    ORDER BY timestamp ASC
    """
    # execute the SELECT statement
    rs = conn.execute(select_sql, timestamp)
    # return all results as a JSON list
    results = [dict(row) for row in rs]
    print(results)
    # close the connection
    conn.close()
    return results


@app.get("/get_prediction")
def get_prediction():
    """
    Queries the PostgreSQL database for prediction data.
    The function retrieves data from the PostgreSQL database and returns it as a JSON object.
    The data is filtered by the fields timestamp, prediction, and confidence.
    The function returns a JSON object containing the prediction data.
    """
    print("Querying PostgreSQL database...")
    # create a database connection
    conn = engine.connect()
    # create a SELECT statement
    select_sql = """
    SELECT * FROM consumption_prediction
    """
    # execute the SELECT statement
    rs = conn.execute(select_sql)
    # return all results as a JSON list
    results = [dict(row) for row in rs]
    print(results)
    # close the connection
    conn.close()
    return results











    



