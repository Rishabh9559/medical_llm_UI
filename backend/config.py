from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str = "medical_llm_db"
    llm_api_url: str
    llm_api_key: str
    llm_model: str = "rishabh9559/medical-llama-3.2-3B"
    
    class Config:
        env_file = ".env"

settings = Settings()
