"""
This module provides an Huggingface interface class that handles all contact point to Huggingface

Author: Luke Voss & Henri Smidt
Email: luke.voss@stud.uni-heidelberg.de & finn.smidt@uni-heidelberg.de
Created: 12.01.2024
Last Updated: 03.03.2024
Version: 1.2.0

Requirements:
- Transformers
- Torch
- LangChain
"""

import torch
from torch import bfloat16
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline


class HuggingFaceInterface:
    """
    This class aims to act as a single contact point to Huggingface,
    increasing the modularity and mantainability of the code

    Sample Usage:
        huggingface = HuggingFaceInterface(authenticator)
        pipeline = huggingface.init_pipeline(model_id="mistralai/Mistral-7B-v0.1")
    """

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

    def init_pipeline(self, model_id):
        """
        Initialized a HuggingFace pipeline with the given model
        """
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

    def _initialize_embedding_model(self, embedding_model_name):
        self.embed_model = HuggingFaceEmbeddings(
            model_name=embedding_model_name,
            model_kwargs=self.model_kwargs,
            encode_kwargs=self.encode_kwargs,
        )
        return self.embed_model
