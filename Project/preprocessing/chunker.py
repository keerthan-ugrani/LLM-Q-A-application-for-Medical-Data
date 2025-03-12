"""
This module introduces a class, that chunks pandas dataframes and returns LangChain Documents

Author: Luke Voss
Email: luke.voss@stud.uni-heidelberg.de
Created: 25.01.2024
Last Updated: 25.01.2024
Version: 1.0.0

Requirements:
- LangChain
- TQMD
- Pandas
"""

from tqdm.auto import tqdm
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import SentenceTransformersTokenTextSplitter
from langchain.docstore.document import Document


class DocumentChunker:
    """
    A class for chunking text data in a Pandas DataFrame and creating LangChain Documents.

    Attributes:
        chunk_size (int): Size of each text chunk measured in characters!.
        chunk_overlap (int): Character overlap between text chunks.
        separators (list): List of separators for text splitting.
    """

    def __init__(self, chunk_size=100, chunk_overlap=50, separators=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", " ", ""]
        # OpenAi Tokenizer that measures number of tokens in chunk
        self.text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
        )
        # self.text_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0)(
        #     chunk_overlap=self.chunk_overlap,
        #     model_name='BAAI/bge-small-en-v1.5'
        # )

    def chunk(self, docs, progress_bar=True):
        """
        Processes all documents in the DataFrame and returns a DataFrame of chunks.

        Args:
            docs (pd.DataFrame): DataFrame containing the documents.
            progress_bar (bool): Whether to show a progress bar.

        Returns:
            List[Document]: List of Documents containing the processed chunks.
        """
        processed_chunks = []
        for row in tqdm(
            docs.itertuples(),
            total=len(docs),
            desc="Creating Documents",
            disable=not progress_bar,
        ):
            chunks = self._split_abstract_into_chunks(row)
            processed_chunks.extend(chunks)
        return processed_chunks

    def _split_abstract_into_chunks(self, row):
        """Splits the abstract text from a DataFrame row into chunks."""
        chunks = self.text_splitter.split_text(row.abstract)
        docs = []
        for i, chunk in enumerate(chunks):
            metadata = {
                "pmid_id": f"{row.pmid}-{i}",
                "title": row.title,
                "authors": row.authors,
                "date": row.date,
                "journal": row.journal,
                "abstract": chunk,
            }
            docs.append(Document(page_content=chunk, metadata=metadata))
        return docs


if __name__ == "__main__":
    docs = pd.read_json("./datasets/data.json")

    chunker = DocumentChunker(chunk_size=400, chunk_overlap=50)
    data = chunker.chunk(docs)
    print(data[0])

    # output_file_path = './datasets/data_chunked.json'
    # data.to_json(output_file_path, orient='records', lines=False, indent=4)
