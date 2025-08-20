import streamlit as st
import chromadb
from ollama import Client

# Chroma vorbereiten
chroma_client = chromadb.PersistentClient(path="chroma_db")
collection = chroma_client.get_or_create_collection(name="attention")

# Streamlit UI
st.set_page_config(page_title="...", page_icon="")
st.title("Bilal's Chatbot")

# Initialisiere Chatverlauf im Session State
#st.session_state speichert gesamte Session
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hallo 👋! Frag mich etwas ..."},
    ]

# Anzeige der bisherigen Chat-History
# st.chat_message(...) erzeugt ein Chat-Message-Element
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Eingabe-Feld für neue Nachricht
# :- Operator speichert Eingabe und prüft gleichzeitig
if user_query := st.chat_input("Deine Frage eingeben..."):
    # User-Nachricht speichern
    st.session_state["messages"].append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    # Dokumente aus Chroma holen
    results = collection.query(query_texts=[user_query], n_results=20)

    # System-Prompt mit bisherigen Nachrichten + Dokumenten
    chat_history = ""
    for m in st.session_state["messages"]:
        if m["role"] in ["user", "assistant"]:
            chat_history += f"{m['role'].capitalize()}: {m['content']}\n"

    system_prompt = f"""
    You are an expert assistant. You answer questions **only** based on the information 
    I am providing you. Do **not** make things up and do **not** use any outside knowledge. 
    If the answer is not in the data, tell it the user.

    Conversation so far:
    {chat_history}
    --------------------
    Data:
    {results['documents']}
    """

    #Connect your own LLM
    client = ...

    response = ...

    #response-Dictionary (Key-Value pair)
    answer = response["message"]["content"]

    # Antwort anzeigen + speichern
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state["messages"].append({"role": "assistant", "content": answer})

  
