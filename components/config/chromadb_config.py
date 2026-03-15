import chromadb

def ChromaDB(db_path, collection_name = "docx_info"):

    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_or_create_collection(collection_name)
    return collection