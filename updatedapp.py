from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import streamlit as st
from PyPDF2 import PdfReader
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

# Set the Google API key
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

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
    return vector_store


#Define prompt template for the conversational chain
def get_conversation_chain(vector_store):
    #llm = ChatOpenAI()
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash",temperature=0.3)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vector_store.as_retriever(),
        memory=memory
    )
    return conversation_chain


# Define the function to handle user input
def handle_userinput(user_question):
    if st.session_state.conversation is None:
        st.warning("Please upload and process PDFs first.")
        return

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.markdown(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.markdown(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)



# Define the main function to run the Streamlit app

import streamlit as st

def main():

    st.set_page_config(page_title="Chat PDF", page_icon="📄", layout="wide")
    st.write(css, unsafe_allow_html=True)

    # === MAIN PAGE HEADER ===
    st.markdown("<h1 style='text-align: center; color:#4B8BBE;'>📚 ChatPDF</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Upload multiple PDF files and chat with them intelligently using AI.</p>", unsafe_allow_html=True)
    st.divider()

    # === SESSION STATE INITIALIZATION ===
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    # === MAIN PDF UPLOAD SECTION ===
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
                vector_store = get_vector_store(text_chunks)
                st.session_state.conversation = get_conversation_chain(vector_store)
                st.success("✅ PDFs processed successfully! You can now ask questions.")
        else:
            st.warning("⚠️ Please upload at least one PDF file.")

    # === QUESTION INPUT SECTION ===
    st.subheader("💬 Ask a Question")
    with st.form("question_form", clear_on_submit=False):
        user_question = st.text_input("Type your question about the uploaded PDF(s):", placeholder="e.g., What is the summary of Chapter 2?")
        submit_qs = st.form_submit_button("💬 Generate Answer")

    if submit_qs and user_question:
        handle_userinput(user_question)

    # === TAGLINE FOOTER ===
    st.markdown("<p style='text-align: center; font-weight: bold; color: #888;'>✨ Smart. Fast. Context-aware.</p>", unsafe_allow_html=True)

    # === SIDEBAR SECTION ===
    with st.sidebar:
        st.title("📂 Upload Menu")

        pdf_docs = st.file_uploader(
            "📎 Upload PDF Files",
            type=["pdf"],
            accept_multiple_files=True,
            key="sidebar_uploader"
        )

        if st.button("🚀 Submit & Process", key="sidebar_process_btn"):
            if pdf_docs:
                with st.spinner("⏳ Processing your documents..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    vector_store = get_vector_store(text_chunks)
                    st.session_state.conversation = get_conversation_chain(vector_store)
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

    # === FOOTER GITHUB SECTION ===
    github_username = "Faisalece18"
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


if __name__ == "__main__":
       main()