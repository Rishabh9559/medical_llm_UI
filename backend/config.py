from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str = "medical_llm_db"
    llm_api_url: str
    llm_api_key: str
    llm_model: str = "rishabh9559/medical-llama-3.2-3B"
    
    # JWT Settings
    secret_key: str = "3zYHS5tyrfj29VxZCgJHmNJktdgq1nhNaSXHYrnloc4"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # Email Settings
    gmail_user: str = ""
    gmail_pass: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
