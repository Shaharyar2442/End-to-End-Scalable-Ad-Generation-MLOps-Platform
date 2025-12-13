# streamlit run src/app/frontend.py
import streamlit as st
import requests

# 1. Configuration
st.set_page_config(page_title="Ad Generator", page_icon="✨")
st.title("✨ AI Ad Creative Generator")
st.markdown("Enter your product details below to generate marketing copy.")

# 2. Sidebar for API URL (So you can switch between Local and Cloud)
with st.sidebar:
    st.header("Settings")
    # Default to your Azure IP. Replace with your actual IP!
    api_url = st.text_input("API URL", value="http://172.188.205.7/generate")

# 3. User Input Form
with st.form("ad_form"):
    product_name = st.text_input("Product Name", placeholder="e.g., Future Sneakers")
    description = st.text_area("Description", placeholder="e.g., Self-lacing, waterproof, neon lights.")
    submitted = st.form_submit_button("Generate Creative 🚀")

# 4. Handle Submission
if submitted:
    if not product_name or not description:
        st.warning("Please fill in all fields.")
    else:
        with st.spinner("AI is thinking..."):
            try:
                payload = {"product_name": product_name, "description": description}
                response = requests.post(api_url, json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("Ad Copy Generated!")
                    st.text_area("Result", value=data["ad_copy"], height=200)
                else:
                    st.error(f"Error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")