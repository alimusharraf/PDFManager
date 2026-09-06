import streamlit as st
import sys
import os
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from core.service import DocumentServices
from core.analytics import AnalyticsServices

from db.database import init_db
init_db()

load_dotenv(os.path.join(BASE_DIR,".env"))
PASSWORD = os.getenv("ADMIN_PASSWORD")

service = DocumentServices()
analytics = AnalyticsServices()

if "search_result" not in st.session_state:
    st.session_state["search_result"] = []
    
if "selected_doc" not in st.session_state:
    st.session_state["selected_doc"] = 0
    
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 0

if "last_read_page_mode" not in st.session_state:
     st.session_state["last_read_page_mode"] = False
    
if "reader_mode" not in st.session_state:
    st.session_state["reader_mode"] = False
    
if "show_reset" not in st.session_state:
    st.session_state["show_reset"] = False
    
    

st.set_page_config(
    page_title= "Document Manager",
    page_icon= "📃",
    layout= "wide"
)

st.title("PDF Manager")
st.divider()

st.subheader("🔑 Admin Access & Control 🔐")
if st.button("Delete All Data",type="primary"):
    st.session_state.show_reset = True

if st.session_state.show_reset:
    password = st.text_input("Enter the password :",type="password")
    
    if st.button("Confirm Reset"):
        if password == PASSWORD:
            
            import shutil
            
            #delete Database
            db_dir = os.path.join("data","documents.db")
            if os.path.exists(db_dir):
                os.remove(db_dir)
                
            #delete Storgae
            pdf_dir = os.path.join("storage","pdfs")
            thumbnail_dir = os.path.join("storage","thumbnail")
            shutil.rmtree(pdf_dir, ignore_errors = True)
            shutil.rmtree(thumbnail_dir, ignore_errors = True)
            
            os.mkdir(pdf_dir)
            os.mkdir(thumbnail_dir)
            st.success("All data deleted Sucessfully.")
            st.session_state["show_reset"] = False
            st.rerun()
    
        else:
            st.error("Incorrect Password")

            

tabs= st.tabs(["upload","Search and View", "Analysis"])

with tabs[0]:
    #Code of Upload
    st.header("Upload PDF")
    uploaded_document = st.file_uploader("Upload PDF",type="pdf")
    tags = st.text_input("tags (Comma Seperated)", type="search")
    description = st.text_area("Description")
    lecture_data = st.date_input("Lecture_Date (Optional)",value=None)
    if st.button("Upload",type="primary"):
        analytics.add_app_visit("upload_click")
        if uploaded_document:
            service.upload_document(uploaded_document,tags,description,lecture_data)
            st.success("Pdf uploded sucessfully")
    

with tabs[1]:
    #code of Search and view
    st.header("Search & View")
    col = st.columns(2)
    with col[0]:
        search_tag = st.text_input("Search by Tags")
    with col[1]:
        search_date = st.date_input("Search by Date", value=None)
        
    if st.button("Search"):
        analytics.add_app_visit("search_click")
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
                        analytics.add_app_visit("open_pdf_click")
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
            
            last_read_page = service.get_last_read_page(doc.id)
            
            if  last_read_page == None:
                service.add_last_read_page(doc.id,st.session_state.current_page)
                
            if last_read_page != None:
                last_page = last_read_page
                
                if st.session_state.last_read_page_mode == False:
                    st.session_state.last_read_page_mode = True
                    st.session_state.current_page = last_page
                
    
            
            current_page = st.session_state.current_page
            
            col1,col2,col3 = st.columns([6,5,1])
            
            with col1:
                if st.button("⬅️Previous") and st.session_state.current_page > 0:
                    analytics.add_app_visit("previous_page_click")
                    st.session_state.current_page -= 1
                    st.rerun()
            
            with col2:
                st.subheader(f"{current_page+1}")
            
            with col3:
                if st.button("Next ➡️") and st.session_state.current_page < total_page-1:
                    analytics.add_app_visit("next_page_click")
                    st.session_state.current_page += 1
                    st.rerun()
            
            image_path = os.path.join(image_dir,images[st.session_state.current_page])
            st.image(image_path, width = "stretch")
            
            progress = (st.session_state.current_page+1)/total_page
            progress_percentage = progress * 100
            st.subheader("Progress")
            st.progress(progress)
            st.write(f"{progress_percentage:.2f}% ({st.session_state.current_page+1}/{total_page}).")
            
        if st.button("Close"):
            analytics.add_app_visit("close_pdf_click")
            st.session_state["reader_mode"] = False
            st.session_state.last_read_page_mode = False
            service.add_last_read_page(doc.id,st.session_state.current_page)
            st.rerun()
            
        
        
        
with tabs[2]:
    #code of Analysis
    st.header("Analytics")
    
    if st.button("🔄️ Reset Analytics"):
        analytics.delete_analytics()
        st.success("Reset Analytics Sucessful")
    
    st.subheader("App Usage")
    
    data = analytics.get_app_visit()
    
    import pandas as pd
    
    df = pd.DataFrame(data, columns=["event","count"])
    
    if df.empty:
        st.info("No Analytics Data yet, Perform some action to see insights.")
    else:
        st.bar_chart(df.set_index("event"))
        
    st.subheader("Progress")
    
    docs = service.get_all_documents()
    
    data1 = []
    
    for doc in docs:
        last_read = service.get_last_read_page(doc.id)
        if not last_read:
            last_read = 0
        progress = ((last_read + 1) / doc.total_page) * 100 if doc.total_page else 0
        
        data1.append({
            "Document": doc.name,
            "Pages Read": last_read+1,
            "Total Pages": doc.total_page,
            "Progress (%)": round(progress,2)
        })
    
    df_docs = pd.DataFrame(data1)
    
    st.dataframe(df_docs, width = "stretch")
