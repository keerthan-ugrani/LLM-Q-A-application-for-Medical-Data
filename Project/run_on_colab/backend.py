"""
This python module contains all relevant backend code and is provided for easier updload to Google Colab.

Author: Luke Voss & Henri Smidt
Email: luke.voss@stud.uni-heidelberg.de & finn.smidt@uni-heidelberg.de
Created: 26.02.2024
Last Updated: 03.03.2024
Version: 1.0.0

Requirements:
- App dependecies
"""

import os
from typing import List
from operator import itemgetter

from dotenv import load_dotenv, find_dotenv
import weaviate
import torch
from torch import bfloat16
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.vectorstores.weaviate import Weaviate
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import (
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)


class LoginCredentials:
    def __init__(self) -> None:
        load_dotenv(find_dotenv("tokens.env"))
        self.weaviate_key = os.getenv("YOUR_WEAVIATE_KEY")
        self.weaviate_cluster = os.getenv("YOUR_WEAVIATE_CLUSTER")
        self.huggingface_key = os.getenv("HF_AUTH")


class WeaviateInterface:
    def __init__(self, authenticator) -> None:
        self.authenticator = authenticator
        self.client = self._init_client(self.authenticator)
        self.vectorstore = None

    def init_vectorstore(self, documents):
        self.vectorstore = Weaviate.from_documents(
            documents, self.embedding_model, client=self.client, by_text=False
        )

    def connect_vectorstore(self, embed_model):
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


class HuggingFaceInterface:
    def __init__(
        self,
        authenticator,
        embedding_model_name="BAAI/bge-small-en-v1.5",
        device="cuda",
        batch_size=32,
    ) -> None:
        self.authenticator = authenticator
        self.device = device
        self.model_kwargs = {"device": device}
        self.encode_kwargs = {"device": device, "batch_size": batch_size}
        self.embedding_model = self._initialize_embedding_model(embedding_model_name)
        self.pipeline = None

    def _initialize_embedding_model(self, embedding_model_name):
        self.embed_model = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs,
        )
        return self.embed_model

    def init_pipeline(self, model_id):
        hf_auth = self.authenticator.huggingface_key
        tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_auth)

        if self.device == torch.device("cuda"):
            bits_and_bites_config = transformers.BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=bfloat16,
            )
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                trust_remote_code=True,
                quantization_config=bits_and_bites_config,
                device_map="auto",
                do_sample=True,
                token=hf_auth,
            )
        else:
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                trust_remote_code=True,
                device_map="auto",
                offload_folder="offload",
                offload_state_dict=True,
                load_in_8bit=True,
                do_sample=True,
                token=hf_auth,
            )

        model.eval()

        pipe = pipeline(
            task="text-generation",
            model=model,
            return_full_text=True,
            tokenizer=tokenizer,
            max_new_tokens=256,
            temperature=0.01,
            repetition_penalty=1.1,
        )

        self.pipeline = HuggingFacePipeline(pipeline=pipe)
        return self.pipeline


class QAModel:
    def __init__(self, model_id="mistralai/Mistral-7B-v0.1") -> None:
        # model_id = "meta-llama/Llama-2-7b-chat-hf" # smaller model^
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
        format_docs_runnable = itemgetter("docs") | RunnableLambda(self._format_docs)
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
