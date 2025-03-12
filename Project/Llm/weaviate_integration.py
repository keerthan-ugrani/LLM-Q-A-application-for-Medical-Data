"""
This Python module connects to Weaviate and enables dense vector retrieval.

Author: Henri Smidt
Email: finn.smidt@stud.uni-heidelberg.de
Created: 14.02.2024
Last Updated: 03.03.2024
Version: 1.0.0

Requirements:
- Weaviate
"""

import weaviate
from dotenv import load_dotenv, find_dotenv
import os
from langchain.vectorstores.weaviate import Weaviate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings


load_dotenv(find_dotenv("./env/tokens.env"))
WCS_API_KEY = os.getenv("YOUR_WEAVIATE_KEY")
WCS_CLUSTER_URL = os.getenv("YOUR_WEAVIATE_CLUSTER")

client = weaviate.Client(
    url=WCS_CLUSTER_URL,
    auth_client_secret=weaviate.auth.AuthApiKey(WCS_API_KEY),
)
device = "cpu"
embed_model = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": device},
    encode_kwargs={"device": device, "batch_size": 32},
)

vectorstore = Weaviate(
    client,
    index_name="LangChain_0c70358e34034236ba8f84cd318e2c7b",
    embedding=embed_model,
    text_key="text",
    by_text=False,
)
query = "children with benign childhood epilepsy"
docs = vectorstore.similarity_search_with_score(query)
print(docs[0])
