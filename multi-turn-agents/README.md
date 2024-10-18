# 🧠 Multi-Turn-Agents in an Application
This repository contains a **Streamlit** web application that leverages **Tune Studio**, an advanced platform for building and managing AI assistants using multiple large language models (LLMs), to conduct market research and generate marketing campaigns. The app uses different AI assistants to:
1. Extract and analyze market research data.
2. Generate a detailed image prompt using the **Claude Sonet** model.
3. Produce the final campaign poster image using **GPT-4o** for image generation.

The application enables you to:
- Perform market research.
- Analyze insights from the data.
- Generate a marketing campaign poster.
- Download the results as a PDF.

## 🎯 Features

- **Market Research Assistant**: Query the AI assistant to conduct in-depth market research using the models available on Tune Studio.
- **Campaign Prompt Generator**: Analyze research data to generate an image prompt that aligns with the research insights.
- **Campaign Poster Generator**: Create an image prompt to generate a marketing poster using GPT-4o.
- **Download PDF**: Export all the research, analysis, and generated content as a PDF.

## 🛠️ Installation

To run this application locally, follow the steps below:

### 1. Clone the Repository

```bash
git clone https://github.com/aryankargwal/genai-tutorials.git
cd genai-tutorials/multi-turn-agents
```

### 2. Set up API Key

The application requires an API key to interact with **Tune Studio** for the AI assistants. During runtime, you can input this key into the app's sidebar.

### 3. Run the Application

```bash
streamlit run app.py
```

The app should now be running on `http://localhost:8501/`.

## 🔑 API Key

You’ll need an API key from **Tune Studio** to use their AI assistant models. Tune Studio offers access to a variety of models such as **Claude Sonet**, **GPT-4o**, **LLaMA 3.1**, **Haiku**, and more. You can input your API key in the app's sidebar during usage.

## 🧩 Application Workflow

### 1. **Market Research**: 
   - Enter a query to conduct market research using **Tune Studio’s** AI assistant (based on a model like **Claude Sonet** or **LLaMA 3.1**).
   - The AI assistant retrieves relevant research and insights from the web.
   - Results are displayed under the "Market Research" section.

### 2. **Generate Campaign Prompt**: 
   - Once research is performed, the assistant analyzes the insights and generates a prompt for image creation.
   - This prompt is crafted to fit the style and tone of the marketing campaign you are aiming for.
   - Results are displayed under "Suggested Prompt."

### 3. **Generate Campaign Poster**:
   - Using the image generation prompt, the app interacts with the **GPT-4o** model to generate a campaign poster image.
   - The generated image description is displayed under "Generated Campaign."

### 4. **Download PDF**:
   - You can export the market research, analysis, and campaign outputs as a PDF file.

## 🧑‍💻 Code Overview

### Main Functions

- **`call_market_research_assistant(query)`**: Interacts with the market research AI assistant via **Tune Studio** to fetch data based on the user’s query.
- **`call_analytics_assistant(research_text)`**: Analyzes research data to generate an image generation prompt for the campaign poster.
- **`call_image_generation(analysis_text)`**: Uses the AI assistant (GPT-4o) to generate the marketing campaign poster.
- **`create_pdf(market_research, analysis_result, image_output)`**: Compiles the market research, analysis, and image output into a PDF.

### Key Libraries

- `Streamlit`: For the web application interface.
- `Requests`: To handle API calls to the **Tune Studio** AI assistants.
- `FPDF`: For generating downloadable PDF reports.

## 🌐 Tune Studio Platform

**Tune Studio** allows you to create and manage AI assistants on their platform, offering multi-functionality for large language models such as **Claude Sonet**, **GPT-4o**, **LLaMA 3.1**, **Haiku**, and more. This application utilizes these models to perform tasks like:
- Market research (e.g., using Claude Sonet or LLaMA 3.1).
- Image generation (e.g., GPT-4o).
- Text-based analysis for generating image prompts.

Tune Studio simplifies access to multiple models through API calls, allowing flexible integration into applications like this one.

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for the application.

## 🌟 Acknowledgments

- [Streamlit](https://streamlit.io/) for providing an easy-to-use platform for building interactive web apps.
- [Tune Studio](https://tunehq.ai/) for enabling seamless integration with various large language models and multi-functional AI assistants.
