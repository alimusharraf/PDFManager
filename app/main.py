import streamlit as st
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from core.service import DocumentServices

from db.database import init_db
init_db()

service = DocumentServices()

if "search_result" not in st.session_state:
    st.session_state["search_result"] = []
    
if "selected_doc" not in st.session_state:
    st.session_state["selected_doc"] = 0
    
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 0
    
if "reader_mode" not in st.session_state:
    st.session_state["reader_mode"] = False

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
    st.header("Search & View")
    col = st.columns(2)
    with col[0]:
        search_tag = st.text_input("Search by Tags")
    with col[1]:
        search_date = st.date_input("Search by Date", value=None)
        
    if st.button("Search"):
        st.session_state.search_result = service.search_documents(
            tag = search_tag if search_tag else None,
            date = str(search_date) if search_date else None)
        
    results = st.session_state.search_result
    
    if results and not st.session_state.reader_mode:
        st.subheader(f"Result: {len(results)} Documents")
        container = st.container(height=500)
        
        with container:
            for doc in results:
                col1,col2 = st.columns([1,3])
                
                with col1:
                    st.image(doc.thumbnail_path,width=150)
                
                with col2:
                    st.write(f"Name: {doc.name}")
                    st.write(f"Tags: {doc.tags}")
                    st.write(f"Description: {doc.description}")
                    st.write(f"Lecture_date: {doc.lecture_date}")
                    if st.button("open",key=f"open_{doc.id}"):
                        st.session_state["selected_doc"] = doc
                        st.session_state["current_page"]  = 0
                        st.session_state["reader_mode"] = True
                        st.rerun()

    if st.session_state.reader_mode and st.session_state.selected_doc:
        doc = st.session_state.selected_doc
        st.subheader(f"Reading Document: {doc.name}")
        image_dir = doc.path.replace(".pdf","")
        
        st.write(f"Image Dir: {image_dir}")
        st.write("Files:", os.listdir(image_dir) if os.path.exists(image_dir) else "NOT FOUND")
        
        if not os.path.exists(image_dir):
            st.error("Image Not Found. PDF conversion Failed.")
        
        else:
            images = sorted(os.listdir(image_dir))
            total_page = doc.total_page
            st.write(total_page)
            current_page = st.session_state.current_page
            
            col1,col2,col3 = st.columns([6,5,1])
            
            with col1:
                if st.button("⬅️Previous") and current_page > 0:
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col2:
                st.subheader(current_page)
            
            with col3:
                if st.button("Next ➡️") and current_page < total_page-1:
                    st.session_state.current_page += 1
                    st.rerun()
            
            image_path = os.path.join(image_dir,images[st.session_state.current_page])
            st.image(image_path, width = "stretch")
        
        
with tabs[2]:
    #code of Analysis
    pass
