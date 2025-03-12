"""
This module introduces a class, that embedds a data.json file into Weaviate Cloud.
When executed this files uploads all data in datasets/data.json

Author: Luke Voss
Email: luke.voss@stud.uni-heidelberg.de
Created: 30.01.2024
Last Updated: 30.01.2024
Version: 1.0.0

Requirements:
- LangChain
- Pandas
- Weaviate
- dotenv
- Environment File tokens.env in folder 'env'
"""

import os

import pandas as pd
from dotenv import load_dotenv, find_dotenv
import weaviate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Weaviate

from .chunker import DocumentChunker


class WeaviateCloudEmbedder:
    """
    Embedds and uploads data to the Weaviate Cloud

    Sample Usage:
    embedder = WeaviateCloudEmbedder(YOUR_WEAVIATE_KEY, YOUR_WEAVIATE_CLUSTER)
    embedder.embed_data('./datasets/data_test.json')
    vectorstore = embedder.vectorstore
    """

    def __init__(
        self,
        weaviate_key,
        weaviate_cluster,
        embedding_model_name="BAAI/bge-small-en-v1.5",
        device="cuda",
    ):
        """
        Initialized the WeaviateCloudEmbedder class

        Args:
            weaviate_key (str): Our Weaviate API Key
            weaviate_cluster (str): Our Weaviate Cluster url
            embedding_model_name (str): Name of HuggingFaceEmbeddings model
            device (str): On which device embedding should be performed, either 'cuda' or 'cpu'
        """

        self.weaviate_key = weaviate_key
        self.weaviate_cluster = weaviate_cluster
        self.device = device
        self.client = self._initialize_client()
        self.embedding_model = self._initialize_embedding_model(embedding_model_name)
        self.vectorstore = None

    def embed_data(self, data_path="./datasets/data_test.json"):
        """Embeds data from the given path into the Cluster"""
        documents = self._get_chunked_data(data_path)
        self._initialize_vectorstore(documents)
        print("Stored all documents!")

    def _initialize_client(self):
        auth_config = weaviate.AuthApiKey(api_key=self.weaviate_key)
        self.client = weaviate.Client(
            url=self.weaviate_cluster,
            auth_client_secret=auth_config,
        )
        print("Successfully connected to Cluster!")
        return self.client

    def _initialize_embedding_model(self, embedding_model_name):
        return HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs={"device": self.device},
            encode_kwargs={"device": self.device, "batch_size": 32},
        )

    def _get_chunked_data(self, data_path):
        data = pd.read_json(data_path)
        chunker = DocumentChunker(chunk_size=100, chunk_overlap=50)
        return chunker.chunk(data)

    def _initialize_vectorstore(self, documents):
        self.vectorstore = Weaviate.from_documents(
            documents, self.embedding_model, client=self.client, by_text=False
        )


if __name__ == "__main__":
    load_dotenv(find_dotenv("./env/tokens.env"))
    YOUR_WEAVIATE_KEY = os.getenv("YOUR_WEAVIATE_KEY")
    YOUR_WEAVIATE_CLUSTER = os.getenv("YOUR_WEAVIATE_CLUSTER")

    embedder = WeaviateCloudEmbedder(YOUR_WEAVIATE_KEY, YOUR_WEAVIATE_CLUSTER)
    embedder.embed_data("./datasets/data_test.json")

    # Test
    query = "children with benign childhood epilepsy"
    docs = embedder.vectorstore.similarity_search_with_score(query, by_text=False)
    print(docs[0])
