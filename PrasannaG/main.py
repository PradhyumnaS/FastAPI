from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the FastAPI app
app = FastAPI()

# Boolean Converter Function
def convert_to_bool(value: str) -> bool:
    """
    Converts a string to a boolean value.
    Accepted values: 'true', 'false', '1', '0', 'yes', 'no'
    """
    value = value.strip().lower()
    if value in ['true', '1', 'yes']:
        return True
    elif value in ['false', '0', 'no']:
        return False
    else:
        raise ValueError("Invalid value for conversion to boolean.")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Boolean Converter API!"}

# Endpoint to convert string to boolean
@app.get("/convert/{value}")
def convert(value: str):
    try:
        # Convert the string value to boolean
        boolean_value = convert_to_bool(value)
        return {"input": value, "converted_to": boolean_value}
    except ValueError as e:
        return {"error": str(e)}
