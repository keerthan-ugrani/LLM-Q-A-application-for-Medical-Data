"""
This module provides an login class that bundles all authentification methods
Author: Luke Voss
Email: luke.voss@stud.uni-heidelberg.de
Created: 12.01.2024
Last Updated: 03.03.2024
Version: 1.2.0

Requirements:
- Dotenv
"""

import os
from dotenv import load_dotenv, find_dotenv


class LoginCredentials:
    """
    This class bundles all authentification keys for improved app security
    """

    def __init__(self) -> None:
        load_dotenv(find_dotenv("./tokens.env"))
        self.weaviate_key = os.getenv("YOUR_WEAVIATE_KEY")
        self.weaviate_cluster = os.getenv("YOUR_WEAVIATE_CLUSTER")
        self.huggingface_key = os.getenv("HF_AUTH")
