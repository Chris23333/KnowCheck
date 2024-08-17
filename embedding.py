
from langchain_community.vectorstores.faiss import FAISS
# from langchain_chroma import Chroma

# from langchain_huggingface import HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain.retrievers import ContextualCompressionRetriever
from BCEmbedding.tools.langchain import BCERerank


from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever
import pickle
import os

# init embedding model
class Embedding():
    def __init__(self) -> None:
        self.embedding_model_name = 'maidalun1020/bce-embedding-base_v1'
        self.embedding_model_kwargs = {'device': 'cuda'}
        self.embedding_encode_kwargs = {'batch_size': 32, 'normalize_embeddings': True, 'show_progress_bar': False}

        self.embed_model = HuggingFaceEmbeddings(
                        model_name=self.embedding_model_name,
                        model_kwargs=self.embedding_model_kwargs,
                        encode_kwargs=self.embedding_encode_kwargs
                                            )

        self.reranker_args = {'model': 'maidalun1020/bce-reranker-base_v1', 'top_n': 8, 'device': 'cuda'}
        self.reranker = BCERerank(**self.reranker_args)

        # self.reranker_args2 = {'model': 'maidalun1020/bce-reranker-base_v1', 'top_n': 1, 'device': 'cuda'}
        # self.reranker2 = BCERerank(**self.reranker_args2)

        #retrieval with embedding and reranker
    def save_vs(self,save_path,texts) ->None:
        vs = FAISS.from_documents(texts, self.embed_model, distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT)
        vs.save_local(save_path)
    
    def load_vs(self,save_path):
        vector_store = FAISS.load_local(save_path,self.embed_model,distance_strategy=DistanceStrategy.MAX_INNER_PRODUCT)
        return vector_store

    def save_bm25_data(self,save_path,texts):
        data_path = os.path.join(save_path, 'bm25_str_data.pkl')
        with open(data_path, 'wb') as f:
            pickle.dump(texts, f)

    def load_bm25_data(self,save_path):
        data_path = os.path.join(save_path, 'bm25_str_data.pkl')
        with open(data_path, 'rb') as f:
            string_list = pickle.load(f)
        return string_list
    
    def retrieve(self,vs_path,query='')->list[str]:
        vs = self.load_vs(vs_path)
        string_list = self.load_bm25_data(vs_path)
        faiss_retriever = vs.as_retriever(search_type="similarity", search_kwargs={"score_threshold": 0.3, "k": 10})
        bm25_retriever = BM25Retriever.from_texts(string_list)
        bm25_retriever.k = 5
        
        retriever = EnsembleRetriever(retrievers=[bm25_retriever, faiss_retriever], weights=[0.5, 0.5])
        # compression_retriever1 = ContextualCompressionRetriever(base_compressor=self.reranker1, base_retriever=faiss_retriever)
        # compression_retriever2 = ContextualCompressionRetriever(base_compressor=self.reranker2, base_retriever=bm25_retriever)
        # response1 = compression_retriever1.get_relevant_documents(query) #-> List[Document]
        # response2 = compression_retriever2.get_relevant_documents(query) #-> List[Document]
        compression_retriever1 = ContextualCompressionRetriever(base_compressor=self.reranker, base_retriever=retriever)
        response1 = compression_retriever1.get_relevant_documents(query) #-> List[Document]
        return [res.page_content for res in response1]
        # return [res.page_content for res in response1]

# if __name__ == "__main__":
#     e = Embedding()
#     pdf
#     e.save_vs()