import streamlit as st
import torch
from PIL import Image
from transformers import AutoModelForCausalLM
from janus.models import MultiModalityCausalLM, VLChatProcessor
from janus.utils.io import load_pil_images

# Load model and processor once at the start
@st.cache_resource
def load_model():
    model_path = "deepseek-ai/Janus-1.3B"
    vl_chat_processor = VLChatProcessor.from_pretrained(model_path)
    tokenizer = vl_chat_processor.tokenizer
    vl_gpt = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
    vl_gpt = vl_gpt.to(torch.bfloat16).cuda().eval()
    return vl_chat_processor, tokenizer, vl_gpt

# Function to generate answers based on the uploaded image and question
def generate_answer(image, question):
    vl_chat_processor, tokenizer, vl_gpt = load_model()
    
    # Convert the uploaded image to RGB if it is not already in that format
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    conversation = [
        {
            "role": "User",
            "content": f"<image_placeholder>\n{question}",
            "images": ["uploaded_image"],
        },
        {"role": "Assistant", "content": ""},
    ]
    
    # Load and prepare the image
    pil_image = [image]  # As a list for batch processing
    prepare_inputs = vl_chat_processor(
        conversations=conversation, images=pil_image, force_batchify=True
    ).to(vl_gpt.device)

    # Get image embeddings and run the model
    inputs_embeds = vl_gpt.prepare_inputs_embeds(**prepare_inputs)
    outputs = vl_gpt.language_model.generate(
        inputs_embeds=inputs_embeds,
        attention_mask=prepare_inputs.attention_mask,
        pad_token_id=tokenizer.eos_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
        max_new_tokens=512,
        do_sample=False,
        use_cache=True,
    )

    answer = tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
    return answer

# Streamlit UI
st.title("Janus Image and Question Interface")

# Upload image
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Input for user question
user_question = st.text_input("Ask a question about the image")

# When the user uploads an image and asks a question
if uploaded_image and user_question:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Generate an answer from the model
    with st.spinner("Generating answer..."):
        answer = generate_answer(image, user_question)
    
    # Display the answer
    st.write(f"**Answer:** {answer}")
