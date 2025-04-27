import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000/cultura"

# Session State initialization
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "critique" not in st.session_state:
    st.session_state.critique = ""
if "rewritten_text" not in st.session_state:
    st.session_state.rewritten_text = ""

# page config
st.set_page_config(layout="wide")

# title config
st.title("CulturaSense - LingoGuard")

# left and right
left, right = st.columns([1.4, 2])

# ================= Left Column: Contents ====================
with left:
    st.header("Contents")

    text = st.text_area("Raw Copy", value=st.session_state.get("text", ""), height=250)
    image = st.file_uploader("Upload Image (Optional)", type=["png", "jpg", "jpeg"])
    pdf = st.file_uploader("Upload PDF (Optional)", type=["pdf"])
    metadata = st.text_area("Product Metadata (Optional)", value=st.session_state.get("metadata", ""))

    if not st.session_state.submitted:
        if st.button("Save and Analyze", key="submit_button"):
            st.session_state.text = text
            st.session_state.metadata = metadata
            payload = {
                "text": text,
                "image_path": None,
                "pdf_path": None,
                "country": st.session_state.get("country", "USA"),
                "language": st.session_state.get("language", "English(America)"),
                "platform": st.session_state.get("platform", "Shopee"),
                "age": st.session_state.get("age", 25),
                "gender": st.session_state.get("gender", "female"),
                "income_level": st.session_state.get("income_level", "middle"),
                "religion": st.session_state.get("religion", ""),
                "sensitive_contributors": st.session_state.get("sensitive_contributors", ""),
            }
            try:
                response = requests.post(BACKEND_URL, json=payload)
                if response.status_code == 200:
                    result = response.json()["result"]
                    st.session_state.critique = result["critique"]
                    st.session_state.rewritten_text = result["rewritten_text"]
                    st.session_state.submitted = True
                    st.rerun()
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
    else:
        if st.button("Start New Analysis", key="new_analysis_button"):
            st.session_state.submitted = False
            st.session_state.critique = ""
            st.session_state.rewritten_text = ""
            st.rerun()

# ================= Right Column: Target + Report ====================
with right:
    with st.expander("🎯 Target Segment Settings", expanded=not st.session_state.submitted):
        st.subheader("Target Settings")

        st.session_state.country = st.selectbox("Country/Region", [
            "Select a country...",
            "Afghanistan", "Albania", "Algeria", "Argentina", "Australia", "Austria", "Bangladesh",
            "Belgium", "Brazil", "Bulgaria", "Cambodia", "Canada", "Chile", "China", "Colombia",
            "Croatia", "Czech Republic", "Denmark", "Dominican Republic", "Egypt", "Estonia",
            "Finland", "France", "Germany", "Ghana", "Greece", "Hong Kong", "Hungary", "Iceland",
            "India", "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Japan", "Jordan",
            "Kazakhstan", "Kenya", "Kuwait", "Latvia", "Lebanon", "Lithuania", "Luxembourg",
            "Malaysia", "Mexico", "Morocco", "Myanmar", "Nepal", "Netherlands", "New Zealand",
            "Nigeria", "Norway", "Pakistan", "Peru", "Philippines", "Poland", "Portugal", "Qatar",
            "Romania", "Russia", "Saudi Arabia", "Serbia", "Singapore", "Slovakia", "Slovenia",
            "South Africa", "South Korea", "Spain", "Sri Lanka", "Sweden", "Switzerland", "Taiwan",
            "Thailand", "Tunisia", "Turkey", "Ukraine", "United Arab Emirates", "United Kingdom",
            "United States", "Uruguay", "Uzbekistan", "Venezuela", "Vietnam"], key="country_select")
        st.session_state.language = st.selectbox("Language", [
            "Select a language...",
            "Afrikaans", "Arabic", "Bengali", "Bulgarian", "Burmese", "Chinese", "Croatian",
            "Czech", "Danish", "Dutch", "English", "Estonian", "Filipino", "Finnish", "French",
            "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian",
            "Italian", "Japanese", "Kazakh", "Korean", "Latvian", "Lithuanian", "Malay",
            "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Romanian", "Russian",
            "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tamil", "Thai",
            "Turkish", "Ukrainian", "Urdu", "Uzbek", "Vietnamese"], key="language_select")
        st.session_state.platform = st.selectbox("Platform", ["Select a platform...", "Amazon", "Shopee", "Shopify", "TikTok", "Instagram"], key="platform_select")
        st.session_state.age = st.number_input("Age", min_value=0, max_value=100, value=25, step=1, key="age_input")
        st.session_state.gender = st.selectbox("Gender", ["Select a gender...","Female","Male","Other"], key="gender_select")
        st.session_state.income_level = st.selectbox("Income Level", ["Select a income level...", "Low Income","Lower-Middle Income","Middle Income","Upper-Middle Income","High Income","Affluent"], key="income_level_select")
        st.session_state.religion = st.text_input("Religion (Optional)", key="religion_input")
        st.session_state.sensitive_contributors = st.text_area("Sensitive Contributors (Optional)", key="sensitive_contributors_input")

    if st.session_state.submitted:
        st.header("📄 Report")
        st.subheader("Critique")
        st.markdown(f"<div style='background-color:#f9f9f9;padding:15px;border-radius:10px'>{st.session_state.critique}</div>", unsafe_allow_html=True)

        st.subheader("Rewritten Content")
        st.markdown(f"<div style='background-color:#f9f9f9;padding:15px;border-radius:10px'>{st.session_state.rewritten_text}</div>", unsafe_allow_html=True)

        st.download_button(
            label="Download Report (txt)",
            data=f"Critique:\n{st.session_state.critique}\n\nRewritten:\n{st.session_state.rewritten_text}",
            file_name="cultura_report.txt",
            mime="text/plain"
        )
