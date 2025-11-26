import requests
import json
import chromadb
from chromadb.config import DEFAULT_TENANT, DEFAULT_DATABASE, Settings

class Chromadb_Worker():
    def __init__(self):
        """Initialization of LLAMA"""
        self.client = chromadb.HttpClient(
            host="100.111.62.92",
            port=8000,
            ssl=False,
            headers=None,
            settings=Settings(),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE
            )
    def heartbeat(self):
        return self.client.heartbeat()

if __name__ == "__main__":
    c = Chromadb_Worker()
    print(c.heartbeat())
