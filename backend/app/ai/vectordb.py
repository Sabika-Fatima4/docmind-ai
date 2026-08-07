import chromadb

client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection("documents")


def store_chunks(chunks, embeddings, document_id, filename):

    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    documents = [
        chunk["text"]
        for chunk in chunks
    ]

    metadatas = [
        {
            "document_id": document_id,
            "filename": filename,
            "page": chunk["page"],
            "chunk": i
        }
        for i, chunk in enumerate(chunks)
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search(query_embedding, document_id, n_results=3):

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        where={
            "document_id": document_id
        }
    )