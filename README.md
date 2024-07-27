# Quant-Stream Project


## Overview
Quant-Stream is a microservice designed to process real-time financial market data and provide an API for querying processed data. It connects to an exchange (ByBit, OKX, or Binance) using WebSockets to ingest public K-Line data for a given trading pair, processes the data to capture relevant data points, and exposes endpoints for querying processed data.

### Features
- Real-time data ingestion via WebSockets
- Backfilling historical data
- Calculation and querying of financial indicators (MACD, RSI)
- REST API for accessing K-Line data and indicators

## Setup Instructions
### Prerequisites
Ensure you have the following installed:

- Docker
- Docker Compose

## .env Example
Create a .env file in the root directory of the project with the following content
```
DEBUG=True
DATABASE_URL=postgresql://quantstream:quantstream@db:5432/quantstream
#Uncomment the following line if you want to connect to a local PostgreSQL instance
#DATABASE_URL=postgresql://quantstream:quantstream@localhost:5432/quantstream
POSTGRES_DB=quantstream
POSTGRES_USER=quantstream
POSTGRES_PASSWORD=quantstream
```

## Building and Running the Services
1. Build Docker Images
`docker-compose build`
2. Start the Services
`docker-compose up`

## Accessing the API
The API will be available at http://localhost:8000. You can use tools like curl or Postman to interact with the endpoints.

### Get K-Line Data

`GET /klines/{symbol}/{interval}`
#### Parameters:
- symbol (str): Trading pair symbol (e.g., BTCUSDT)
- interval (str): Time interval (e.g., 1m, 5m, 1h)


### Get MACD Indicator
`GET /indicators/macd/{symbol}/{interval}`
#### Parameters:
- symbol (str): Trading pair symbol (e.g., BTCUSDT)
- interval (str): Time interval (e.g., 1m, 5m, 1h)

### Get MACD Indicator
`GET /indicators/rsi/{symbol}/{interval}`
#### Parameters:
- symbol (str): Trading pair symbol (e.g., BTCUSDT)
- interval (str): Time interval (e.g., 1m, 5m, 1h)

P.S the endpoints return last 100 data points by default. 
You can modify the code to return more data points if needed.
Last number of return values is for the latest candle.