import streamlit as st
import requests
from streamlit_pdf_viewer import pdf_viewer

st.title("ChatWithPDF")
 
if 'pdf_ref' not in st.session_state:
    st.session_state.pdf_ref = None

if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = None

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf", key='pdf')

if uploaded_file:
    st.session_state.pdf_ref = uploaded_file  
     
if st.session_state.pdf_ref:
    if st.button("VIEW PDF"):
        with st.spinner('Processing...'):
            binary_data = st.session_state.pdf_ref.getvalue()
            pdf_viewer(input=binary_data, width=700)
             
if uploaded_file:
    user_query = st.text_input("Enter Query")

              
    if st.button("GET ANSWER"):
        with st.spinner('Processing...'):
                    try: 
                        if st.session_state.pdf_ref:
                            files = {'file': st.session_state.pdf_ref}
                            upload_response = requests.post("https://pdf-ai-l6cm.onrender.com/uploadfile/", files=files)
                    
                        if upload_response.status_code == 200:
                            data = upload_response.json()
                            st.session_state.pdf_content = data['content']
                        else:
                            st.write("Please Upload File ...")
                            st.stop()
                        payload = {
                            'content': st.session_state.pdf_content,
                            'query': user_query
                        }
                        
                        response = requests.post("https://pdf-ai-l6cm.onrender.com/query/", json=payload)
                        
                        if response.status_code == 200:
                            answer = response.json().get('answer', 'No answer found.')
                            st.write("Answer:")
                            st.write(answer)
                        else:
                            st.write("Error Occured")
                    except Exception as e:
                        st.error(f"Failed to get the answer: {e}")            
                              


     

    
