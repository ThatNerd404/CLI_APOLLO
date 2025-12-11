import os
import requests
import json
import sys
from requests.exceptions import Timeout, HTTPError, RequestException
from ollama_exceptions import (
    OllamaConnectionError, 
    OllamaTimeoutError, 
    OllamaHTTPError, 
    OllamaNetworkError,
    OllamaModelNotFoundError
)


class Llama_Worker():
    def __init__(self,console, model="mistral:7b", embedding_model="embeddinggemma"):
        """Initialization of LLAMA"""
        self.chat_url = "http://100.111.62.92:11434/api/chat"
        self.pull_url = "http://100.111.62.92:11434/api/pull"
        self.running_model_url = "http://100.111.62.92:11434/api/ps"
        self.list_models_url = "http://100.111.62.92:11434/api/tags"
        self.generate_embeddings_url = "http://100.111.62.92:11434/api/embed"

        self.model = model
        self.embedding_model = embedding_model
        self.console = console

    def preload_model(self):
        try:
            payload = {
                    "model": self.model,
                    "keep_alive":-1,
                    "stream":True}
            preload = requests.post(self.chat_url,json=payload, timeout=30)
            preload.raise_for_status()

        except HTTPError as e:
            if e.response.status_code == 404:
                raise OllamaModelNotFoundError(f"Model '{self.model}' not found in Ollama")
            else:
                raise OllamaHTTPError(e.response.status_code, str(e))

        except ConnectionError:
            raise OllamaConnectionError("Failed to connect to Ollama server. Ensure Ollama server is online and try again.")

        except Timeout:
            raise OllamaTimeoutError("Connection to Ollama server timed out. Ensure Ollama server is online and try again.")

        except KeyboardInterrupt:
            raise

        except RequestException as e:
            raise OllamaNetworkError(f"Network error occurred: {e}")

        except Exception as e:
            raise Exception(f"Error: Unexpected error occured during initialization: {e}\n Restart Ollama server and try again.")

    def generate_response(self,messages):
        try:
            payload = {
                "model":self.model,
                "messages": messages,
                "keep_alive": -1,
                "stream":True}

            response = requests.post(self.chat_url, json=payload, stream=True, timeout=30)
            response.raise_for_status()

            for line in response.iter_lines():
                data = json.loads(line.decode("utf-8"))
                yield data["message"]["content"]

        except HTTPError as e:
            if e.response.status_code == 404:
                raise OllamaModelNotFoundError(f"Model '{self.model}' not found in Ollama")
            else:
                raise OllamaHTTPError(e.response.status_code, str(e))

        except ConnectionError:
            raise OllamaConnectionError("Failed to connect to Ollama server. Ensure Ollama server is online and try again.")

        except Timeout:
            raise OllamaTimeoutError("Connection to Ollama server timed out. Ensure Ollama server is online and try again.")

        except KeyboardInterrupt:
            raise

        except RequestException as e:
            raise OllamaNetworkError(f"Network error occurred: {e}")

        except Exception as e:
            raise
    def pull_model(self, new_model):
        try:
            self.new_model = new_model
            payload = {
                "model": self.new_model}

            response = requests.post(self.pull_url, json=payload, timeout=30)
            response.raise_for_status()
            return self.new_model

        except HTTPError as e:
            if e.response.status_code == 404:
                raise OllamaModelNotFoundError(f"Model '{self.new_model}' not found in Ollama")
            else:
                raise OllamaHTTPError(e.response.status_code, str(e))

        except ConnectionError:
            raise OllamaConnectionError("Failed to connect to Ollama server. Ensure Ollama server is online and try again.")

        except Timeout:
            raise OllamaTimeoutError("Connection to Ollama server timed out. Ensure Ollama server is online and try again.")

        except KeyboardInterrupt:
            raise

        except RequestException as e:
            raise OllamaNetworkError(f"Network error occurred: {e}")

        except Exception as e:
            raise

    def swap_model(self, model):
        try:
            self.model = model
            payload = {
                        "model": self.model,
                        "keep_alive":-1
            }

            preload = requests.post(self.chat_url,json=payload, timeout=30)
            preload.raise_for_status()

            return self.model

        except HTTPError as e:
            if e.response.status_code == 404:
                raise OllamaModelNotFoundError(f"Model '{self.model}' not found in Ollama")
            else:
                raise OllamaHTTPError(e.response.status_code, str(e))

        except ConnectionError:
            raise OllamaConnectionError("Failed to connect to Ollama server. Ensure Ollama server is online and try again.")

        except Timeout:
            raise OllamaTimeoutError("Connection to Ollama server timed out. Ensure Ollama server is online and try again.")

        except KeyboardInterrupt:
            raise

        except RequestException as e:
            raise OllamaNetworkError(f"Network error occurred: {e}")

        except Exception as e:
            raise

    def list_model(self):
        try: 
            response = requests.get(self.running_model_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            running_model = data["models"][0]["model"]

            response = requests.get(self.list_models_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            stored_models = [item["name"] for item in data["models"]]
            return running_model, stored_models

        except HTTPError as e:
            if e.response.status_code == 404:
                raise OllamaModelNotFoundError(f"Model '{self.model}' not found in Ollama")
            else:
                raise OllamaHTTPError(e.response.status_code, str(e))

        except ConnectionError:
            raise OllamaConnectionError("Failed to connect to Ollama server. Ensure Ollama server is online and try again.")

        except Timeout:
            raise OllamaTimeoutError("Connection to Ollama server timed out. Ensure Ollama server is online and try again.")

        except KeyboardInterrupt:
            raise

        except RequestException as e:
            raise OllamaNetworkError(f"Network error occurred: {e}")

        except Exception as e:
            raise

    def generate_embeddings(self, input_text):
        try:
            payload = {
                "model": self.embedding_model,
                "input": input_text
            }
            response = requests.post(self.embedding_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            embeddings = data["embeddings"]
            return embeddings

        except HTTPError as e:
            if e.response.status_code == 404:
                raise OllamaModelNotFoundError(f"Model '{self.embedding_model}' not found in Ollama")
            else:
                raise OllamaHTTPError(e.response.status_code, str(e))

        except ConnectionError:
            raise OllamaConnectionError("Failed to connect to Ollama server. Ensure Ollama server is online and try again.")

        except Timeout:
            raise OllamaTimeoutError("Connection to Ollama server timed out. Ensure Ollama server is online and try again.")

        except KeyboardInterrupt:
            raise

        except RequestException as e:
            raise OllamaNetworkError(f"Network error occurred: {e}")

        except Exception as e:
            raise

