import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def prepare_rag():
    # Define the directory containing the text files and the persistent directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    books_dir = os.path.join(current_dir, "knowledge-bank")
    db_dir = os.path.join(current_dir, "knowledge-bank/db")
    persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata")

    print(f"Books directory: {books_dir}")
    print(f"Persistent directory: {persistent_directory}")

    # Check if the Chroma vector store already exists
    if not os.path.exists(persistent_directory):
        print("Persistent directory does not exist. Initializing vector store...")

        # Ensure the books directory exists
        if not os.path.exists(books_dir):
            raise FileNotFoundError(
                f"The directory {books_dir} does not exist. Please check the path."
            )

        # List all text files in the directory
        book_files = [f for f in os.listdir(books_dir) if f.endswith(".txt")]

        # Read the text content from each file and store it with metadata
        documents = []
        for book_file in book_files:
            file_path = os.path.join(books_dir, book_file)
            loader = TextLoader(file_path)
            book_docs = loader.load()
            for doc in book_docs:
                # Add metadata to each document indicating its source
                doc.metadata = {"source": book_file}
                documents.append(doc)

        # Split the documents into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)

        # Display information about the split documents
        print("\n--- Document Chunks Information ---")
        print(f"Number of document chunks: {len(docs)}")

        # Create embeddings
        print("\n--- Creating embeddings ---")
        embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"
        )  # Update to a valid embedding model if needed
        print("\n--- Finished creating embeddings ---")

        # Create the vector store and persist it
        print("\n--- Creating and persisting vector store ---")
        db = Chroma.from_documents(
            docs, embeddings, persist_directory=persistent_directory)
        print("\n--- Finished creating and persisting vector store ---")

    else:
        print("Vector store already exists. No need to initialize.")

def call_rag(query: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    books_dir = os.path.join(current_dir, "knowledge-bank")
    db_dir = os.path.join(current_dir, "knowledge-bank/db")
    persistent_directory = os.path.join(db_dir, "chroma_db_with_metadata")

    """Call the RAG agent with the given query."""
    # Create a new agent executor with the web search tool
    # Define the embedding model
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    # Load the existing vector store with the embedding function
    db = Chroma(persist_directory=persistent_directory,
            embedding_function=embeddings)

    # Retrieve relevant documents based on the query
    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3},
    )
    relevant_docs = retriever.invoke(query)

    # Display the relevant results with metadata
    print("\n--- Relevant Documents ---")
    for i, doc in enumerate(relevant_docs, 1):
        print(f"Document {i}:\n{doc.page_content}\n")
        print(f"Source: {doc.metadata['source']}\n")

    # Combine the query and the relevant document contents
    combined_input = (
        "Here are some documents that might help answer the question: "
        + query
        + "\n\nRelevant Documents:\n"
        + "\n\n".join([doc.page_content for doc in relevant_docs])
        + "\n\nSources:\n"
        + "\n\n".join([doc.metadata["source"] for doc in relevant_docs])
        + "\n\nPlease provide a rough answer based only on the provided documents. "
        + "If the answer is not found in the documents, respond with 'I'm not sure'."
        + "Please also print the list of documents used.\n\n"
    )
    return combined_input