import streamlit as st
import requests
from streamlit_pdf_viewer import pdf_viewer

st.title("Query PDF Using AI")
st.write("Upload a PDF file")

if 'pdf_ref' not in st.session_state:
    st.session_state.pdf_ref = None

if 'pdf_content' not in st.session_state:
    st.session_state.pdf_content = None

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key='pdf')

if uploaded_file:
    st.session_state.pdf_ref = uploaded_file  
     
if st.session_state.pdf_ref:
    if st.button("VIEW PDF"):
        with st.spinner('Processing...'):
            binary_data = st.session_state.pdf_ref.getvalue()
            pdf_viewer(input=binary_data, width=700)
             
if uploaded_file:
    st.write("You can now query the PDF content")
    user_query = st.text_input("Enter your query")

 
              
    if st.button("GET ANSWER"):
        with st.spinner('Processing...'):
                    try: 
                        if st.session_state.pdf_ref:
                            files = {'file': st.session_state.pdf_ref}
                            upload_response = requests.post("http://127.0.0.1:8000/uploadfile/", files=files)
                    
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
                        
                        response = requests.post("http://127.0.0.1:8000/query/", json=payload)
                        
                        if response.status_code == 200:
                            answer = response.json().get('answer', 'No answer found.')
                            st.write("Answer:")
                            st.write(answer)
                        else:
                            st.write("Error Occured")
                    except Exception as e:
                        st.error(f"Failed to get the answer: {e}")            
                              


     

    
