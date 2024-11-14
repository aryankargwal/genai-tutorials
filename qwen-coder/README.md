# Qwen 2.5 Coder - UI to Code Generation using Vision-Language Models

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Welcome to the **Qwen 2.5 Coder** repository! This project demonstrates the capabilities of the **Qwen 2.5 Coder model** to automate the transformation of UI elements into structured HTML and CSS, leveraging the power of vision-language models (VLMs). With this tool, developers and designers can streamline the UI design process and rapidly prototype web components.

## Overview

Qwen 2.5 Coder by Alibaba is a cutting-edge **vision-language model** that interprets visual inputs and translates them into code, helping convert UI layouts into HTML/CSS formats. It’s designed to understand complex visual features and generate accurate, ready-to-use code snippets. This repository provides a **Streamlit** application for interactive UI-to-code transformation.

### Key Highlights:
- **Automated Code Generation**: Transform images of UI layouts into structured HTML/CSS with a few clicks.
- **Flexible Model Options**: Choose between multiple powerful models like Qwen 2.5, Pixtral, GPT-4o, and LLaMA for diverse coding and layout needs.
- **Simple Deployment**: Run the code transformation tool locally with minimal setup.

## Repository Contents

- **Streamlit Application**: A web app interface for uploading UI images and generating HTML/CSS.
- **Code Scripts**: Functions to encode images, call the model API, and process code outputs.
- **HTML/CSS Extraction**: Automated extraction of code blocks for easy integration into your projects.

---

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/aryankargwal/genai-tutorials
cd genai-tutorials
cd qwen-coder
```

### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

### 3. Set Up API Credentials
Ensure you have an API key from [Tune Studio](https://studio.tune.app/login) to access the Qwen model.

### 4. Run the Streamlit App
To start the interactive UI for uploading images and generating HTML/CSS:
```bash
streamlit run app.py
```

## How It Works

1. **Image Upload**: Upload any UI image, such as a wireframe or a screenshot of a software layout.
2. **Model Selection**: Choose from Qwen, GPT-4o, Pixtral, and LLaMA models for generating code based on your specific requirements.
3. **Generate HTML/CSS**: Get a detailed description and HTML/CSS code output for the UI elements in your image.

---

## Features

- **Multimodal Parsing**: Qwen and other models accurately interpret both visual and text elements.
- **User-Friendly Interface**: Easily upload, process, and view outputs in a streamlined app.
- **Versatile Model Choices**: Experiment with different models to get the best results for diverse UI scenarios.

## Future Development

- **Model Fine-Tuning**: Tutorials for optimizing Qwen 2.5 on unique data sets.
- **Extended Use Cases**: Explore applications in automated prototyping, document parsing, and screen parsing.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

