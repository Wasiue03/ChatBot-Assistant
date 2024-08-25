import streamlit as st
import requests

# Define the FastAPI server URL
api_url = "http://127.0.0.1:8000/chatbot"

# Streamlit UI
st.title("Chatbot Interface")
st.write("Enter your query below:")

user_input = st.text_input("Your query")

if st.button("Send"):
    # Prepare the payload based on the user input
    if user_input.startswith("open youtube"):
        payload = {"input": user_input}
    elif user_input.startswith("search for"):
        payload = {"input": user_input}
    elif user_input.startswith("summarize"):
        article = st.text_area("Article to summarize", "Default long article text here")
        payload = {"input": "summarize", "article": article}
    else:
        payload = {"input": user_input}

    # Send request to FastAPI server
    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()
        result = response.json()
        st.write("Response:", result)
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
