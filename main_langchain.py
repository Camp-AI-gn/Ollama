import streamlit as st
from langchain_community.llms import Ollama
import requests
from bs4 import BeautifulSoup

# Initialize Ollama model
llm = Ollama(model="phi3")

# Function to generate response
def generate_response(question, document_text):
    full_text = f"{question}\n{document_text}" if document_text else question
    response = llm.invoke(full_text)
    return response

# Function to read text from the uploaded document
def read_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            document_text = uploaded_file.getvalue().decode("utf-8")
            return document_text
        elif uploaded_file.type == "application/pdf":
            # Logic to extract text from PDF
            # You can use PyPDF2, pdfminer.six, or any other library to extract text from PDF
            st.error("PDF support is not implemented yet.")
    return None

# Function to fetch text from a URL
def fetch_text_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Extract text from HTML
            text = "\n".join([p.get_text() for p in soup.find_all("p")])
            return text
        else:
            st.error("Failed to fetch content from URL. Please check the URL.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    return None

# Streamlit UI for chat interface
def chat_interface():
    st.title("Chatbot with Local Ollama Model")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input question from user
    prompt = st.text_input("What is up?")

    # Import document using slider in the sidebar
    document = None
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload a document", type=['txt', 'pdf'])
        url = st.text_input("Enter URL:")
        if url:
            document_text = fetch_text_from_url(url)
        else:
            document_text = read_uploaded_file(uploaded_file)

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response using local Ollama API
        answer_placeholder = st.empty()  # Placeholder for displaying the response
        
        with st.spinner("Assistant is typing..."):  # Show spinner while generating the response
            response = generate_response(prompt, document_text)
            answer_placeholder.markdown(response)
            
            # Ajouter la réponse de l'assistant à la liste des messages
            st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    chat_interface()

if __name__ == "__main__":
    main()
