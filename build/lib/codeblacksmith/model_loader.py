import os
import ollama
from langchain_openai import AzureChatOpenAI
from langchain_ollama import ChatOllama

# Ensure environment variables are loaded globally
from . import config

class ModelLoader:
    """
    Abstract class to load an LLM model dynamically based on environment variables.
    Supports Azure OpenAI and Ollama.
    """

    def __init__(self):
        self.provider = os.getenv("MODEL_PROVIDER", "ollama").lower()

    def get_model(self):
        """Load the model based on the selected provider."""
        if self.provider == "azure":
            return self._load_azure_model()
        elif self.provider == "ollama":
            return self._load_ollama_model()
        else:
            raise ValueError(f"Invalid MODEL_PROVIDER: {self.provider}")

    def _load_azure_model(self):
        """Load Azure OpenAI model using environment variables."""
        return AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-35-turbo"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-06-01-preview"),
            temperature=float(os.getenv("AZURE_OPENAI_TEMPERATURE", 0)),
            max_tokens=os.getenv("AZURE_OPENAI_MAX_TOKENS"),
            timeout=os.getenv("AZURE_OPENAI_TIMEOUT"),
            max_retries=int(os.getenv("AZURE_OPENAI_MAX_RETRIES", 2))
        )

    def _load_ollama_model(self):
        """Load Ollama model using environment variables."""
        model_name = os.getenv("OLLAMA_MODEL_NAME", "mistral")
        return ChatOllama(model=model_name)

    def get_available_models(self):
        """Retrieve available models based on the provider."""
        if self.provider == "azure":
            return []  # No API for listing Azure models
        elif self.provider == "ollama":
            try:
                return [m["name"] for m in ollama.list()["models"]]
            except Exception:
                return []
        return []
    
    def check_if_model_exists(self, model_name):
        if self.provider == "ollama":
            available_models = [m["model"] for m in ollama.list()["models"]]
            if model_name in available_models:
                return True
            else:
                error_message = (
                    f"❌ Model '{model_name}' not found in Ollama.\n"
                    f"📥 To download it, run:\n\n"
                    f"   ollama pull {model_name}\n"
                    f"\n🔹 Available models: {', '.join(available_models) if available_models else 'None'}"
                )
                raise ValueError(error_message)
        else:
            return True

# Usage Example:
if __name__ == "__main__":
    loader = ModelLoader()
    model = loader.get_model()
    print(f"✅ Loaded model: {model}")
    print(f"📜 Available models: {loader.get_available_models()}")