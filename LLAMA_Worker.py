from da_console import console
import os
import requests
import json

class Llama_Worker():
    def __init__(self,model="mistral:7b"):
        """Initialization of LLAMA"""
        self.chat_server = "http://100.111.62.92:11434/api/chat"
        self.pull_server = "http://100.111.62.92:11434/api/pull"

        self.model = model
        payload = {
                    "model": self.model,
                    "keep_alive":-1,
                    "stream":True,
                    "messages":[]}
        try:
            # empty request to preload the model
            preload = requests.post(self.chat_server,json=payload )
            console.print("loaded successfully")
        except Exception as e:
            console.print(f"Error occurred: {e}")

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
            
            response = requests.post(self.chat_server, json=payload, stream=True)
                               
            for line in response.iter_lines():
                if first_line:
                    # This clears the spinner line and resets output
                    self.status.stop() 
                    console.print("Apollo: ",style="#fcc200",end="")
                    first_line = False

                data = json.loads(line.decode("utf-8"))
                console.print(data["message"]["content"], end="")
                response_text += data["message"]["content"]
            return response_text

        except Exception as e:
            console.print(f"Error Occured:{e}", style="red bold")
        except KeyboardInterrupt:
            console.print("\nRequest cancelled.", style="red bold")
    
    def pull_model(self, new_model, status):
        try:
            self.status = status
            self.new_model = new_model
            payload = {
                "model": self.new_model}
            
            response = requests.post(self.pull_server, json=payload)
            self.status.stop()
            console.print(f"Model: {self.new_model} loaded successfully!")
            return self.new_model

        except Exception as e:
            console.print(f"Error Occured:{e}", style="red bold")
        except KeyboardInterrupt:
            console.print("\nRequest cancelled.", style="red bold")

    def swap_model(self, model, status):
        try:
            self.model = model
            self.status = status
            payload = {
                        "model": self.model,
                        "keep_alive":-1
            }

            # empty request to preload the model
            preload = requests.post(self.chat_server,json=payload )
            
            self.status.stop()
            console.print(f"Current loaded model: {self.model}")
            return self.model

        except Exception as e:
            console.print(f"Error Occured:{e}", style="red bold")

        except KeyboardInterrupt:
            console.print("\nRequest cancelled.", style="red bold")


