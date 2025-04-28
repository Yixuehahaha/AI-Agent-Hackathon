import streamlit as st
import requests
import markdown as md 
BACKEND_URL = "http://localhost:8000/cultura"

# Session State initialization
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "critique" not in st.session_state:
    st.session_state.critique = ""
if "rewritten_text" not in st.session_state:
    st.session_state.rewritten_text = ""
if "upload_key" not in st.session_state:
    st.session_state.upload_key = 0
if "form_key" not in st.session_state:
    st.session_state.form_key = 0

# page config
st.set_page_config(layout="wide")

# title config
st.title("CulturaSense - LingoGuard")
def render_card_with_markdown(raw_md: str, background_color: str = "#f9f9f9") -> None:
    html_body = md.markdown(
                            raw_md,
                            extensions=["sane_lists"])   
    text_color = "#2e7d32" if background_color == "#e8f5e9" else "#000000"
    
    html_body = md.markdown(raw_md, extensions=["sane_lists"])         
    card_html = f"""
    <div style="
        background-color:{background_color};
        padding:10px 20px;
        border-radius:0px;
        margin-bottom:0px;
        line-height:1.65;
        margin-left:20px;
        font-size:16px;
        margin-top: 0;
        color:{text_color};"> 
        {html_body}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
# left and right
left, right = st.columns([1.4, 2])


# ================= Left Column: Contents ====================
with left:
    st.header("Contents")

    text = st.text_area("Raw Copy", value=st.session_state.get("text", ""), height=250, key=f"raw_copy_{st.session_state.form_key}")
    image = st.file_uploader("Upload Image (Optional)", type=["png", "jpg", "jpeg"], key=f"file_uploader_{st.session_state.upload_key}")
    image_hint = st.text_input("Image content hint (Optional)", placeholder="e.g., 'couple hugging', 'woman in hijab'", key=f"image_hint_{st.session_state.form_key}")
    pdf = st.file_uploader("Upload PDF (Optional)", type=["pdf"], key=f"pdf_uploader_{st.session_state.upload_key}")
    metadata = st.text_area("Product Metadata (Optional)", value=st.session_state.get("metadata", ""), key=f"metadata_{st.session_state.form_key}")

    if not st.session_state.submitted:
        if st.button("Save and Analyze", key="submit_button"):
            st.session_state.text = text
            st.session_state.metadata = metadata
            # 1. data and files
            data = {
                "text": text,
                "country": st.session_state.get("country", "USA"),
                "language": st.session_state.get("language", "English(America)"),
                "platform": st.session_state.get("platform", "Shopee"),
                "age": st.session_state.get("age", 25),
                "gender": st.session_state.get("gender", "female"),
                "income_level": st.session_state.get("income_level", "middle"),
                "religion": st.session_state.get("religion", ""),
                "sensitive_contributors": st.session_state.get("sensitive_contributors", ""),
                "image_hint": image_hint,
                "metadata": metadata,
            }
            files = {} 
            if image:
                files["image_file"] = ("uploaded_image.png", image.getvalue(), "image/png")

            try:
                response = requests.post(BACKEND_URL, data=data, files=files)  #
                if response.status_code == 200:
                    result = response.json().get("result", {})

                    st.session_state.critique = result.get("critique", "No critique returned.")
                    st.session_state.rewritten_text = result.get("rewritten_text", "No rewritten text returned.")
                    st.session_state.image_analysis = result.get("image_analysis", "No image analysis found.")
                    st.session_state.submitted = True
                    st.rerun()
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")
    else:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Edit Analysis", key="edit_analysis_button"):
                st.session_state.submitted = False
                st.session_state.critique = ""
                st.session_state.rewritten_text = ""
                st.rerun()
        with col2:
            if st.button("Start New Analysis", key="clear_button"):
                for key in [
                    "text", "metadata", "image_analysis", "image", "pdf", "image_hint",
                    "country", "language", "platform", "age", "gender", "income_level",
                    "religion", "sensitive_contributors", "critique", "rewritten_text"
                ]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.session_state.submitted = False
                st.session_state.upload_key += 1
                st.session_state.form_key += 1
                st.rerun()


# ================= Right Column: Target + Report ====================
with right:
    with st.expander("Target Segment Settings", expanded=not st.session_state.submitted):
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
            "United States", "Uruguay", "Uzbekistan", "Venezuela", "Vietnam"], key=f"country_select_{st.session_state.form_key}")
        st.session_state.language = st.selectbox("Language", [
            "Select a language...",
            "Afrikaans", "Arabic", "Bengali", "Bulgarian", "Burmese", "Chinese", "Croatian",
            "Czech", "Danish", "Dutch", "English", "Estonian", "Filipino", "Finnish", "French",
            "German", "Greek", "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian",
            "Italian", "Japanese", "Kazakh", "Korean", "Latvian", "Lithuanian", "Malay",
            "Nepali", "Norwegian", "Persian", "Polish", "Portuguese", "Romanian", "Russian",
            "Serbian", "Slovak", "Slovenian", "Spanish", "Swahili", "Swedish", "Tamil", "Thai",
            "Turkish", "Ukrainian", "Urdu", "Uzbek", "Vietnamese"], key=f"language_select_{st.session_state.form_key}")
        st.session_state.platform = st.selectbox("Platform", ["Select a platform...", "Amazon", "Shopee", "Shopify", "TikTok", "Instagram"], key=f"platform_select_{st.session_state.form_key}")
        st.session_state.age = st.number_input("Age", min_value=0, max_value=100, value=25, step=1, key=f"age_input_{st.session_state.form_key}")
        st.session_state.gender = st.selectbox("Gender", ["Select a gender...","Female","Male","Other"], key=f"gender_select_{st.session_state.form_key}")
        st.session_state.income_level = st.selectbox("Income Level", ["Select a income level...", "Low Income","Lower-Middle Income","Middle Income","Upper-Middle Income","High Income","Affluent"], key=f"income_level_select_{st.session_state.form_key}")
        st.session_state.religion = st.text_input("Religion (Optional)", key=f"religion_input_{st.session_state.form_key}")
        st.session_state.sensitive_contributors = st.text_area("Sensitive Contributors (Optional)", key=f"sensitive_contributors_input_{st.session_state.form_key}")

    if st.session_state.submitted:

        st.header("Report")  
        full_critique = ""
        full_critique += f"** Text Critique:**\n\n{st.session_state.critique}"

        st.markdown("""<div style="padding-left:20px;">""", unsafe_allow_html=True)

        st.subheader("Critique")  

        sections = st.session_state.critique.split("### ")
        for section in sections:
            if not section.strip():
                continue
            if section.startswith("Copy Adjustment"):
                st.markdown('<h4 style="margin-left:20px; margin-bottom:8px;">Copy Adjustment</h4>', unsafe_allow_html=True)
                render_card_with_markdown(section.replace("Copy Adjustment", "").strip(), background_color="#ffffff")
            elif section.startswith("Word Choice Check"):
                st.markdown('<h4 style="margin-left:20px;margin-bottom:8px;">Word Choice Check</h4>', unsafe_allow_html=True)
                render_card_with_markdown(section.replace("Word Choice Check", "").strip(), background_color="#ffffff")
            elif section.startswith("Content Update"):
                st.markdown('<h4 style="margin-left:20px;margin-bottom:8px;">Content Update</h4>', unsafe_allow_html=True)
                render_card_with_markdown(section.replace("Content Update", "").strip(), background_color="#ffffff")
            elif section.startswith("Language Tone"):
                st.markdown('<h4 style="margin-left:20px;margin-bottom:8px;">Language Tone</h4>', unsafe_allow_html=True)
                render_card_with_markdown(section.replace("Language Tone", "").strip(), background_color="#ffffff")
            elif section.startswith("Image Suggestion"):
                st.markdown('<h4 style="margin-left:20px;margin-bottom:8px;">Image Suggestion</h4>', unsafe_allow_html=True)
                render_card_with_markdown(section.replace("Image Suggestion", "").strip(), background_color="#ffffff")
            elif section.startswith("Actionable Suggestions"):
                st.markdown("""
                <div style="background-color:#f5f5f5; padding:20px; margin-top:20px; margin-left:20px">
                    <h4 style="margin-bottom: 8px; ">Actionable Suggestions</h4>
                """, unsafe_allow_html=True)
                render_card_with_markdown(section.replace("Actionable Suggestions", "").strip(), background_color="#f5f5f5")
                st.markdown("</div>", unsafe_allow_html=True)
            elif section.startswith("Estimated CTR Impact and Risk Mitigation"):
                st.markdown("""
                <div style="background-color:#e8f5e9; padding:20px; margin-top:20px; margin-left:20px">
                <h4 style="color:#2e7d32;">Estimated CTR Impact and Risk Mitigation</h4>
                """, unsafe_allow_html=True)
                render_card_with_markdown(section.replace("Estimated CTR Impact and Risk Mitigation", "").strip(), background_color="#e8f5e9")
                st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background-color: #ffffff; padding:30px 30px; margin-top:20px; margin-bottom:30px; box-shadow:0px 2px 8px rgba(0,0,0,0.05);">
        """, unsafe_allow_html=True)

        st.header("Suggested Content")
        render_card_with_markdown(st.session_state.rewritten_text, background_color="#ffffff")

        st.markdown("</div>", unsafe_allow_html=True)

        # download
        st.download_button(
            label="Download Report",
            data=f"Critique:\n{full_critique}\n\nRewritten:\n{st.session_state.rewritten_text}",
            file_name="cultura_report.txt",
            mime="text/plain"
        )
