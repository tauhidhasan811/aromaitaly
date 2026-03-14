import chromadb

def ChromaDB(collection_name = "docx_info",
             db_path ="chroma_db"):

    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(collection_name)
    return collection