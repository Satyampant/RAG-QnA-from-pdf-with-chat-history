import streamlit as st
from langchain.chains import create_retrieval_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.vectorstores import Chroma
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
import tempfile
import os

# UI Setup
st.title("🧠 Conversational RAG with PDF Upload and Chat History")
st.write("Upload PDF files and ask questions about them. The assistant remembers your conversation.")

# API Key Input
api_key = st.text_input("🔑 Enter your Groq API Key", type="password")

# Initialize session store
if 'store' not in st.session_state:
    st.session_state.store = {}

if api_key:
    llm = ChatGroq(api_key=api_key, model="Gemma2-9b-It")  

    session_id = st.text_input("🪪 Session ID", value="default_session")

    uploaded_files = st.file_uploader("📄 Upload PDF files", type="pdf", accept_multiple_files=True)

    if uploaded_files:
        all_docs = []
        for file in uploaded_files:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(file.read())
                loader = PyPDFLoader(temp_file.name)
                docs = loader.load()
                all_docs.extend(docs)

        # Split and embed documents
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(all_docs)

        embeddings = HuggingFaceBgeEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
        retriever = vectorstore.as_retriever()

        # Prompts
        contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "Given the chat history and the latest user question, rewrite the question so it stands alone without needing the history. If it's already standalone, return it as-is."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", 
             "You are an assistant answering questions using the following context:\n\n{context}\n\n"
             "Keep answers concise. If unsure, say you don't know."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])

        # Build RAG chain
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
        qa_chain = create_stuff_documents_chain(llm, qa_prompt)
        rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

        # Chat history manager
        def get_session_history(session: str) -> BaseChatMessageHistory:
            if session not in st.session_state.store:
                st.session_state.store[session] = ChatMessageHistory()
            return st.session_state.store[session]

        conversational_rag_chain = RunnableWithMessageHistory(
            rag_chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
            output_messages_key="answer"
        )

        user_question = st.text_input("❓ Ask your question:")

        if user_question:
            response = conversational_rag_chain.invoke(
                {"input": user_question},
                config={"configurable": {"session_id": session_id}}
            )

            st.markdown("### 🤖 Assistant's Answer")
            st.success(response["answer"])

            with st.expander("🧾 Chat History"):
                history = get_session_history(session_id)
                for msg in history.messages:
                    st.markdown(f"**{msg.type.capitalize()}**: {msg.content}")

else:
    st.warning("Please enter your Groq API key to continue.")
