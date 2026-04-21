import streamlit as st
import openai
import json

st.set_page_config(page_title="BrandIQ", page_icon="🎯", layout="centered")

st.markdown("""
<style>
.stApp { background-color: #0D1117; color: #E6EDF3; }
</style>
""", unsafe_allow_html=True)

openai.api_key = st.secrets["OPENAI_KEY"]

st.title("🎯 BrandIQ")
st.caption("Personal Brand Intelligence · Powered by GPT-4o Mini")

with st.form("brand_form"):
    experience = st.text_area("Experience Summary *", placeholder="e.g. 5+ years building ML systems...")
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Target Role *", placeholder="e.g. Senior ML Engineer")
    with col2:
        company = st.text_input("Target Company *", placeholder="e.g. Anthropic, Google")
    submitted = st.form_submit_button("Analyze My Brand →")
