from llama_index.core.schema import BaseNode, TransformComponent
from typing import List
import hashlib
from llama_index.core.ingestion import IngestionPipeline
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.core.text_splitter import SentenceSplitter
from llama_index.core import VectorStoreIndex
import faiss
import pickle
import os


class TextCleaner(TransformComponent):
    """
    Transformation to be used within the ingestion pipeline.
    Cleans clutters from texts.
    """
    def __call__(self, nodes, **kwargs) -> List[BaseNode]:
        
        for node in nodes:
            node.text = node.text.replace('\t', ' ') # Replace tabs with spaces
            node.text = node.text.replace(' \n', ' ') # Replace paragraph separator with spacaes
            
        return nodes
    

def hash_documents(documents):
    # combine all the texts into a single string
    all_titles = [doc.metadata['file_name'] for doc in documents]
    all_titles_distinct = list(set(all_titles))
    all_titles_distinct.sort()
    all_titles_str = " ".join(all_titles_distinct)
    # return a hash of the combined text which will stay consistent if the text is the same across multiple runs
    return hashlib.md5(all_titles_str.encode('utf-8')).hexdigest()


def load_or_create_vector_store(documents, embed_dim, chunk_size, chunk_overlap, cache_dir, vector_store_path, hash_path):
    os.makedirs(cache_dir, exist_ok=True)
    
    current_hash = hash_documents(documents)
    
    if os.path.exists(hash_path) and os.path.exists(vector_store_path):
        with open(hash_path, 'r') as f:
            stored_hash = f.read().strip()

        if stored_hash == current_hash:
            print("Loading vector store from cache...")
            with open(vector_store_path, 'rb') as f:
                return pickle.load(f)
    
    print("Creating new vector store...")
    faiss_index = faiss.IndexFlatL2(embed_dim)
    vector_store = FaissVectorStore(faiss_index=faiss_index)
    
    text_splitter = SentenceSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    pipeline = IngestionPipeline(
        transformations=[
            TextCleaner(),
            text_splitter,
        ],
        vector_store=vector_store,
    )
    
    nodes = pipeline.run(documents=documents)
    vector_store_index = VectorStoreIndex(nodes)
    
    # Save the new vector store and hash
    with open(vector_store_path, 'wb') as f:
        pickle.dump(vector_store_index, f)
    
    with open(hash_path, 'w') as f:
        f.write(current_hash)
    
    return vector_store_index