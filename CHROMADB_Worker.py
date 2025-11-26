import requests
import json
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings
from LLAMA_Worker import Llama_Worker

class Chromadb_Worker():
    def __init__(self,console):
        """Initialization of Chromadb Worker"""
        self.console = console
        self.http_client = chromadb.HttpClient(
            host="100.111.62.92",
            port=8000,
            ssl=False,
            headers=None,
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE
            )
       
    def generate_embeddings(self):
        lw = Llama_Worker(self.console,model="embeddinggemma")
    def heartbeat(self):
        return self.http_client.heartbeat()

if __name__ == "__main__":
    c = Chromadb_Worker()
    print(c.heartbeat())
