import json
import requests
import base64
from PIL import Image
from io import BytesIO
import streamlit as st
import re

# Set API details for models
url = "https://proxy.tune.app/chat/completions"
headers = {
    "Authorization": "sk-tune-QfKcSGhyo5b8HbWVSRT4M98UONQ4hQ65ryp",  # Replace with your actual API key
    "Content-Type": "application/json",
}

# Function to encode image into base64 format
def encode_image(image):
    if image.mode == 'RGBA':
        image = image.convert('RGB')  # Convert RGBA mode images into RGB mode
    buffered = BytesIO()
    image.save(buffered, format="JPEG")  # Save image into buffer as JPEG format
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to query model
def query_model(base64_image, prompt, model_id, max_tokens=1000, temperature=0.9):
    image_content = {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
    }

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
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        answer = response.json().get('choices', [{}])[0].get('message', {}).get('content', "")
        return answer.strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Function to extract HTML and CSS from model response
def extract_html_css(response_text):
    html_match = re.search(r"### HTML\n```html\n(.*?)```", response_text, re.DOTALL)
    css_match = re.search(r"### CSS.*\n```css\n(.*?)```", response_text, re.DOTALL)

    html_code = html_match.group(1).strip() if html_match else ""
    css_code = css_match.group(1).strip() if css_match else ""
    
    return html_code, css_code

# Function to write HTML and CSS to files
def write_files(html_code, css_code):
    with open("index.html", "w") as html_file:
        html_file.write(html_code)
    with open("styles.css", "w") as css_file:
        css_file.write(css_code)

# Streamlit UI setup
st.title("Image Description and HTML/CSS Generation")
model_choice = st.selectbox("Select Model for Image Understanding", 
                            options=["qwen/qwen-2-vl-72b", "openai/gpt-4o", "mistral/pixtral-12B-2409", "meta/llama-3.2-90b-vision"],
                            index=0)
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if 'description' not in st.session_state:
    st.session_state.description = None
if 'html_css' not in st.session_state:
    st.session_state.html_css = None

if st.button("Generate Description"):
    if uploaded_image:
        image = Image.open(uploaded_image)
        base64_image = encode_image(image)
        st.image(image)

        description_prompt_template = """
        Please analyze this software interface image provided below:
        Provide an extremely detailed description capturing every aspect including color schemes, typography, layout structures, navigation elements, forms, icons, spacing, etc.
        """
        description = query_model(base64_image, description_prompt_template, model_id=model_choice)
        st.session_state.description = description
        st.subheader("Generated Description:")
        st.markdown(description)

        if description:
            system_prompt = "You are TuneStudio, a coding assistant that generates HTML and CSS based on descriptions."
            user_prompt = f"Please create HTML and CSS based on the following detailed description: {description}"

            html_css_data = {
                "temperature": 0.9,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "model": "qwen/qwen-2.5-coder-32b",
                "max_tokens": 3000
            }

            response = requests.post(url, headers=headers, json=html_css_data)
            if response.status_code == 200:
                html_css_code = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
                st.session_state.html_css = html_css_code

                html_code, css_code = extract_html_css(html_css_code)
                
                if html_code and css_code:
                    write_files(html_code, css_code)
                    st.success("HTML and CSS files have been updated successfully.")
                else:
                    st.error("Could not extract HTML/CSS from the response.")
                
                st.subheader("Generated HTML and CSS:")
                st.code(html_css_code, language="html")
            else:
                st.error("Error generating HTML/CSS.")
    else:
        st.warning("Please upload an image.")
