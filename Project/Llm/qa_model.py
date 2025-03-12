"""
This Python module facilitates interaction with Weaviate, Hugging Face, and LangChain libraries to perform semantic similarity searches on PubMed article snippets and generate answers to user questions using Hugging Face language models.

Author: Henri Smidt
Email: finn.smidt@stud.uni-heidelberg.de
Created: 14.02.2024
Last Updated: 14.02.2024
Version: 1.0.0


Requirements:
- LangChain
- Pandas
"""

from operator import itemgetter
from typing import List


import torch
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)

from utils import LoginCredentials, WeaviateInterface, HuggingFaceInterface


class QAModel:
    def __init__(self, model_id="meta-llama/Llama-2-13b-chat-hf") -> None:
        authenticator = LoginCredentials()
        weaviate = WeaviateInterface(authenticator)
        huggingface = HuggingFaceInterface(
            authenticator,
            embedding_model_name="BAAI/bge-small-en-v1.5",
            device=self._get_best_device(),
        )  # Priorises Cuda. If Cuda Memory too small choose cpu.
        self.vectorstore = weaviate.connect_vectorstore(
            embed_model=huggingface.embed_model
        )
        self.pipeline = huggingface.init_pipeline(model_id)
        self.prompt = self._init_chat_prompt_template()
        self.chain = self._init_chain()

    def ask(self, user_question):
        return self.chain.invoke(user_question)

    def _init_chain(self):
        format_docs_runnable = itemgetter(
            "docs") | RunnableLambda(self._format_docs)
        answer = self.prompt | self.pipeline | StrOutputParser()
        self.chain = (
            RunnableParallel(
                question=RunnablePassthrough(),
                docs=self.vectorstore.as_retriever(search_kwargs={"k": 3}),
            )
            .assign(context=format_docs_runnable)
            .assign(answer=answer)
            .pick(["answer", "docs"])
        )
        return self.chain

    def _init_chat_prompt_template(self):
        system_message = (
            "You're a helpful AI assistant. Given a user question and some pubmed article snippets, answer the user question "
            "using only the information contained in the article snippets. Important: Name the title of the article snippet "
            "you used to generate the answer. If none of the articles answer the question, just say you don't know.\n\n"
            "Here are the pubmed articles:{context}"
        )

        human_message = "{question}"

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", human_message),
            ]
        )
        return prompt

    def _format_docs(self, docs: List[Document]) -> str:
        """Convert Documents with Title to a single string."""
        formatted = [
            f"Article Title: {doc.metadata['title']}\nArticle Snippet: {doc.page_content}"
            for doc in docs
        ]
        return "\n\n" + "\n\n".join(formatted)

    def _get_best_device(self):
        """
        Returns the best available device for computation based on the system configuration.

        Returns:
            torch.device: The selected device for computation.
        """
        if torch.cuda.is_available():
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            return torch.device("mps")
        else:
            return torch.device("cpu")


def main():
    user_question = "This is a Dummy Question"

    llm_model = QAModel()
    answer = llm_model.ask(user_question)
    print(answer)


if __name__ == "__main__":
    main()
