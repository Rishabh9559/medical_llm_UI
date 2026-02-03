from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "medical_llm_db"
    llm_api_url: str = "https://8000-dep-01kghvzqm6m9vdvjhjzmta1e19-d.cloudspaces.litng.ai/v1/chat/completions"
    llm_api_key: str = "88f48d77-00b2-4090-8737-c2f7b1e5c64f"
    llm_model: str = "rishabh9559/medical-llama-3.2-3B"
    
    class Config:
        env_file = ".env"

settings = Settings()
