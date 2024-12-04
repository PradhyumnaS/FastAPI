from pydantic import BaseModel

class CurrencyConversionRequest(BaseModel):
    from_currency: str
    to_currency: str
    amount: float

class CurrencyConversionResponse(BaseModel):
    from_currency: str
    to_currency: str
    amount: float
    converted_amount: float
