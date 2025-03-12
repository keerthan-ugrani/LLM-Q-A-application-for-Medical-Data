import weaviate
from langchain.vectorstores.weaviate import Weaviate


class WeaviateInterface:
    """
    This class aims to act as a single contact point to Weaviate,
    increasing the modularity and mantainability of the code
    Sample Usage:
        weaviate = WeaviateInterface(authenticator)
        vectorstore = weaviate.connect_vectorstore(embed_model)
    """

    def __init__(self, authenticator) -> None:
        self.authenticator = authenticator
        self.client = self._init_client(self.authenticator)
        self.vectorstore = None

    def init_vectorstore(self, documents):
        """
        Create vectorstore from new documents
        Args:
            documents [List(LangChain Documents)]: List of prepared Langchain Documents
        """
        self.vectorstore = Weaviate.from_documents(
            documents, self.embedding_model, client=self.client, by_text=False
        )

    def connect_vectorstore(self, embed_model):
        """
        Connect to an existing vectorstore
        Arg:
            embed_model [Huggingface model]: Embedding model used for uploading the data
        Returns:
            vectorstore = Connected vectorstore
        """
        index_name = self.client.data_object.get()["objects"][0][
            "class"
        ]  # dynmaic Index name
        attributes = ["title", "authors", "pmid_id", "journal", "date"]

        self.vectorstore = Weaviate(
            self.client,
            index_name=index_name,
            embedding=embed_model,
            text_key="text",
            by_text=False,
            attributes=attributes,
        )
        return self.vectorstore

    def _init_client(self, authenticator):
        client = weaviate.Client(
            url=authenticator.weaviate_cluster,
            auth_client_secret=weaviate.auth.AuthApiKey(authenticator.weaviate_key),
        )
        return client
