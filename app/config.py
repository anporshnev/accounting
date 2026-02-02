from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import find_dotenv


class DBSettings(BaseSettings):
    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int

    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='ignore')

    @property
    def db_url(self):
        return (f"postgresql+asyncpg://"
                f"{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}")

class SecuritySettings(BaseSettings):
    secret_key: SecretStr = Field(validation_alias='SEC_SECRET_KEY')
    algorithm: str = Field(validation_alias='SEC_ALGORITHM')
    access_token_expire: int = Field(validation_alias='SEC_ACCESS_TOKEN_EXPIRE_MINUTES')
    refresh_token_expire: int = Field(validation_alias='SEC_REFRESH_TOKEN_EXPIRE_MINUTES')

    model_config = SettingsConfigDict(env_file=find_dotenv(), extra='ignore')

class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()
    security_settings: SecuritySettings = SecuritySettings()

settings = Settings()