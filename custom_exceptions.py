class OllamaHTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"HTTP {status_code}: {message}")

class OllamaConnectionError(Exception):
     def __init__(self, message):
        self.message = message
        super().__init__(f"{message}")

class OllamaTimeoutError(Exception):
     def __init__(self, message):
        self.message = message
        super().__init__(f"{message}")

class OllamaNetworkError(Exception):
     def __init__(self, message):
        self.message = message
        super().__init__(f"{message}")

class OllamaModelNotFoundError(Exception):
     def __init__(self, message):
        self.message = message
        super().__init__(f"{message}")

