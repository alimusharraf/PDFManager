import streamlit as st
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from core.service import DocumentServices

from db.database import init_db
init_db()

service = DocumentServices()


st.set_page_config(
    page_title= "Document Manager",
    page_icon= "📃",
    layout= "wide"
)

st.title("PDF Manager")
st.divider()

tabs= st.tabs(["upload","Search and View", "Analysis"])

with tabs[0]:
    #Code of Upload
    st.header("Upload PDF")
    uploaded_document = st.file_uploader("Upload PDF",type="pdf")
    tags = st.text_input("tags (Comma Seperated)", type="search")
    description = st.text_area("Description")
    lecture_data = st.date_input("Lecture_Date (Optional)",value=None)
    if st.button("Save",type="primary"):
        if uploaded_document:
            service.upload_document(uploaded_document,tags,description,lecture_data)

with tabs[1]:
    #code of Search and view
    pass

with tabs[2]:
    #code of Analysis
    pass
