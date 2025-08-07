from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# File paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRICES_PATH = os.path.join(BASE_DIR, 'data', 'brent_oil_prices.csv')
EVENTS_PATH = os.path.join(BASE_DIR, 'data', 'events.csv')
CHANGE_POINTS_PATH = os.path.join(BASE_DIR, 'data', 'change_points.csv')

@app.get("/api/prices")
async def get_prices():
    try:
        prices = pd.read_csv(PRICES_PATH)
        prices['Date'] = pd.to_datetime(prices['Date'], format='%d-%b-%y', errors='coerce')
        if prices['Date'].isnull().any():
            raise ValueError("Invalid date format in brent_oil_prices.csv")
        prices = prices[['Date', 'Price']]
        prices['Date'] = prices['Date'].dt.strftime('%Y-%m-%d')
        return prices.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/events")
async def get_events():
    try:
        events = pd.read_csv(EVENTS_PATH)
        events['Date'] = pd.to_datetime(events['Date'], format='%Y-%m-%d', errors='coerce')
        if events['Date'].isnull().any():
            raise ValueError("Invalid date format in events.csv")
        events = events[['Date', 'Event']]
        events['Date'] = events['Date'].dt.strftime('%Y-%m-%d')
        return events.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/change_points")
async def get_change_points():
    try:
        if not os.path.exists(CHANGE_POINTS_PATH):
            raise FileNotFoundError("change_points.csv not found. Complete Task 2 first.")
        change_points = pd.read_csv(CHANGE_POINTS_PATH)
        change_points['Date'] = pd.to_datetime(change_points['Date'], errors='coerce')
        if change_points['Date'].isnull().any():
            raise ValueError("Invalid date format in change_points.csv")
        change_points['Date'] = change_points['Date'].dt.strftime('%Y-%m-%d')
        return change_points.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
