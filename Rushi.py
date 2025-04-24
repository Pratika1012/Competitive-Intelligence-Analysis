import streamlit as st
import pandas as pd
from groq import Groq
from datetime import datetime, timedelta
import base64
from fpdf import FPDF
from io import BytesIO

st.set_page_config(layout="wide")

# Configure Groq API
groq_api_key = st.secrets.get("GROQ_API_KEY", "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")  # Replace with your Groq API key
try:
    client = Groq(api_key=groq_api_key)
    if not hasattr(client, 'chat') or not hasattr(getattr(client, 'chat'), 'completions'):
        st.error("Groq client initialization failed: Invalid API key or unsupported method.")
        st.stop()
except Exception as e:
    st.error(f"Failed to initialize Groq client: {str(e)}")
    st.stop()

# Define generation configuration
generation_config = {
    "temperature": 0.0,
    "max_tokens": 4096,
    "top_p": 1.0,
}

def generate_content(prompt, config):
    """Helper function to generate content using Groq API."""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Ensure this model is available
            messages=[{"role": "user", "content": prompt}],  # Chat format with a single user message
            temperature=config["temperature"],
            max_tokens=config["max_tokens"],
            top_p=config["top_p"]
        )
        return response.choices[0].message.content  # Extract the generated text
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None

def generate_pdf(response_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, response_text)
    pdf_buffer = pdf.output(dest='S').encode('latin1')
    b64_pdf = base64.b64encode(pdf_buffer).decode()
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Generated_Analysis.pdf">Download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

challenge = "RSS Feeds for Competitive Intelligence and Summarization"
objective = "Stay ahead of competitors by monitoring industry trends"
analysis = "Competitive Intelligence Analysis"

st.sidebar.header("Competitive Intelligence Analysis")
industry = st.sidebar.text_input("Industry Name", "Pharmaceutical")
market = st.sidebar.text_input("Market/Geography Name", "United States")
client = st.sidebar.text_input("Client Name", "Astrazeneca")
curr_date = st.sidebar.date_input("Fortnight End Date", format="DD/MM/YYYY")
temperature = st.sidebar.slider('Generated Text (Deterministic <===> Creative)', 0.0, 0.5, 0.25)
top_p = st.sidebar.slider('Vocabulary Diversity (Deterministic <===> Creative)', 0.1, 1.0, 0.9)

generation_config2 = {
    "temperature": temperature,
    "max_tokens": 4096,
    "top_p": top_p,
}

if st.sidebar.button("Generate Analysis"):
    days_to_subtract = timedelta(days=15)
    past_date = curr_date - days_to_subtract
    desired_format = "%d-%m-%Y"
    curr_date_str = curr_date.strftime(desired_format)
    past_date_str = past_date.strftime(desired_format)

    st.markdown(f"<h2 style='text-align: center;'>Fortnightly Newsletter</h2>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Competitive Intelligence Analysis for {client}</h3>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{industry} industry in {market}</h3>", unsafe_allow_html=True)

    competitor_list = f"For {industry} industry, {market} market, {client} client, give a list of competitors."
    response_comp = generate_content(competitor_list, generation_config)
    if response_comp is None:
        st.stop()

    RSS_feed1 = f"For {industry} industry, {market} market, compile a list of relevant RSS feed URLs."
    RSS_feed2 = f"For {industry} industry, {market} market, {client} client and {response_comp} competitors, compile a list of relevant RSS feed URLs."

    prompt1 = f"{analysis}\n{objective}\n{RSS_feed1}"
    response1 = generate_content(prompt1, generation_config)
    if response1 is None:
        st.stop()

    prompt2 = f"{analysis}\n{objective}\n{RSS_feed2}"
    response2 = generate_content(prompt2, generation_config)
    if response2 is None:
        st.stop()

    combine_prompt = f"Combine two responses.\nResponse 1: {response1}\nResponse 2: {response2}"
    combined_response = generate_content(combine_prompt, generation_config)
    if combined_response is None:
        st.stop()

    analysis_RSS = f"For {client} client, {industry} industry, {market} market, perform detailed competitive intelligence analysis by fetching data from {combined_response}"

    notes = f"Analysis should be elaborate in nature and should present statistics and latest data. Only focus on developments between {past_date_str} to {curr_date_str}. Do not use old articles and data. &\
            Analyse their data and prepare the output accordingly. Include visuals for better understanding. Briefly cite sources for information. &\
            Tailor content for manager level audience. &\
            Ensure information adheres to ethical and legal boundaries."

    notes2 = f"Output should be in following layout: &\
          Headline: Key Insights for the Fortnight of {past_date_str} to {curr_date_str} &\
          Introduction: Briefly welcome readers and introduce the purpose of the newsletter. &\
          Provide date, source info name and source url for each item in the body. &\
          Body: &\
          Competitive Landscape Overview: Mention key industry trends and developments while expanding upon the basis of the article in depth. Leave two lines space after each section.&\
          Competitor Spotlight: A few lines related to any recent developments for major competitors. Try including as many points as possible. &\
          Recent News & Announcements: Highlight significant news, launches, partnerships, or campaigns throughout the industry. Try including as many points as possible. &\
          Financial Performance & Market Share: Analyze data on competition's financial performance and Industry market share shifts. Try including as many points as possible. &\
          Strategic Moves & Insights: Identify potential strategic moves by competitors and analyze their impact on {client} business. Try including as many points as possible. &\
          Actionable Insights: Provide key takeaways for {client} company to maintain a competitive edge. Try including as many points as possible. &\
          Conclusion: Encourage feedback and next edition information. &\
          Design the output in a beautiful format using san serif font. Word count 1500 words - 2000 words."

    final_prompt = f"{objective}\n{analysis}\n{analysis_RSS}\n{notes}\n{notes2}"
    final_response = generate_content(final_prompt, generation_config2)
    if final_response is None:
        st.stop()

    st.write(final_response)
    response_text = final_response

    response_without_asterisks = response_text.replace('*', '')
    generate_pdf(response_without_asterisks)
