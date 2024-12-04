from fastapi import FastAPI, HTTPException, Query, staticfiles
from fastapi.responses import HTMLResponse
from flask.cli import load_dotenv
from pydantic import BaseModel
from typing import List, Optional
import httpx
import os

load_dotenv()

app = FastAPI()

app.mount("/static", staticfiles.StaticFiles(directory="static"), name="static")

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
ALPHA_VANTAGE_BASE_URL = "https://www.alphavantage.co/query"

class StockData(BaseModel):
    symbol: str
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int

class StockFilter(BaseModel):
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    min_volume: Optional[int] = None
    max_volume: Optional[int] = None

async def fetch_stock_data(symbol: str):
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(ALPHA_VANTAGE_BASE_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to fetch stock data")
        
        data = response.json()
        if "Time Series (Daily)" not in data:
            if "Error Message" in data or "Note" in data:
                raise HTTPException(status_code=404, detail="Stock symbol not supported or API limit exceeded")
            raise HTTPException(status_code=404, detail="Stock data not found")
        
        latest_date = max(data["Time Series (Daily)"].keys())
        latest_data = data["Time Series (Daily)"][latest_date]
        return StockData(
            symbol=symbol,
            date=latest_date,
            open=float(latest_data["1. open"]),
            high=float(latest_data["2. high"]),
            low=float(latest_data["3. low"]),
            close=float(latest_data["4. close"]),
            volume=int(latest_data["5. volume"]),
        )

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/stocks/{symbol}", response_model=StockData)
async def get_stock(symbol: str):
    return await fetch_stock_data(symbol)

@app.post("/stocks/filter", response_model=List[StockData])
async def filter_stocks(
    filter_criteria: StockFilter,
    symbols: str = Query(..., description="Comma-separated list of stock symbols")
):
    symbol_list = symbols.split(",")
    matching_stocks = []

    for symbol in symbol_list:
        try:
            stock = await fetch_stock_data(symbol.strip())
            if (
                (filter_criteria.min_price is None or stock.close >= filter_criteria.min_price) and
                (filter_criteria.max_price is None or stock.close <= filter_criteria.max_price) and
                (filter_criteria.min_volume is None or stock.volume >= filter_criteria.min_volume) and
                (filter_criteria.max_volume is None or stock.volume <= filter_criteria.max_volume)
            ):
                matching_stocks.append(stock)
                print(f"Stock {symbol} matches criteria.")
            else:
                print(f"Stock {symbol} does not match criteria.")
        except HTTPException as e:
            print(f"Error fetching data for {symbol}: {e.detail}")
            continue
    return matching_stocks



