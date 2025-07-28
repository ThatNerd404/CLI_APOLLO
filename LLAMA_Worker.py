from llama_cpp import Llama
from da_console import console


class Llama_Worker():
    def __init__(self,model_path,messages,threads=6,context=2048,gpu_layers=0):
        self.model_path = model_path
        self.messages = messages
        self.threads = threads
        self.context = context
        self.gpu_layers = gpu_layers

    def generate_response(self,status=None):
        try:
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
            for chunk in llm.create_chat_completion(messages=self.messages, temperature=0.7, stream=True):
                delta = chunk["choices"][0]["delta"].get("content", "")
                if delta:
                    response_text += delta

                    if first_chunk:
                        # This clears the spinner line and resets output
                        self.status.stop() 
                        first_chunk = False

                    console.print(delta, end="")
                    console.file.flush()
            return response_text



        except Exception as e:
            console.print(f"Error Occured:{e}", style="red bold")
        except KeyboardInterrupt:
            console.print("\nRequest cancelled.", style="red bold")
