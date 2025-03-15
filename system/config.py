from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Fukuro System"
    DEBUG: bool = True
    VERSION: str = "0.1.0"
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str = 'postgresql://fukuro:fukuro@localhost/fukurodb' 
    SQLALCHEMY_DATABASE_URL: str = 'postgresql://fukuro:fukuro@localhost/fukurodb' 
    
    # Fields for other environment variables
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"

    class Config:
        env_file = ".env"  # Ensure the .env file is loaded
        extra = 'allow'  # Allow extra fields

settings = Settings()
