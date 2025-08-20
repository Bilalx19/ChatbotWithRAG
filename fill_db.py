from langchain_community.document_loaders import PyPDFDirectoryLoader #ermöglicht laden von PDF
from langchain_text_splitters import RecursiveCharacterTextSplitter # ermöglicht PDf in Chunks zu unterteilen
import chromadb

# festlegen der environment

DATA_PATH = r"C:\Users\MButt\Retrieval-Augmented-Generation\data" # Pfad der PDF Dateien
CHROMA_PATH = r"chroma_db" #Nutzen von Chroma Datenbank, um die gesamte History zu speichern

#erstellen eines Client, mit persistenen Datenbank
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

#existiert die Collection, wenn nicht vorhanden wird eine neue erstellt
collection = chroma_client.get_or_create_collection(name="attention") 

# alle PDF von Data-file laden
loader = PyPDFDirectoryLoader(DATA_PATH)

#liest alle ODF und wandelt in Text um, zusätzlich erhhält man Metadaten, um diese Später als Quelle angeben zu können
raw_pdf = loader.load()

#Festlegung der Konfiguration für unterteilen in Chunks (von LangChain)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300, #Chars
    chunk_overlap=100,
    length_function=len,
    is_separator_regex=False
)

#erstellen von Chunks
chunks = text_splitter.split_documents(raw_pdf)

#Variablen, die später in der DB gespeichert werden

documents = [] #enhält spä#ter den Text
metadata = []#entählt zusätzliche Information, z.B. die Quelle
ids = [] #eindeutige Kennung, damit jeder Chunk in der DB wiedergefunden werden kann 

i = 0

#Iteration über Chunks, füllt alle drei Variablen oben auf, die später in die DB gespeichert werden
for chunk in chunks:
    documents.append(chunk.page_content)
    ids.append("ID"+str(i))
    metadata.append(chunk.metadata)
    i += 1

# hinzufügen von Daten in DB
collection.upsert(
    documents=documents,
    metadatas=metadata,
    ids=ids
)