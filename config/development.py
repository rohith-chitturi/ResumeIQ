from config.base import Settings

class DevSettings(Settings):
    ENVIRONMENT: str = "development"
    
dev_settings = DevSettings()
