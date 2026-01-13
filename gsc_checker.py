import streamlit as st
import requests

# Replace this with your actual Make Webhook URL
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/86v6dhdxc6sc00up9cmjd8nqoypa1gpk"

st.title("Send URL to Make Webhook")

user_url = st.text_input("Enter the URL to send:")

if st.button("Send to Make"):
    if user_url:
        payload = {"url": user_url}
        try:
            response = requests.post(MAKE_WEBHOOK_URL, json=payload)
            if response.status_code == 200:
                st.success("URL successfully sent to Make!")
            else:
                st.error(f"Failed to send. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a URL before submitting.")
