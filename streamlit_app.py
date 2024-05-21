import binascii
import streamlit_app as st
import requests
from streamlit_app import session_state as ss
from streamlit_pdf_viewer import pdf_viewer


st.title("Query PDF Using AI")
st.write("Upload a PDF file")
 
if 'pdf_ref' not in ss:
    ss.pdf_ref = None
    
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf",key='pdf')
   
if uploaded_file:
    ss.pdf_ref = uploaded_file  

if ss.pdf_ref:
    if st.button("Display PDF "):
        
        with st.spinner('Processing...'):
            binary_data = ss.pdf_ref.getvalue()
            pdf_viewer(input=binary_data, width=700)   
        
    if st.button("View PDF"):
        
            with st.spinner('Processing...'):
                try:
                    files = {'file': uploaded_file}
                    response = requests.post("http://127.0.0.1:8000/uploadfile", files=files)

                    if response.status_code == 200:
                        data = response.json()
                        st.text_area("PDF Content", data['content'], height=400)
                        ss.pdf_content = data['content']  
                    else:
                        st.error(f"Error: {response.status_code} - {response.json()['detail']}")
                except Exception as e:
                    st.error(f"Failed to process the file: {e}")    
    
    if 'pdf_content' in ss and ss.pdf_content:
        st.write("You can now query the PDF content")
        user_query = st.text_input("Enter your query")
        
        if st.button("Get Answer"):
            with st.spinner('Processing...'):
                try:
                    payload = {
                        'content': ss.pdf_content,
                        'query': user_query
                    }
                    response = requests.post("http://127.0.0.1:8000/query", json=payload)

                    if response.status_code == 200:
                        answer = response.json().get('answer', 'No answer found.')
                        st.write("Answer:")
                        st.write(answer)
                    else:
                        st.error(f"Error: {response.status_code} - {response.json()['detail']}")
                except Exception as e:
                    st.error(f"Failed to get the answer: {e}")