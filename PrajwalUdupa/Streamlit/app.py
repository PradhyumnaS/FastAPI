import streamlit as st
import tensorflow as tf
import keras
import numpy as np
from PIL import Image

# Load the MobileNetV2 model pre-trained on ImageNet
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Function to process and predict the image
def classify_image(uploaded_image):
    # Open the image and resize it to 224x224 (required by MobileNetV2)
    img = Image.open(uploaded_image)
    img = img.resize((224, 224))
    
    # Convert image to numpy array
    img_array = np.array(img)
    
    # Preprocess image for MobileNetV2 (normalization)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)

    # Add batch dimension (MobileNetV2 expects a batch of images)
    img_array = np.expand_dims(img_array, axis=0)

    # Get predictions
    predictions = model.predict(img_array)

    # Decode the predictions to get human-readable labels
    decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=3)[0]
    
    return decoded_predictions

# Streamlit app UI
st.title("Image Classifier with MobileNetV2")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)

    # Get predictions for the image
    predictions = classify_image(uploaded_file)

    # Display predictions
    st.subheader("Predictions:")
    for i, (imagenet_id, label, score) in enumerate(predictions):
        st.write(f"{i+1}. **{label}** (Confidence: {score*100:.2f}%)")
