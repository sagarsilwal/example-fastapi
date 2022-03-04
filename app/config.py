from pydantic import BaseSettings


#to set up environment variables
class Settings(BaseSettings):
  #database_password: str = "localhost"
  #database_username: str = "postgres"
  #secret_key: str = "2155456gtjkuguvtdc"
  database_hostname: str 
  database_port: str 
  database_password: str
  database_name: str
  database_username: str
  secret_key: str
  algorithm: str
  access_token_expire_minutes: int

  class Config:
      env_file = ".env"

#creating instance of Settings class
settings = Settings()
