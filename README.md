# ChatbotWithRAG
This project is a Chatbot using RAG (Retrieval-Augmented Generation).

Setup Instructions:

First, connect your own LLM to run the chatbot.

Run fill_db.py to create a Chroma vector database. This will generate a file in the db folder where all vectors are stored.

After setting up the database, you can run UIChatbot.py, which provides a web-based user interface to interact with the chatbot.

Note: Place any files you want the chatbot to reference for answering questions in the data folder. These files will be used by the RAG system to generate context-aware responses.
