from dataclasses import dataclass, field
from datetime import datetime, date, time, timezone, UTC
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
  db_url: str = f"postgresql+psycopg://postgres:developserver@localhost:5432/kolak_inv"

settings = Settings()



@dataclass()
class Timestamp:
  time_zone: bool = field(default=False)

  def get_datetime(self) -> datetime:
    if self.time_zone:
      return datetime.now(UTC)
    return datetime.now()

  def get_time(self) -> time:
    return self.get_datetime().time()

  def get_date(self) -> date:
    return self.get_datetime().date()


PROJECT_DATETIME = Timestamp(time_zone=False)
