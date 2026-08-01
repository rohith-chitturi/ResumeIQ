from pydantic_settings import BaseSettings

class FeatureFlags(BaseSettings):
    ENABLE_BATCH: bool = True
    ENABLE_VECTOR_SEARCH: bool = True
    ENABLE_METRICS: bool = True
    ENABLE_EXPORT: bool = True

features = FeatureFlags()
