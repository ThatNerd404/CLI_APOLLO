import os
import requests
import json
import sys
from requests.exceptions import Timeout, RequestException, HTTPError

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
        try:
            payload = {
                    "model": self.model,
                    "keep_alive":-1,
                    "stream":True}
            # empty request to preload the model
            preload = requests.post(self.chat_url,json=payload, timeout=300)
            preload.raise_for_status()

        except HTTPError:
            self.console.print("Error: Failed to connect to Ollama server. Ensure Ollama server is online and try again.", style="red bold")
            sys.exit(1)

        except requests.exceptions.ConnectionError:
            self.console.print("Error: Failed to connect to Ollama server. Ensure Ollama server is online and try again.", style="red bold")
            sys.exit(1)
        except Timeout:
            self.console.print("Error: Connection to Ollama server timed out. Ensure Ollama server is online and try again.", 
                             style="red bold")
            sys.exit(1)

        except RequestException as e:
            self.console.print(f"Error: Network error during initialization: {e}\n Restart Ollama server and try again.", 
                             style="red bold")
            sys.exit(1)

        except Exception as e:
            self.console.print(f"Error: Unexpected error occured during initialization: {e}\n Restart Ollama server and try again.", style="red bold")
            sys.exit(1)

    def generate_response(self,messages,status):
        try:
            self.messages = messages
            payload = {
                "model":self.model,
                "messages":self.messages,
                "keep_alive": -1,
                "stream":True}

            self.status = status
            response_text = ""
            first_line = True

            response = requests.post(self.chat_url, json=payload, stream=True, timeout=300)
            response.raise_for_status()

            for line in response.iter_lines():
                if first_line:
                    # This clears the spinner line and resets output
                    self.status.stop() 
                    self.console.print("Apollo: ",style="#fcc200",end="")
                    first_line = False

                data = json.loads(line.decode("utf-8"))
                self.console.print(data["message"]["content"], end="")
                response_text += data["message"]["content"]
            return response_text

        except HTTPError as e:
            self.status.stop()
            self.console.print(f"Error: HTTP {e.response.status_code} - {e}", style="red bold")
            return None
        except requests.exceptions.ConnectionError:
            self.status.stop()
            self.console.print("Error: Failed to connect to Ollama server. Ensure Ollama server is online and try again.", style="red bold")
            return None

        except Timeout:
            self.status.stop()
            self.console.print("Error: Connection to Ollama server timed out. Ensure Ollama server is online and try again.", 
                             style="red bold")
            return None

        except RequestException as e:
            self.status.stop()
            self.console.print(f"Error: Network error during generation: {e}\n Restart Ollama server and try again.", 
                             style="red bold")
            return None


        except KeyboardInterrupt:
            self.status.stop()
            self.console.print("\nRequest cancelled.", style="red bold")
            return None

    def pull_model(self, new_model, status):
        try:
            self.status = status
            self.new_model = new_model
            payload = {
                "model": self.new_model}

            response = requests.post(self.pull_url, json=payload, timeout=300)
            response.raise_for_status()
            self.status.stop()
            self.console.print(f"Model: {self.new_model} loaded successfully!")
            return self.new_model
        except HTTPError as e:
            self.status.stop()
            if e.response.status_code == 404:
                self.console.print(f"Error: Model '{model}' not found in Ollama", style="red bold")
            else:
                self.console.print(f"Error: HTTP {e.response.status_code} - {e}", style="red bold")
            return None

        except requests.exceptions.ConnectionError:
            self.status.stop()
            self.console.print("Error: Failed to connect to Ollama server. Ensure Ollama server is online and try again.", style="red bold")
            return None

        except Timeout:
            self.status.stop()
            self.console.print("Error: Connection to Ollama server timed out. Ensure Ollama server is online and try again.", 
                             style="red bold")
            return None

        except RequestException as e:
            self.status.stop()
            self.console.print(f"Error: Network error during initialization: {e}\n Restart Ollama server and try again.", 
                             style="red bold")
            return None
 
        except KeyboardInterrupt:
            self.status.stop()
            self.console.print("\nRequest cancelled.", style="red bold")
            return None

        except Exception as e:
            self.status.stop()
            self.console.print(f"Error Occured:{e}", style="red bold")
            return None

    def swap_model(self, model, status):

        self.model = model
        self.status = status
        payload = {
                        "model": self.model,
                        "keep_alive":-1
            }

        try:
            preload = requests.post(self.chat_url,json=payload, timeout=300)
            preload.raise_for_status()
            self.status.stop()
            self.console.print(f"Current loaded model: {self.model}")
            return self.model
        except HTTPError as e:
            self.status.stop()
            if e.response.status_code == 404:
                self.console.print(f"Error: Model '{self.model}' not found in Ollama", style="red bold")
            else:
                self.console.print(f"Error: HTTP {e.response.status_code} - {e}", style="red bold")
            return None

        except requests.exceptions.ConnectionError:
            self.status.stop()
            self.console.print("Error: Failed to connect to Ollama server. Ensure Ollama server is online and try again.", style="red bold")
            return None

        except Timeout:
            self.status.stop()
            self.console.print("Error: Connection to Ollama server timed out. Ensure Ollama server is online and try again.", 
                             style="red bold")
            return None

        except RequestException as e:
            self.status.stop()
            self.console.print(f"Error: Network error during initialization: {e}\n Restart Ollama server and try again.", 
                             style="red bold")
            return None

        except KeyboardInterrupt:
            self.status.stop()
            self.console.print("\nRequest cancelled.", style="red bold")
            return None

        except Exception as e:
            self.status.stop()
            self.console.print(f"Error Occured:{e}", style="red bold")
            return None

    def list_model(self, status):
        try: 
            self.status = status
            response = requests.get(self.list_models_url, timeout=300)
            response.raise_for_status()
            self.status.stop()
            model_list = []
            data = response.json()
            return data["models"][0]["model"]

        except HTTPError as e:
            self.status.stop()
            self.console.print(f"Error: HTTP {e.response.status_code} - {e}", style="red bold")
            return None
        except KeyboardInterrupt:
            self.status.stop()
            self.console.print("\nRequest cancelled.", style="red bold")
            return None

        except requests.exceptions.ConnectionError:
            self.status.stop()
            self.console.print("Error: Failed to connect to Ollama server. Ensure Ollama server is online and try again.", style="red bold")
            return None

        except Timeout:
            self.status.stop()
            self.console.print("Error: Connection to Ollama server timed out. Ensure Ollama server is online and try again.", 
                             style="red bold")
            return None

        except RequestException as e:
            self.status.stop()
            self.console.print(f"Error: Network error during initialization: {e}\n Restart Ollama server and try again.", 
                             style="red bold")
            return None
 
        except Exception as e:
            self.status.stop()
            self.console.print(f"Error Occured:{e}", style="red bold")
            return None


    def generate_embeddings(self,text):
        try:
            payload = {
                       "model": self.embedding_model,
                       "input": text}

            response = requests.post(self.generate_embeddings_url, json=payload, timeout=300)
            response.raise_for_status()
            data = response.json()
            return data["embeddings"]

        except HTTPError as e:

            if e.response.status_code == 404:
                self.console.print(f"Error: Model '{self.embedding_model}' not found in Ollama", style="red bold")
            else:
                self.console.print(f"Error: HTTP {e.response.status_code} - {e}", style="red bold")
            return None
        except KeyboardInterrupt:
            self.console.print("\nRequest cancelled.", style="red bold")
            return None

        except requests.exceptions.ConnectionError:
            self.console.print("Error: Failed to connect to Ollama server. Ensure Ollama server is online and try again.", style="red bold")
            return None

        except Timeout:
            self.console.print("Error: Connection to Ollama server timed out. Ensure Ollama server is online and try again.", 
                             style="red bold")
            return None

        except RequestException as e:
            self.console.print(f"Error: Network error during initialization: {e}\n Restart Ollama server and try again.", 
                             style="red bold")
            return None

        except Exception as e:
            self.console.print(f"Error Occured:{e}", style="red bold")
            return None



