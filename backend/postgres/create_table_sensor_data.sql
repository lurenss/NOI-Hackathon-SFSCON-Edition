CREATE TABLE sensor_data (
  timestamp INT PRIMARY KEY NOT NULL,
  temperature DECIMAL(5,2) NOT NULL,
  humidity INT NOT NULL,
  iaq DECIMAL(5,2) NOT NULL,
  co2 INT NOT NULL,
  gas INT NOT NULL,
  battery INT NOT NULL
);
