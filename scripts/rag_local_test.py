from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def rag_local_test():
    embeddings = BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0", region_name="us-east-1"
    )
    docs = [
        Document(page_content = "Urgência CRÍTICA: prazo de resposta até 4 horas."),
        Document(page_content="Cartão de crédito: estorno provisório em até 48h."),
    ]

    vectorstore = FAISS.from_documents(docs, embeddings)
    results = vectorstore.similarity_search("prazo para fraude no cartão", k=1)
    print(results[0].page_content)