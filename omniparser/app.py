# Imports
from utils import get_som_labeled_img, check_ocr_box, get_caption_model_processor, get_yolo_model
import torch
from ultralytics import YOLO
from PIL import Image
import streamlit as st
import base64
import matplotlib.pyplot as plt
import io
import tempfile

# Initialize device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Streamlit file upload
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Check if an image has been uploaded
if uploaded_file:
    image = Image.open(uploaded_file)
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
        image_path = tmp_file.name
        image.save(image_path)

    # Load YOLO model
    som_model = get_yolo_model(model_path='weights/icon_detect/best.pt').to(device)
    print(f'Model loaded to {device}')
    
    # Load caption model processor
    caption_model_processor = get_caption_model_processor(
        model_name="blip2",
        model_name_or_path="weights/icon_caption_blip2",
        device=device
    )

else:
    image_path = 'imgs/windows_home.png'  # Default image path
    image = Image.open(image_path)

# Button to start inference
if st.button("Run Inference") and uploaded_file:
    image_rgb = image.convert('RGB')

    # Set draw config and threshold
    draw_bbox_config = {
        'text_scale': 0.8,
        'text_thickness': 2,
        'text_padding': 3,
        'thickness': 3,
    }
    BOX_THRESHOLD = 0.03

    # Run OCR and object detection
    ocr_bbox_rslt, is_goal_filtered = check_ocr_box(
        image_path,
        display_img=False,
        output_bb_format='xyxy',
        goal_filtering=None,
        easyocr_args={'paragraph': False, 'text_threshold': 0.9}
    )
    text, ocr_bbox = ocr_bbox_rslt

    # Generate labeled image
    dino_labeled_img, label_coordinates, parsed_content_list = get_som_labeled_img(
        img_path=image_path,
        model=som_model,
        BOX_TRESHOLD=BOX_THRESHOLD,
        output_coord_in_ratio=False,
        ocr_bbox=ocr_bbox,
        draw_bbox_config=draw_bbox_config,
        caption_model_processor=caption_model_processor,
        ocr_text=text,
        use_local_semantics=True,
        iou_threshold=0.1
    )

    # Display base64 image using Streamlit
    if dino_labeled_img:
        decoded_image = Image.open(io.BytesIO(base64.b64decode(dino_labeled_img)))
        st.image(decoded_image, caption="Labeled Image")
    else:
        st.write("Error decoding the labeled image.")

    # Print label coordinates and parsed content list
    st.write("Label Coordinates:", label_coordinates)
    st.write("Parsed Content List:", parsed_content_list)
