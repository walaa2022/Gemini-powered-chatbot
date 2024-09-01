import google.generativeai as genai
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
# Fetch the API key from environment variables
API_KEY = os.getenv("API_KEY")

genai.configure(api_key= "API_KEY")

# Check if API key is available
if not API_KEY:
    raise ValueError("API key not found. Please set it in the environment variables.")

# Configure the Generative AI client with the API key
genai.configure(api_key=API_KEY)

#model
model = genai.GenerativeModel("gemini-1.5-flash")

def get_chatbot_response(user_input):
    response = model.generate_content(user_input)
    return response.text

st.set_page_config(page_title="Simple Chatbot", layout='centered' )
st.title('Simple Chatbot')
st.write('POWERED BY GOOGLE GENERATIVE AI')

if 'history' not in st.session_state:
    st.session_state['history']=[]
    
for i, (user_message, bot_message) in enumerate(st.session_state.history):
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;">
        <div style="
            background-color: #d1d3e0;
            border-radius: 15px;
            padding: 10px 15px;
            max-width: 70%;
            text-align: right;">
            <p style="margin: 0; font-size: 16px; line-height: 1.5;">{user_message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bot message
    st.markdown(f"""
    <div style="
        display: flex;
        justify-content: flex-start;
        margin-bottom: 10px;">
        <div style="
            background-color: #e1ffc7;
            border-radius: 15px;
            padding: 10px 15px;
            max-width: 70%;
            text-align: left;">
            <p style="margin: 0; font-size: 16px; line-height: 1.5;">{bot_message}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)



with st.form(key='chat_form', clear_on_submit=True):
    user_input= st.text_input('', max_chars=2000)
    submit_button= st.form_submit_button('Send')
    
    if submit_button and user_input:
        with st.spinner('Thinking...'):
            response = get_chatbot_response(user_input)
        st.session_state.history.append((user_input, response))
        st.experimental_rerun()
    elif submit_button:
        st.warning('Please enter a message before sending.')

#user_input=input('enter your prompt')
#output = getchatbotresponse(user_input)
#print(output)