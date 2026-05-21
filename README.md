# Aromaitaly

## Description  
Aromaitaly is a FastAPI backend application designed to manage and process villa-related data using document uploads and AI-powered retrieval. It integrates custom modules for reading, chunking, embedding, and storing documents, as well as handling chat interactions and availability checks. The system uses OpenAI models and LangChain for natural language processing and retrieval-augmented generation. It supports villa data fetching from external APIs like Beds24, manages tokens for authentication, and stores processed data in a persistent ChromaDB instance. The project ensures environment consistency with Python 3.13 and includes tools for cleaning text, validating tokens, and deleting directories.

## Run Instructions  
1. Clone the repository:  
   `git clone <repo-url>`  
2. Create a virtual environment:  
   `py -3.13 -m venv venv`  
3. Activate the virtual environment:  
   - On Windows: `venv\Scripts\activate`  
   - On Unix/Mac: `source venv/bin/activate`  
4. Install dependencies:  
   `pip install -r requirements.txt`  
5. Run the important files:  
   - `python main.py`  
   - `python test.py`  

## Folder Structure  
```
aromaitaly
|-- .python-version
|-- main.py
|-- pyproject.toml
|-- README.md
|-- test.py
|-- uv.lock
|-- components
|   |-- __init__.py
|   |-- hyperparms.py
|   |-- asset
|       |-- avaiabality_tools.py
|       |-- beds24.py
|       |-- get_all_villa.py
|       |-- validate_token.py
|   |-- config
|       |-- agent.py
|       |-- chromadb_config.py
|       |-- embd_model.py
|       |-- openai_model.py
|   |-- core
|       |-- chunk_config.py
|       |-- clean_chunk_doc.py
|       |-- clean_text.py
|       |-- delete_path.py
|       |-- file_reader.py
|       |-- rag_prompt.py
|       |-- store_chunk.py
|       |-- wrapper.py
|-- db
|   |-- chroma_db
|       |-- ea8cc9b7-b138-4705-a08b-51ddb718fed0
|           |-- length.bin
|           |-- link_lists.bin
|-- schema
    |-- chat_model.py
```

## File Descriptions  

- **.python-version**  
  Specifies the Python version (3.13) for environment consistency.

- **main.py**  
  FastAPI backend application managing villa data, document uploads, AI retrieval, and chat interactions with OpenAI integration.

- **pyproject.toml**  
  Project metadata and dependencies including FastAPI, LangChain, and ChromaDB for API and NLP functionalities.

- **README.md**  
  Project documentation placeholder.

- **test.py**  
  Demonstrates initialization of user query and conversation history for dialogue management related to villa availability.

- **uv.lock**  
  Dependency lock file ensuring reproducible installs with pinned package versions for Python 3.13+.

- **components/__init__.py**  
  Marks `components` as a Python package enabling imports of its modules.

- **components/hyperparms.py**  
  Configuration dictionary for fetching and normalizing property data from an external API.

- **components/asset/avaiabality_tools.py**  
  LangChain tool to check room availability over date ranges, dynamically updating descriptions.

- **components/asset/beds24.py**  
  Class to fetch detailed villa data from Beds24 API using environment-stored credentials.

- **components/asset/get_all_villa.py**  
  Utilities and functions (partially commented) for retrieving and organizing villa property data.

- **components/asset/validate_token.py**  
  Retrieves and refreshes access tokens from an authentication API using stored refresh tokens.

- **components/config/agent.py**  
  Sets up a custom GPT-based agent with a RAG prompt, modular for enhanced retrieval and chat.

- **components/config/chromadb_config.py**  
  Initializes and returns a persistent ChromaDB client and document collection.

- **components/config/embd_model.py**  
  Loads and returns a SentenceTransformer embedding model for generating text embeddings.

- **components/config/openai_model.py**  
  Loads a ChatOpenAI model augmented with a custom availability checking tool.

- **components/core/chunk_config.py**  
  Splits large text into chunks for better processing using RecursiveCharacterTextSplitter.

- **components/core/clean_chunk_doc.py**  
  Formats retrieved documents and cleans villa data strings by removing special characters.

- **components/core/clean_text.py**  
  Cleans input text by decoding HTML entities, removing URLs and tags, normalizing whitespace.

- **components/core/delete_path.py**  
  Force deletes directories including read-only files with permission handling and garbage collection.

- **components/core/file_reader.py**  
  Reads and extracts text from DOCX and PDF files using python-docx and PyMuPDF.

- **components/core/rag_prompt.py**  
  Defines a RAG prompt for a customer support assistant tailored to villa booking and availability.

- **components/core/store_chunk.py**  
  Stores text chunks and embeddings into a ChromaDB collection with UUID identifiers.

- **components/core/wrapper.py**  
  Centralized document extraction based on file extension for PDF and DOCX files.

- **db/chroma_db/ea8cc9b7-b138-4705-a08b-51ddb718fed0/length.bin**  
  Serialized data caching villa listing metadata for faster retrieval.

- **db/chroma_db/ea8cc9b7-b138-4705-a08b-51ddb718fed0/link_lists.bin**  
  Serialized binary storing link/reference lists for ChromaDB entity relationships.

- **schema/chat_model.py**  
  Pydantic model `ChatBody` validating user query and previous conversation context inputs.