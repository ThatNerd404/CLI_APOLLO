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
# TODO: Make this file not need to use console at all. remember the yield word


class Llama_Worker():
    def __init__(self,console, model="mistral:7b", embedding_model="embeddinggemma"):
        """Initialization of LLAMA"""
        self.chat_url = "http://100.111.62.92:11434/api/chat"
        self.pull_url = "http://100.111.62.92:11434/api/pull"
        self.list_models_url = "http://100.111.62.92:11434/api/ps"
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
            self.messages = messages
            payload = {
                "model":self.model,
                "messages":self.messages,
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
    def pull_model(self, new_model, status):
        try:
            self.status = status
            self.new_model = new_model
            payload = {
                "model": self.new_model}

            response = requests.post(self.pull_url, json=payload, timeout=30)
            response.raise_for_status()
            self.status.stop()
            self.console.print(f"Model: {self.new_model} loaded successfully!")
            return self.new_model

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
    def swap_model(self, model, status):

        self.model = model
        self.status = status
        payload = {
                        "model": self.model,
                        "keep_alive":-1
            }

        try:
            preload = requests.post(self.chat_url,json=payload, timeout=30)
            preload.raise_for_status()
            self.status.stop()
            self.console.print(f"Current loaded model: {self.model}")
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

    def list_model(self, status):
        try: 
            self.status = status
            response = requests.get(self.list_models_url, timeout=30)
            response.raise_for_status()
            self.status.stop()
            model_list = []
            data = response.json()
            return data["models"][0]["model"]

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


