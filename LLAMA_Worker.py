from da_console import console
import os
import requests
import json
#TODO: make function only be inited once and not constantly

class Llama_Worker():
    def __init__(self):
        """Initialization of LLAMA"""
        self.server = "http://100.111.62.92:8000/api/chat"
        payload = {
                    "model":"mistral:7b",
                    "keep_alive":-1,
                    "stream":True}

        # empty request to preload the model
        preload = requests.post(self.server,json=payload )
    
    def generate_response(self,messages,status):
        try:
            self.messages = messages
            payload = {
                "model":"mistral:7b",
                "messages":self.messages,
                "keep_alive": -1,
                "stream":True}

            self.status = status
            response_text = ""
            first_line = True
            
            response = requests.post(self.server, json=payload, stream=True)
                               
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
