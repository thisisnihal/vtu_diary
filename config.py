from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = ""
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL_NAME: str = "" 
    VTU_EMAIL: str = ""
    VTU_PASSWORD: str = ""
    
    DAILY_WORK_HRS: int = 8
    
    class Config:
        env_file = ".env"
        env_file_encoding='utf-8'
        case_sensitive=True
        extra="ignore"
        


settings = Settings()