import os
import requests
import json

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
        payload = {
                    "model": self.model,
                    "keep_alive":-1,
                    "stream":True}
        # empty request to preload the model
        preload = requests.post(self.chat_url,json=payload )

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
            
            response = requests.post(self.chat_url, json=payload, stream=True)
                               
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

        except Exception as e:
            self.console.print(f"Error Occured:{e}", style="red bold")
        except KeyboardInterrupt:
            self.console.print("\nRequest cancelled.", style="red bold")
    
    def pull_model(self, new_model, status):
        try:
            self.status = status
            self.new_model = new_model
            payload = {
                "model": self.new_model}
            
            response = requests.post(self.pull_url, json=payload)
            self.status.stop()
            self.console.print(f"Model: {self.new_model} loaded successfully!")
            return self.new_model

        except Exception as e:
            self.console.print(f"Error Occured:{e}", style="red bold")
        except KeyboardInterrupt:
            self.console.print("\nRequest cancelled.", style="red bold")

    def swap_model(self, model, status):
        try:
            self.model = model
            self.status = status
            payload = {
                        "model": self.model,
                        "keep_alive":-1
            }

            # empty request to preload the model
            preload = requests.post(self.chat_url,json=payload )
            
            self.status.stop()
            self.console.print(f"Current loaded model: {self.model}")
            return self.model

        except Exception as e:
            self.console.print(f"Error Occured:{e}", style="red bold")

        except KeyboardInterrupt:
            self.console.print("\nRequest cancelled.", style="red bold")

    def list_model(self, status):
        try: 
            self.status = status
            response = requests.get(self.list_models_url)
            self.status.stop()
            model_list = []
            data = response.json()
            return data["models"][0]["model"]

        except Exception as e:
            self.console.print(f"Error Occured:{e}", style="red bold")

        except KeyboardInterrupt:
            self.console.print("\nRequest cancelled.", style="red bold")

    def generate_embeddings(self,text):
        try:
            payload = {
                       "model": self.embedding_model,
                       "input": text}

            response = requests.post(self.generate_embeddings_url, json=payload)
            data = response.json()
            return data["embeddings"]

        except Exception as e:
            self.console.print(f"Error Occured:{e}", style="red bold")

        except KeyboardInterrupt:
            self.console.print("\nRequest cancelled.", style="red bold")


