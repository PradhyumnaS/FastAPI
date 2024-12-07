import streamlit as st

# Step 1: App Title
st.title("Unit Converter App")
st.write("Convert between different units of measurement easily!")

# Debugging: Confirm app runs
st.write("Debug: App is running!")

# Step 2: Conversion Categories
categories = ["Length", "Weight", "Temperature"]
selected_category = st.selectbox("Select a category:", categories)

st.write(f"Debug: Selected category - {selected_category}")

# Step 3: Input for Conversion
if selected_category == "Length":
    st.subheader("Length Conversion")
    length_units = ["Meters", "Kilometers", "Miles", "Feet"]
    from_unit = st.selectbox("From:", length_units)
    to_unit = st.selectbox("To:", length_units)
    value = st.number_input("Enter the value to convert:", min_value=0.0, format="%.2f")
    
    # Debugging: Show inputs
    st.write(f"Debug: Length Conversion - From {from_unit} to {to_unit}, value: {value}")

    # Conversion Logic for Length
    conversion_factors = {
        "Meters": {"Meters": 1, "Kilometers": 0.001, "Miles": 0.000621371, "Feet": 3.28084},
        "Kilometers": {"Meters": 1000, "Kilometers": 1, "Miles": 0.621371, "Feet": 3280.84},
        "Miles": {"Meters": 1609.34, "Kilometers": 1.60934, "Miles": 1, "Feet": 5280},
        "Feet": {"Meters": 0.3048, "Kilometers": 0.0003048, "Miles": 0.000189394, "Feet": 1},
    }
    result = value * conversion_factors[from_unit][to_unit]
    st.write(f"Result: {value} {from_unit} = {result:.2f} {to_unit}")

elif selected_category == "Weight":
    st.subheader("Weight Conversion")
    weight_units = ["Kilograms", "Pounds", "Grams"]
    from_unit = st.selectbox("From:", weight_units)
    to_unit = st.selectbox("To:", weight_units)
    value = st.number_input("Enter the value to convert:", min_value=0.0, format="%.2f")
    
    # Debugging: Show inputs
    st.write(f"Debug: Weight Conversion - From {from_unit} to {to_unit}, value: {value}")

    # Conversion Logic for Weight
    conversion_factors = {
        "Kilograms": {"Kilograms": 1, "Pounds": 2.20462, "Grams": 1000},
        "Pounds": {"Kilograms": 0.453592, "Pounds": 1, "Grams": 453.592},
        "Grams": {"Kilograms": 0.001, "Pounds": 0.00220462, "Grams": 1},
    }
    result = value * conversion_factors[from_unit][to_unit]
    st.write(f"Result: {value} {from_unit} = {result:.2f} {to_unit}")

elif selected_category == "Temperature":
    st.subheader("Temperature Conversion")
    temp_units = ["Celsius", "Fahrenheit", "Kelvin"]
    from_unit = st.selectbox("From:", temp_units)
    to_unit = st.selectbox("To:", temp_units)
    value = st.number_input("Enter the value to convert:", format="%.2f")
    
    # Debugging: Show inputs
    st.write(f"Debug: Temperature Conversion - From {from_unit} to {to_unit}, value: {value}")

    # Conversion Logic for Temperature
    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            result = (value * 9/5) + 32
        elif to_unit == "Kelvin":
            result = value + 273.15
        else:
            result = value
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            result = (value - 32) * 5/9
        elif to_unit == "Kelvin":
            result = (value - 32) * 5/9 + 273.15
        else:
            result = value
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            result = value - 273.15
        elif to_unit == "Fahrenheit":
            result = (value - 273.15) * 9/5 + 32
        else:
            result = value
    
    st.write(f"Result: {value} {from_unit} = {result:.2f} {to_unit}")

# Footer
st.write("Built with 💻 by PrasannaG")
