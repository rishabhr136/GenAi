import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import os
os.environ['GOOGLE_API_KEY'] = "AIzaSyD4EKdGbVxYnB9Ua5GqqTxzQC-ETohzBIA"
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-1.5-flash')
chat = model.start_chat(history=[])
def get_gemini_res(question):
    res = chat.send_message(question, stream= True)
    return res
st.set_page_config("Q&A session")
st.header("Gemini LLM Application")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history']=[]
input = st.text_input("input:",key= 'input')
submit = st.button("Ask the question")
if submit and input:
    response = get_gemini_res(input)
    st.session_state['chat_history'].append(("You",input))
    st.subheader("The Response is......")
    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('Rishabh',chunk.text))

st.subheader("The chat history is:")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")