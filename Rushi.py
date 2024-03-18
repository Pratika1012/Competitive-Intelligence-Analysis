import streamlit as st
import pandas as pd
import google.generativeai as genai
from datetime import datetime, timedelta
import base64
from fpdf import FPDF
import google.generativeai as genai
from datetime import datetime, timedelta
from io import BytesIO
import pdfkit

st.set_page_config(layout="wide")

# Configure Google Generative AI
gemini_api_key = "AIzaSyAGxhWaMKBEnFXfhGeQWWvq92rE5JtkTIw"
genai.configure(api_key=gemini_api_key)

# Define Generative Models
generation_config = {
  "temperature": 0,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4096,
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

generation_config2 = {
  "temperature": 0.6,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 4096,
}

def generate_pdf(response_text):
    # Create a PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add the response_text to the PDF document
    pdf.multi_cell(0, 10, response_text)

    # Save the PDF document to a BytesIO object
    pdf_buffer = pdf.output(dest='S').encode('latin1')
    b64_pdf = base64.b64encode(pdf_buffer).decode()

    # Provide a download link for the generated PDF
    href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="Generated_Analysis.pdf">Download PDF</a>'
    st.markdown(href, unsafe_allow_html=True)


model2 = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config2)
challenge = "RSS Feeds for Competitive Intelligence and Summarization"
objective = "Stay ahead of competitors by monitoring industry trends"
analysis = "Competitive Intelligence Analysis"
# Streamlit UI
st.markdown("<h1 style='text-align: center;'>Competitive Intelligence Analysis</h1>", unsafe_allow_html=True)

st.sidebar.header("ITC")
industry = st.sidebar.text_input("Industry Name","Pharmaceutical")
market = st.sidebar.text_input("Market/Geography Name", "United States")
client = st.sidebar.text_input("Client Name", "Astrazeneca")
curr_date = st.sidebar.date_input("Fortnight End Date ", format="DD/MM/YYYY")

if st.sidebar.button("Generate Analysis"):
    # Convert date string to date object
    # date_format = "%d-%m-%y"
    # date_object = datetime.strptime(current_date, date_format)
    # curr_date = date_object.date()
    days_to_subtract = timedelta(days=15)
    past_date = curr_date - days_to_subtract
    # desired_format = "%d-%m-%Y"
    # curr_date = curr_date.strftime(desired_format)
    # past_date = past_date.strftime(desired_format)

    # Generate content using Generative Models
    # competitor_list = f"For {industry} industry, {market} market, {client} client, give a list of competitors."
    # prompt_parts = [competitor_list]
    # response_comp = model.generate_content(prompt_parts)

    # RSS_feed1 = f"For {industry} industry, {market} market, compile a list of relevant RSS feed URLs."
    # RSS_feed2 = f"For {industry} industry, {market} market, {client} client and {response_comp.text} competitors, compile a list of relevant RSS feed URLs."
    
    # prompt_parts = ["Competitive Intelligence Analysis", "Stay ahead of competitors by monitoring industry trends", RSS_feed1]
    # response1 = model.generate_content(prompt_parts)

    # prompt_parts = ["Competitive Intelligence Analysis", "Stay ahead of competitors by monitoring industry trends", RSS_feed2]
    # response2 = model.generate_content(prompt_parts)

    # prompt_parts = ["Combine two responses.", response1.text, response2.text]
    # final_response = model.generate_content(prompt_parts)

    # st.subheader("Generated Competitive Intelligence Analysis")
    # st.write(final_response.text)

# st.markdown(footer, unsafe_allow_html=True)
    
    company_info = f"Summarize company information {client}"

    competitor_list = f"For {industry} industry, {market} market, {client} client, give a list of competitors."

    prompt_parts = [competitor_list]
    response_comp = model.generate_content(prompt_parts)

    RSS_feed1 = f"For {industry} industry, {market} market, compile a list of relevant RSS feed URLs."
    RSS_feed2 = f"For {industry} industry, {market} market, {client} client and {response_comp.text} competitors, compile a list of relevant RSS feed URLs."

    prompt_parts = [analysis,objective,RSS_feed1]
    response1 = model.generate_content(prompt_parts)

    prompt_parts = [analysis,objective,RSS_feed2]
    response2 = model.generate_content(prompt_parts)

    prompt_parts = ["Combine two responses.",response1.text,response2.text]
    response = model.generate_content(prompt_parts)

    #analysis = f"For {industry} industry in {market}, perform {analysis_model} analysis"
    analysis_RSS = f"For {client} client, {industry} industry, {market} market, perform detailed competitive intelligence analysis by fetching data from {response.text}"

    #notes2 = "Industry news and trending topics. Competitor news (i.e. financial reporting, new partnerships, mergers & acquisitions, and product announcements). Upcoming events, webinars, and conferences. Industry thought leadership pieces."
    notes = f"Analysis should be elaborate in nature and should present statistics and latest data. Only focus on developments between {past_date} to {curr_date}. Do not use old articles and data. &\
            Analyse their data and prepare the output accordingly. Include visuals for better understanding.  Briefly cite sources for information. &\
            Tailor content for manager level audience. &\
            Ensure information adheres to ethical and legal boundaries."

    notes2 = f"Output should be in following format: &\
            Headline: Competitive Edge: Key Insights for the Fortnight of {past_date} - {curr_date} &\
            Introduction: Briefly welcome readers and introduce the purpose  of the newsletter. &\
            Provide date, source info name and source url for each item in the body. &\
            Body: &\
            Competitive Landscape Overview: Summarize key industry trends and developments. &\
            Competitor Spotlight: A few lines related to any recent developments for major competitors. Try including as many points as possible. &\
            Recent News & Announcements: Highlight significant news, launches, partnerships, or campaigns throughout the industry. Try including as many points as possible. &\
            Financial Performance & Market Share: Analyze data on competition's financial performance and Industry market share shifts. Try including as many points as possible. &\
            Strategic Moves & Insights: Identify potential strategic moves by competitors and analyze their impact on {client} business. Try including as many points as possible. &\
            Actionable Insights: Provide key takeaways for {client} company to maintain a competitive edge. Try including as many points as possible. &\
            Conclusion: Encourage feedback and next edition information."

    prompt_parts = [objective,analysis,analysis_RSS,notes,notes2]
    response = model2.generate_content(prompt_parts)
    response_text=response.text
    st.write(response_text)
    
    response_without_asterisks = response_text.replace('*', '')
    generate_pdf(response_without_asterisks)

  


    

