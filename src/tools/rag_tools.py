from langchain.tools import tool
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient

@tool
def rag_tool(query: str) -> str:
    """Retrieve relevant documents from the RAG vector store based on the query. Use this tool to add the context so you can answer the user's question accurately.
    Args:
        query: The user's query string.
    """
    # Kết nối đến Qdrant vector store
    qdrant_client = QdrantClient(
        url="http://localhost:6333",
        prefer_grpc=False
    )

    # Khởi tạo Ollama Embeddings
    embeddings = OllamaEmbeddings(
        model="embeddinggemma:300m",
        # base_url="http://ollama:11434" # Sử dụng khi chạy trong Docker
    )

    # Tạo Qdrant Vector Store
    qdrant_vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name="stock_book",
        embedding=embeddings,
        retrieval_mode=RetrievalMode.DENSE,
    )
    # Truy vấn vector store để lấy các tài liệu liên quan
    relevant_docs  = qdrant_vector_store.similarity_search(query, k=10)
    result_contents = [doc.page_content for doc in relevant_docs]
    return "\n\n".join(result_contents)
    