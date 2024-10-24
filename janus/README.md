Here's an updated README with the Janus paper link and the correct installation command:

---

# Janus 1.3B - Multimodal & Image Generation Abilities

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This repository explores the **multimodal** and **image generation** capabilities of **[Janus 1.3B](https://arxiv.org/abs/2410.13848)**, one of the smallest yet highly effective vision-language models (VLMs). Despite its compact size, Janus delivers impressive results in both natural language processing and image generation, proving to be a powerful tool for real-world multimodal applications.

## Overview

[Janus 1.3B](https://arxiv.org/abs/2410.13848) is designed to handle both text and visual data in a unified framework. It is a compact yet highly capable model, excelling at tasks like visual question answering, captioning, and image-text retrieval. The paper provides more insights into its architecture and performance.

This repo includes:
- **Streamlit applications** for **image generation** and **multimodal inference** using Janus.
- Easy-to-use scripts that demonstrate how to utilize the model in under 200 lines of code.

### Tools & Frameworks:
- **Janus 1.3B**: Vision-Language Model for multimodal tasks.
- **Streamlit**: Framework for building web apps to run multimodal and image generation demos.

## Steps to Run

### 1. Clone the Repository
```bash
git clone https://github.com/aryankargwal/genai-tutorials.git
cd genai-tutorials/janus-multimodal
```

### 2. Install Dependencies
Install the necessary requirements using the command:
```bash
pip install -e .
```

### 3. Run the Streamlit Applications

For **image generation**:
```bash
streamlit run app.py
```

For **multimodal inference** (e.g., Visual Question Answering):
```bash
streamlit run multi.py
```

## Features

- **Multimodal Inference**: Handle tasks like Visual Question Answering (VQA) with Janus, combining text and image inputs for reasoning.
- **Image Generation**: Generate high-quality images from text descriptions using a streamlined and efficient framework.
- **Compact but Powerful**: With just 1.3B parameters, [Janus](https://arxiv.org/abs/2410.13848) offers a remarkable balance between size and performance, making it accessible for real-world deployment.

## Future Work
- **Fine-tuning**: Future updates will include tutorials for fine-tuning Janus on custom datasets.
- **Advanced Inferences**: Explore more complex multimodal tasks and benchmarks in upcoming releases.

## License
This project is licensed under the Apache 2.0 License. See the full license [here](LICENSE).

---

This version now includes the link to the [Janus paper](https://arxiv.org/abs/2410.13848) and the corrected `pip install -e .` command. Let me know if any other changes are needed!