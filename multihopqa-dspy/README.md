# MultiHopQA with DSPy, ColBERT, and Qwen 2.5 72B

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This repository contains tutorials and code implementations for **MultiHop Question Answering (QA)** using advanced tools such as **DSPy**, **ColBERT**, **HotPotQA**, **TuneAPI**, and **Qwen 2.5 72B**. MultiHopQA is a task where a question requires synthesizing information from multiple documents to derive the correct answer.

## Overview

The project demonstrates how to combine powerful **retrieval** and **language modeling** techniques to tackle multi-hop question-answering tasks. The pipeline uses **DSPy** to handle data pipelines and multi-step reasoning, **ColBERT** for dense retrieval, and **Qwen 2.5 72B** as the backbone generative model to provide the final answers. The **HotPotQA** dataset is used for training and evaluation.

### Tools Used:
- **DSPy**: Modular tool to help structure multi-hop question answering pipelines.
- **ColBERT**: A dense retrieval model that helps retrieve relevant passages for complex QA.
- **TuneAPI**: A proxy API for interacting with language models like Qwen.
- **Qwen 2.5 72B**: A state-of-the-art large language model for reasoning and text generation.
- **HotPotQA**: A dataset specifically designed for multi-hop QA.

## Steps to Run

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/aryankargwal/genai-tutorials.git
cd nlp-tutorials
```

### 2. Install Dependencies
Install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Set Up API Keys
To use the **TuneAPI** for Qwen, export your API key as an environment variable:
```bash
export API_KEY="your_api_key_here"
```

### 4. Run the Script
Run the main script to perform multi-hop QA:
```bash
python multihopqa.py
```

This will initiate the multi-hop reasoning process by:
1. Loading the **HotPotQA** dataset.
2. Using **ColBERT** for dense passage retrieval.
3. Utilizing **Qwen 2.5 72B** to generate answers based on the retrieved contexts.

## How It Works

1. **Data Loading**: The HotPotQA dataset is loaded and split into train/dev sets.
2. **Retrieval**: The **ColBERT** model retrieves relevant passages from a knowledge base using the input question.
3. **Reasoning**: The **Qwen 2.5 72B** model, via the **TuneAPI**, processes the retrieved context to answer the question.
4. **Prediction**: The final answer and relevant contexts are returned.

## Features
- **Multi-Hop Reasoning**: Tackles complex QA tasks that require synthesizing information from multiple sources.
- **Dense Retrieval with ColBERT**: Efficient passage retrieval from large knowledge bases.
- **State-of-the-Art Generative Model**: Uses **Qwen 2.5 72B** to process and answer questions.
- **HotPotQA**: Handles the popular QA dataset tailored for multi-hop reasoning.

## Simplified Baleen

**Simplified Baleen** is a key component of this repository, designed to streamline the process of combining retrieval and generation for multi-hop reasoning tasks. It integrates **ColBERT** for retrieval with **Qwen 2.5 72B** for reasoning and answering. The name **Baleen** is inspired by the baleen plates in whales, which filter information efficiently—just as the system filters through large corpora to retrieve relevant data.

### Key Features of Simplified Baleen:
- **Unified Interface**: Simplified Baleen abstracts the retrieval and reasoning process into a single pipeline, making it easier to use for complex QA tasks.
- **Retrieval-Augmented Generation**: Baleen leverages retrieval models like **ColBERT** to provide context for the generative model, allowing the language model to answer multi-hop questions more effectively.
- **Customizable Pipeline**: It allows users to define the retrieval method and the language model to create a flexible question-answering pipeline.

## Dataset

This repository uses the **HotPotQA** dataset, designed for multi-hop QA. You can find more details about it [here](https://hotpotqa.github.io/).

## Future Work
- **Fine-Tuning**: Future releases will include scripts for fine-tuning the model on custom datasets.
- **Enhanced Retrieval**: Improved passage retrieval techniques are in progress to further enhance the accuracy of multi-hop reasoning.

## License
This project is licensed under the Apache 2.0 License. See the full license [here](LICENSE).
