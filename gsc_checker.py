import streamlit as st
import requests
import pandas as pd

# Replace this with your actual Make Webhook URL
MAKE_WEBHOOK_URL = "https://hook.eu2.make.com/86v6dhdxc6sc00up9cmjd8nqoypa1gpk"

st.title("GSC Quick Checker")

user_url = st.text_input("Enter the URL to send:")

if st.button("Send"):
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
    
    # Convert JSON to DataFrame for table display (items as rows)
    try:
        data = st.session_state.response_data
        
        # Handle different JSON structures
        if isinstance(data, list):
            # If it's a list of objects, process each one
            all_rows = []
            for item in data:
                if isinstance(item, dict):
                    for key, value in item.items():
                        all_rows.append({"Attribute": key, "Value": value})
            df = pd.DataFrame(all_rows)
        elif isinstance(data, dict):
            # Convert dict to rows: each key-value pair becomes a row
            rows = [{"Attribute": key, "Value": value} for key, value in data.items()]
            df = pd.DataFrame(rows)
        else:
            # Fallback: show as JSON if it's not a list or dict
            st.json(data)
            df = None
        
        if df is not None:
            st.dataframe(df, use_container_width=True, hide_index=True)
    except Exception as e:
        # If conversion fails, fall back to JSON display
        st.json(st.session_state.response_data)
        st.warning(f"Could not convert to table: {e}")
