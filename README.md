Conversational RAG with PDF Upload and Chat History
This is a Streamlit-based web application that allows users to upload PDF files, ask questions about their content, and maintain a conversation history. It uses a Retrieval-Augmented Generation (RAG) pipeline powered by LangChain, Groq, and Chroma to provide accurate and context-aware answers.
Features

PDF Upload: Upload one or more PDF files to extract and process their content.
Conversational Q&A: Ask questions about the PDFs, and the app retrieves relevant information to answer.
Chat History: Maintains conversation context, allowing follow-up questions to be understood in context.
Vector Search: Uses Chroma and HuggingFace embeddings for efficient document retrieval.
User-Friendly Interface: Built with Streamlit for an intuitive and interactive experience.
Customizable Sessions: Supports multiple conversation sessions via unique session IDs.

Tech Stack

Python: Core programming language.
Streamlit: Web app framework for the user interface.
LangChain: Orchestrates the RAG pipeline, including retrieval and history-aware question answering.
Groq: Provides the language model (Gemma2-9b-It) for generating answers.
Chroma: Vector database for storing and retrieving document embeddings.
HuggingFace BGE Embeddings: Converts text to numerical vectors for similarity search.
PyPDFLoader: Extracts text from PDF files.

Prerequisites
Before running the app, ensure you have:

Python 3.8 or higher installed.
A Groq API key (sign up at x.ai to obtain one).
Git installed for cloning the repository.
A virtual environment (recommended) to manage dependencies.

Installation

Clone the Repository:
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name


Set Up a Virtual Environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

If a requirements.txt file doesn't exist, install the required packages manually:
pip install streamlit langchain langchain-community langchain-groq chromadb sentence-transformers pypdf


Run the Application:
streamlit run app.py

Replace app.py with the name of your Python script (e.g., main.py if you renamed it).


Usage

Launch the App:

After running streamlit run app.py, the app opens in your default browser (usually at http://localhost:8501).


Enter Groq API Key:

Input your Groq API key in the provided text box (it’s hidden for security).


Set Session ID:

Enter a unique session ID (e.g., user1_session) or use the default (default_session) to track your conversation.


Upload PDFs:

Upload one or more PDF files using the file uploader.


Ask Questions:

Type your question about the PDF content in the text input field.
The app retrieves relevant document chunks and provides a concise answer.
View the conversation history in the expandable "Chat History" section.



Example

Uploaded PDF: A document about machine learning.
Question: "What is supervised learning?"
Response: "Supervised learning is a type of machine learning where the model is trained on labeled data, with input-output pairs, to predict outcomes for new data."
Follow-Up Question: "Can you give an example?"
Response: "An example of supervised learning is email spam detection, where the model learns from labeled emails (spam or not spam) to classify new emails."

Project Structure
your-repo-name/
├── app.py              # Main Streamlit app script
├── .gitignore          # Ignores virtual env, temporary files, etc.
├── README.md           # This file
└── requirements.txt    # (Optional) List of dependencies

Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Contact
For questions or feedback, feel free to open an issue on GitHub or contact your-email@example.com.

Built with ❤️ using Streamlit and LangChain.
