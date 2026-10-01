from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  db_url: str = f"postgresql+psycopg://postgres:developserver@localhost:5432/kolak_inv"

settings = Settings()




