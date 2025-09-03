from llama_cpp import Llama
from da_console import console
import os
import sys
import contextlib

@contextlib.contextmanager
def suppress_stderr():
    """Suppress stderr output temporarily (like llama.cpp log spam)."""
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr


class Llama_Worker():
    def __init__(self,model_path,messages,threads=6,context=2048,gpu_layers=0):
        """Initialization of LLAMA"""
        self.model_path = model_path
        self.messages = messages
        self.threads = threads
        self.context = context
        self.gpu_layers = gpu_layers

    def generate_response(self,status=None):
        try:
            with suppress_stderr():
                llm = Llama(
                    model_path=self.model_path,
                    n_ctx=self.context,
                    n_threads=self.threads,
                    n_gpu_layers=self.gpu_layers,
                    verbose=False # Set to True for debugging
                )
            self.status = status
            response_text = ""
            first_chunk = True
            
            with suppress_stderr():
                
                for chunk in llm.create_chat_completion(messages=self.messages, temperature=0.3, max_tokens=1024, stream=True):
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        response_text += delta

                        if first_chunk:
                            # This clears the spinner line and resets output
                            self.status.stop() 
                            console.print("Apollo: ",style="#fcc200",end="")
                            first_chunk = False

                        console.print(delta, end="")
                        console.file.flush()
            return response_text



        except Exception as e:
            console.print(f"Error Occured:{e}", style="red bold")
        except KeyboardInterrupt:
            console.print("\nRequest cancelled.", style="red bold")
