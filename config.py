from pydantic_settings import BaseSettings, SettingsConfigDict


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
    )

    bot_token: str
    admin_ids: frozenset[int] = frozenset({42, 701372755})


settings = Setting()
