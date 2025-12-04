
import os
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def main():
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    qdrant_url = os.getenv("QDRANT_URL", "http://localhost:6333")
    pdf_file = os.getenv("PDF_FILE", "stock_book.pdf")
    
    print(f"📁 Loading PDF: {pdf_file}")
    print(f"🤖 Ollama URL: {ollama_url}")
    print(f"🗄️  Qdrant URL: {qdrant_url}")
    
    if not os.path.exists(pdf_file):
        print(f"Error: {pdf_file} not found!")
        return
    
    try:
        # Load PDF
        print("\n Loading PDF documents...")
        loader = PyPDFLoader(pdf_file)
        documents = loader.load()
        print(f"✅ Loaded {len(documents)} documents")
        
        # Split text
        print("\n2️⃣ Splitting documents...")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        print(f"Created {len(texts)} chunks")
        
        # Create embeddings
        print("\n Loading embedding model...")
        embeddings = OllamaEmbeddings(
            model="embeddinggemma:300m",
            base_url=ollama_url
        )
        print("\n Embedding model loaded")
        
        # Create Qdrant vector store
        print("\n Creating Qdrant vector store...")
        qdrant = QdrantVectorStore.from_documents(
            documents=texts,
            embedding=embeddings,
            url=qdrant_url,
            prefer_grpc=False,
            collection_name="stock_book"
        )
        print("Qdrant vector store created!")
        
        print("\n" + "="*60)
        print("🎉 Ingest completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during ingest: {str(e)}")
        raise

if __name__ == "__main__":
    main()