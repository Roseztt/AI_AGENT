import argparse
import os
import shutil
from langchain_community.document_loaders import CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


CHROMA_PATH = "chroma"
DATA_PATH = "influxdb_export.csv"


def main():

    # Check if the database should be cleared (using the --clear flag).
    parser = argparse.ArgumentParser()
    parser.add_argument("--reset", action="store_true", help="Reset the database.")
    args = parser.parse_args()
    if args.reset:
        print("✨ Clearing Database")
        clear_database()

    # Create (or update) the data store.
    documents = load_documents()
    add_to_chroma(documents)


def load_documents():
    documents = []
    with open(DATA_PATH, 'r') as f:
        row_index = 0
        for line in f:
            content = line.strip()
            if content:
                metadata = {"source": DATA_PATH, "row": row_index}
                doc = Document(page_content=content, metadata=metadata)
                documents.append(doc)
                row_index += 1
    #document_loader = CSVLoader(DATA_PATH)
    return documents

"""
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=0,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

"""    

def get_embedding_function():
    embeddings= OllamaEmbeddings(model="mxbai-embed-large")
    return embeddings


def add_to_chroma(chunks: list[Document]):
    # Load the existing database.
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=get_embedding_function()
    )

    # Calculate Page IDs.
    chunks_with_ids = calculate_chunk_ids(chunks)

    # Add or Update the documents.
    existing_items = db.get(include=[])  # IDs are always included by default
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Only add documents that don't exist in the DB.
    new_chunks = []
    for chunk in chunks_with_ids:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
            
            

    if len(new_chunks):
        print(f"👉 Adding new documents: {len(new_chunks)}")
        new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
        db.add_documents(new_chunks, ids=new_chunk_ids)
        print('adding')

        for i, added_chunk in enumerate(new_chunks):
            # Print the index and the raw CSV line content
            # Using .get() for ID retrieval for robustness, minimal change
            print(f"Document {i+1} (ID: {added_chunk.metadata.get('id', 'N/A')}): {added_chunk.page_content}")
    else:
        print("✅ No new documents to add")


def calculate_chunk_ids(chunks):
    

    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        #page = chunk.metadata.get("page")
        #current_page_id = f"{source}:{page}"
        row = chunk.metadata.get("row")
        # If the page ID is the same as the last one, increment the index.
        chunk_id = f"{source}:{row}"
        """
        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        # Calculate the chunk ID.
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id
        """
        # Add it to the page meta-data.
        chunk.metadata["id"] = chunk_id

    return chunks


def clear_database():
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)


if __name__ == "__main__":
    main()