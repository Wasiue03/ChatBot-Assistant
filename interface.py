import streamlit as st
import requests

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

st.title("Chatbot Interface")

# Input field
user_input = st.text_input("Enter Command:")

# Button to send request
if st.button("Send"):
    if user_input:
        payload = {"input": user_input}
        response = requests.post(f"{BACKEND_URL}/chatbot", json=payload)
        response_data = response.json()
        st.write(response_data.get('message', response_data.get('summary', "No response")))

# Button to check server status
if st.button("Check Server"):
    try:
        response = requests.get(f"{BACKEND_URL}/ping")
        if response.status_code == 200:
            st.success("Server is running")
        else:
            st.error("Server not reachable")
    except requests.exceptions.ConnectionError:
        st.error("Server not reachable")
