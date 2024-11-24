from pydantic_settings import BaseSettings

# Define a Settings class that inherits from BaseSettings to manage application configurations.
class Settings(BaseSettings):
    database_hostname:str
    database_port:str
    # Define a database password with a default value. 
    # This value can be overridden by an environment variable if one is set.
    database_password: str 
    # Define a database username with a default value.
    # This too can be replaced by an environment variable.
    database_username: str 
    database_name :str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int
    
    class Config:
        env_file = ".env"
    

# Create an instance of the Settings class to access the configuration values.
# Any configuration defined in environment variables will override the default values.
settings = Settings()

# Access configuration attributes like settings.database_password, settings.database_username, etc.