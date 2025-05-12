#importting Necessary Libraries
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import requests

load_dotenv()

# Set the Google API key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



#define the function to get the text from the pdf
def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()
    return  text


# Define the function to split the text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks



# Define the function to create the vector store
def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


#Define prompt template for the conversational chain
def get_conversational_chain():

    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-2.0-flash",
                             temperature=0.3)

    prompt = PromptTemplate(template = prompt_template, input_variables = ["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return chain


# Define the function to handle user input
def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    
    response = chain(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)

    print(response)
    st.write("Reply: ", response["output_text"])


# Define the main function to run the Streamlit app

import streamlit as st

def main():
    st.set_page_config(page_title="Chat PDF", page_icon="📄", layout="wide")

    # === MAIN PAGE ===
    st.markdown("<h1 style='text-align: center; color:#4B8BBE;'>💬 ChatPDF</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload multiple PDF files and chat with them intelligently using AI.</p>", unsafe_allow_html=True)
    st.divider()

    # Main Page PDF Upload
    st.subheader("📤 Upload Your PDF Files")
    with st.form(key="pdf_upload_form"):
        uploaded_files_main = st.file_uploader(
            "Drag and drop or browse to upload PDFs here",
            type=["pdf"],
            accept_multiple_files=True
        )
        submit_main = st.form_submit_button("🚀 Submit & Process")

    if submit_main:
        if uploaded_files_main:
            with st.spinner("⏳ Processing your documents..."):
                raw_text = get_pdf_text(uploaded_files_main)
                text_chunks = get_text_chunks(raw_text)
                get_vector_store(text_chunks)
                st.success("✅ PDFs processed successfully! You can now ask questions.")
        else:
            st.warning("⚠️ Please upload at least one PDF file.")

    # Question input
    st.subheader("💬 Ask a Question")
    with st.form("question_form", clear_on_submit=False):
        user_question = st.text_input("Type your question about the uploaded PDF(s):", placeholder="e.g., What is the summary of Chapter 2?")
        submit_qs = st.form_submit_button("💬 Generate Answer")

    if user_question:
        user_input(user_question)

    # Smart tagline at the bottom
    st.markdown("<p style='text-align: center; font-weight: bold; color: #888;'>✨ Smart. Fast. Context-aware.</p>", unsafe_allow_html=True)
  



  # GitHub user info
    github_username = "Faisalece18"  # Replace with your GitHub username
    github_api_url = f"https://api.github.com/users/{github_username}"

    try:
        response = requests.get(github_api_url)
        if response.status_code == 200:
            data = response.json()
            profile_img_url = data["avatar_url"]
            profile_name = data["name"] or github_username
        else:
            profile_img_url = None
            profile_name = github_username
    except:
        profile_img_url = None
        profile_name = github_username
    # Display at bottom of app
    st.markdown("---")
    if profile_img_url:
        st.markdown(
          f"""
          <div style="text-align: center;">
              <img src="{profile_img_url}" width="80" style="border-radius: 50%;" />
              <p>👨‍💻 Developed by <a href="https://github.com/{github_username}" target="_blank">{profile_name}</a></p>
          </div>
          """,
          unsafe_allow_html=True
        )
    else:
          st.markdown(f"<p style='text-align: center;'>👨‍💻 Developed by <a href='https://github.com/{github_username}' target='_blank'>{profile_name}</a></p>", unsafe_allow_html=True)

    st.markdown("---")

    # === SIDEBAR ===
    with st.sidebar:
        st.title("📂 Upload Menu")

        uploaded_files_sidebar = st.file_uploader(
            "📎 Upload PDF Files",
            type=["pdf"],
            accept_multiple_files=True,
            key="sidebar_uploader"
        )

        if st.button("🚀 Submit & Process"):
            if uploaded_files_sidebar:
                    with st.spinner("⏳ Processing your documents..."):
                        raw_text = get_pdf_text(uploaded_files_sidebar)
                        text_chunks = get_text_chunks(raw_text)
                        get_vector_store(text_chunks)
                        st.success("✅ PDFs processed successfully! You can now ask questions.")
            else:
                st.warning("⚠️ Please upload at least one PDF file.")

        st.markdown("---")
        st.title("📘 About This App")
        st.markdown("""
        **Welcome to ChatPDF 💁‍♂️**

        🚀 Upload one or more PDF files and interact with them instantly using the power of AI.

        💬 **Ask questions** about the documents — whether it's to extract specific details, summarize long content, or clarify complex information.

        📚 **Multi-PDF support** lets you upload several documents at once and chat across all of them as if you're talking to a knowledgeable assistant.

        🎯 Built for students, researchers, professionals, or anyone who wants fast, intelligent access to PDF content without manually reading through it.
        """)




if __name__ == "__main__":
    main()