# 📚 ChatPDF with Gemini 💬

A powerful Streamlit web app that allows users to interact with their PDF documents. Upload multiple PDFs, ask complex questions, and get intelligent, context-aware answers — all in real-time.

---

## 🚀 Features

- 📎 **Multi-PDF Upload** – Upload one or many PDF files simultaneously  
- 💬 **Ask Anything** – Pose any question related to your documents   
- 🗂️ **Semantic Search** – Uses FAISS and embeddings to find relevant context  
- 🧩 **LangChain Integration** – Efficiently chains your input and context to the LLM  
- ⚡ **Fast & Responsive** – Real-time Q&A with a clean, modern UI  

---

## 🧪 Use Cases

- 📖 Summarize academic papers  
- 📝 Extract key info from contracts or legal docs  
- 📊 Analyze business or financial reports  
- 💼 Query employee handbooks or onboarding docs  

---

## 📸 App Preview
 
> Example:  
> ![App Screenshot](Images\img1.png)
> ![App Screenshot](Images\img2.png)

---

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [FAISS](https://github.com/facebookresearch/faiss)
- [PyPDF2](https://github.com/py-pdf/PyPDF2)
- Python 3.9+

---

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Faisalece18/chat-with-multiple-documents
cd chat-with-multiple-documents
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Configure API Key

### Option 1: Use `.env` File Locally

Create a `.env` file in your root directory and add:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

### Option 2: Add Secrets in Streamlit Cloud

Go to:

```
Settings → Secrets → Add Secret
```

Add:

```toml
GOOGLE_API_KEY = "your_google_api_key_here"
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 🙋‍♂️ About the Developer

**👨‍💻 Faisal**  
🎓 BSc in Electrical and Computer Engineering  
🔍 Passionate about NLP, Generative AI, and LLM-based tools  
📬 Connect on [GitHub](https://github.com/Faisalece18)

---

_“Turning documents into dialogue with the power of AI.”_
