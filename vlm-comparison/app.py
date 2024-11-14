import requests
import base64
from PIL import Image
from io import BytesIO
import pandas as pd
import os
import csv
import streamlit as st
import time

# Set the API details for the model
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "API-KEY",  # This is a Temp Key, Add your own Key
    "Content-Type": "application/json",
}

# Function to encode image to base64
def encode_image(image):
    if image.mode == 'RGBA':
        image = image.convert('RGB')  # Convert RGBA to RGB
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Save image as JPEG to buffer
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Combined function for querying models
def query_model(base64_image, question, model_id, max_tokens=300, temperature=0.9, stream=False, frequency_penalty=0.2):
    image_content = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    }

    prompt = question

    data = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    image_content
                ]
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": stream,
        "frequency_penalty": frequency_penalty
    }

    # Latency calculation start
    start_time = time.time()

    # Make API request
    response = requests.post(url, headers=headers, json=data)

    latency = time.time() - start_time

    if response.status_code == 200:
        answer = response.json().get('choices', [{}])[0].get('message', {}).get('content', "No response")
        return answer, latency
    else:
        return f"Error: {response.status_code} - {response.text}", latency

# Save results to CSV
def save_to_csv(image_path, question, model_1_response, model_2_response, model_1_latency, model_2_latency, model_1_tokens, model_2_tokens, best_model):
    file_exists = os.path.isfile('art.csv')
    
    data = {
        'Image Path': image_path,
        'Question': question,
        'Llama 3.2 Response': model_1_response,
        'GPT 4o Response': model_2_response,
        'Llama 3.2 Latency': model_1_latency,
        'GPT 4o Latency': model_2_latency,
        'Llama 3.2 Tokens': model_1_tokens,
        'GPT 4o Tokens': model_2_tokens,
        'Best Model': best_model
    }

    df = pd.DataFrame([data])

    # Ensure proper quoting to handle commas and double quotes
    if not file_exists:
        df.to_csv('art.csv', index=False, quoting=csv.QUOTE_ALL, escapechar='\\')
    else:
        df.to_csv('art.csv', mode='a', header=False, index=False, quoting=csv.QUOTE_ALL, escapechar='\\')

# Streamlit UI
st.title("VLM Model Stress Test")

# Upload an image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_image:
    image = Image.open(uploaded_image)
    base64_image = encode_image(image)
    st.image(image)

# User input for the question
question = st.text_input("Enter your question:")

# Model selection
model_options = {
    "Llama 3.2": "meta/llama-3.2-90b-vision",
    "Qwen 2 VL": "qwen/qwen-2-vl-72b",
    "GPT 4o": "anthropic/claude-3.5-sonnet"
}
model_1 = st.selectbox("Select the first model:", list(model_options.keys()))
model_2 = st.selectbox("Select the second model:", list(model_options.keys()))

# Initialize session state variables
if 'responses' not in st.session_state:
    st.session_state.responses = None

# Generate responses and display metrics
if st.button("Generate Responses"):
    if uploaded_image is not None and question:
        model_1_id = model_options[model_1]
        model_2_id = model_options[model_2]
        
        response_1, latency_1 = query_model(base64_image, question, model_1_id)
        response_2, latency_2 = query_model(base64_image, question, model_2_id)

        tokens_1 = len(response_1.split())
        tokens_2 = len(response_2.split())

        st.session_state.responses = {
            "model_1_response": response_1,
            "model_1_latency": latency_1,
            "model_1_tokens": tokens_1,
            "model_2_response": response_2,
            "model_2_latency": latency_2,
            "model_2_tokens": tokens_2,
        }

        # Display results in columns
        st.subheader("Model Responses and Metrics")
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"{model_1} Response")
            st.write(response_1)
            st.markdown(f"**Latency:** {latency_1:.2f} seconds")
            st.markdown(f"**Tokens:** {tokens_1}")

        with col2:
            st.subheader(f"{model_2} Response")
            st.write(response_2)
            st.markdown(f"**Latency:** {latency_2:.2f} seconds")
            st.markdown(f"**Tokens:** {tokens_2}")

        st.success("Responses generated successfully! Now choose the best model and save your results.")
    else:
        st.warning("Please upload an image and enter a question.")

# Dropdown to choose the better model
best_model = st.selectbox("Choose the better model based on responses:", options=[model_1, model_2])

# Save results to CSV
if st.button("Save Best Model to CSV"):
    if st.session_state.responses:
        save_to_csv(
            image_path=uploaded_image.name,
            question=question,
            model_1_response=st.session_state.responses['model_1_response'],
            model_2_response=st.session_state.responses['model_2_response'],
            model_1_latency=st.session_state.responses['model_1_latency'],
            model_2_latency=st.session_state.responses['model_2_latency'],
            model_1_tokens=st.session_state.responses['model_1_tokens'],
            model_2_tokens=st.session_state.responses['model_2_tokens'],
            best_model=best_model
        )
        st.success("Data saved successfully!")
    else:
        st.warning("Please generate responses first before saving.")
