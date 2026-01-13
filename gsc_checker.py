import streamlit as st
import requests
import pandas as pd

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
                try:
                    st.session_state.response_data = response.json()
                except:
                    st.session_state.response_data = response.text
            else:
                st.error(f"Failed to send. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a URL before submitting.")

if 'response_data' in st.session_state and st.session_state.response_data:
    st.write("Webhook response data:")
    
    # Convert JSON to DataFrame for table display
    try:
        data = st.session_state.response_data
        
        # Handle different JSON structures
        if isinstance(data, list):
            # If it's a list of objects, convert directly
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            # If it's a single object, wrap it in a list
            df = pd.DataFrame([data])
        else:
            # Fallback: show as JSON if it's not a list or dict
            st.json(data)
            df = None
        
        if df is not None:
            st.dataframe(df, use_container_width=True)
            # Optionally also show as a static table
            # st.table(df)
    except Exception as e:
        # If conversion fails, fall back to JSON display
        st.json(st.session_state.response_data)
        st.warning(f"Could not convert to table: {e}")
