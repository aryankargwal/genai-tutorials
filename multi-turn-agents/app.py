import streamlit as st
import requests
import json
from fpdf import FPDF

# Set the page configuration
st.set_page_config(page_title="Market Research & Campaign Planning", page_icon="📊")

# Streamlit app title and description
st.title("Market Research & Campaign Planning Tool 📊💬")
st.write("Perform market research, analyze numerical data, and generate a campaign poster, all in one place!")

# Text input for API key
api_key = st.sidebar.text_input("Enter your API key", type="password")

# Define the API headers and URLs for requests
research_url = "https://proxy.tune.app/chat/completions"

# Check if API key is provided
if api_key:
    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    # Function to call market research assistant
    def call_market_research_assistant(query):
        payload = {
            "temperature": 0.8,
            "messages": [{"role": "user", "content": query}],
            "model": "kargwalaryan/research",
            "stream": False,
            "frequency_penalty": 0,
            "max_tokens": 100
        }
        response = requests.post(research_url, headers=headers, data=json.dumps(payload))
        return response.json()

    # Function to extract and analyze numerical data from research
    def call_analytics_assistant(research_text):
        user_content = f"Here is some market research data: {research_text}. Extract all the stylistic and marketing insights from the research to come up with a prompt to generate the best campaign poster that resonates with the style using an image generation model."
        
        payload = {
            "temperature": 0.9,
            "messages": [
                {"role": "system", "content": "You are TuneStudio"},
                {"role": "user", "content": user_content}
            ],
            "model": "anthropic/claude-3.5-sonnet",
            "stream": False,
            "frequency_penalty": 0.2,
            "max_tokens": 300
        }
        response = requests.post(research_url, headers=headers, data=json.dumps(payload))
        return response.json()

    # Function to generate campaign poster based on analysis
    def call_image_generation(analysis_text):
        payload = {
            "temperature": 0.9,
            "messages": [
                {"role": "system", "content": "You are TuneStudio"},
                {"role": "user", "content": f"Generate a campaign poster based on this analysis: {analysis_result}"}
            ],
            "model": "kargwalaryan/image-gen",
            "stream": False,
            "frequency_penalty": 0.2,
            "max_tokens": 100
        }
        response = requests.post(research_url, headers=headers, data=json.dumps(payload))
        return response.json()

    # Function to create future campaign based on analysis
    def call_future_campaign(analysis_text):
        user_content = f"Based on the following analysis: {analysis_text}, generate a forward-looking campaign strategy that includes goals, target audience, and potential platforms for marketing."
        
        payload = {
            "temperature": 0.9,
            "messages": [
                {"role": "system", "content": "You are Sonet a modern smart and calculative Marketer"},
                {"role": "user", "content": user_content}
            ],
            "model": "anthropic/claude-3.5-sonnet",
            "stream": False,
            "frequency_penalty": 0.2,
            "max_tokens": 500
        }
        response = requests.post(research_url, headers=headers, data=json.dumps(payload))
        return response.json()

    # Function to create a PDF from the collected output
    def create_pdf(market_research, analysis_result, image_output, future_campaign):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.multi_cell(0, 10, "Market Research:\n" + market_research)
        pdf.add_page()
        pdf.multi_cell(0, 10, "Suggested Prompt:\n" + analysis_result)
        pdf.add_page()
        pdf.multi_cell(0, 10, "Generated Campaign:\n" + image_output)
        pdf.add_page()
        pdf.multi_cell(0, 10, "Future Campaign Strategy:\n" + future_campaign)

        return pdf.output(dest='S').encode('latin1')

    # Initialize session state variables to store research, analysis data, and image output
    if 'research_data' not in st.session_state:
        st.session_state.research_data = []
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = ""
    if 'image_output' not in st.session_state:
        st.session_state.image_output = ""
    if 'future_campaign' not in st.session_state:
        st.session_state.future_campaign = ""

    # Sidebar for input and actions
    st.sidebar.header("Actions")
    user_input = st.sidebar.text_input("Ask the market research assistant...")

    if st.sidebar.button("Perform All Operations") and user_input:
        # Step 1: Perform Market Research
        research_response = call_market_research_assistant(user_input)
        research_result = research_response.get('choices', [{}])[0].get('message', {}).get('content', "No response")
        
        # Store research result in session state
        st.session_state.research_data.append(research_result)

        # Step 2: Create Campaign Poster Prompt
        last_research = st.session_state.research_data[-1]
        analytics_response = call_analytics_assistant(last_research)
        analysis_result = analytics_response.get('choices', [{}])[0].get('message', {}).get('content', "No response")
        
        # Store the analysis result in session state
        st.session_state.analysis_result = analysis_result

        # Step 3: Generate Campaign Poster
        poster_response = call_image_generation(st.session_state.analysis_result)
        poster_text = poster_response.get('choices', [{}])[0].get('message', {}).get('content', "No response")
        
        # Store the image output directly in session state
        st.session_state.image_output = poster_text

        # Step 4: Generate Future Campaign
        future_campaign_response = call_future_campaign(st.session_state.analysis_result)
        future_campaign_text = future_campaign_response.get('choices', [{}])[0].get('message', {}).get('content', "No response")

        # Store the future campaign strategy in session state
        st.session_state.future_campaign = future_campaign_text

        # Display results after all operations
        st.write("### Market Research")
        st.markdown(research_result)

        st.write("### Suggested Prompt")
        st.markdown(analysis_result)

        st.write("### Generated Campaign")
        st.markdown(poster_text)

        st.write("### Future Campaign Strategy")
        st.markdown(future_campaign_text)

    # Button to download all outputs as a PDF
    if st.session_state.research_data or st.session_state.analysis_result or st.session_state.image_output or st.session_state.future_campaign:
        if st.button("Download All Outputs as PDF"):
            pdf_content = create_pdf(
                st.session_state.research_data[-1] if st.session_state.research_data else "No market research available",
                st.session_state.analysis_result if st.session_state.analysis_result else "No analysis available",
                st.session_state.image_output if st.session_state.image_output else "No campaign generated",
                st.session_state.future_campaign if st.session_state.future_campaign else "No future campaign generated"
            )
            st.download_button(
                label="Download PDF",
                data=pdf_content,
                file_name="market_research_campaign.pdf",
                mime="application/pdf"
            )
else:
    st.sidebar.warning("Please enter your API key to use the tool.")
