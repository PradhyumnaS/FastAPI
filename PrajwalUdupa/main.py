from fastapi import FastAPI, HTTPException
from typing import List
from .schemas import CurrencyConversionRequest, CurrencyConversionResponse
from .constants import EXCHANGE_RATES

# Initialize FastAPI app
app = FastAPI()

# Route for the root URL
@app.get("/")
def read_root():
    return {"message": "Welcome to the Currency Converter API!"}

# Route to get the list of supported currencies
@app.get("/currencies")
def get_supported_currencies():
    return {"currencies": list(EXCHANGE_RATES.keys())}

# Route for converting currencies (POST /convert)
@app.post("/convert", response_model=CurrencyConversionResponse)
def convert_currency(request: CurrencyConversionRequest):
    if request.from_currency not in EXCHANGE_RATES:
        raise HTTPException(status_code=400, detail="Unsupported from_currency")
    if request.to_currency not in EXCHANGE_RATES.get(request.from_currency, {}):
        raise HTTPException(status_code=400, detail="Unsupported to_currency")

    exchange_rate = EXCHANGE_RATES[request.from_currency].get(request.to_currency)
    converted_amount = request.amount * exchange_rate

    return CurrencyConversionResponse(
        from_currency=request.from_currency,
        to_currency=request.to_currency,
        amount=request.amount,
        converted_amount=converted_amount
    )

# Route to convert currency using GET parameters
@app.get("/convert")
def convert_currency_get(
    from_currency: str, 
    to_currency: str, 
    amount: float
):
    if from_currency not in EXCHANGE_RATES:
        raise HTTPException(status_code=400, detail="Unsupported from_currency")
    if to_currency not in EXCHANGE_RATES.get(from_currency, {}):
        raise HTTPException(status_code=400, detail="Unsupported to_currency")

    exchange_rate = EXCHANGE_RATES[from_currency].get(to_currency)
    converted_amount = amount * exchange_rate

    return CurrencyConversionResponse(
        from_currency=from_currency,
        to_currency=to_currency,
        amount=amount,
        converted_amount=converted_amount
    )

# Route to get exchange rates for a given currency
@app.get("/rates/{currency}")
def get_exchange_rates(currency: str):
    if currency not in EXCHANGE_RATES:
        raise HTTPException(status_code=400, detail="Unsupported currency")

    return EXCHANGE_RATES[currency]
