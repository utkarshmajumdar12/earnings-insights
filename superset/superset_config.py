from datetime import timedelta
FEATURE_FLAGS = {"ALERT_REPORTS": True}
SECRET_KEY = "2EhYC/dwzYVB1uPoJntvO4wIC7MIrB8uHD/1EbQwQyP4bkg6uigi7g=="

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://superset:superset@postgres:5432/earnings"
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_URL": "redis://redis-cache:6379/0"
}
ROW_LIMIT = 100000
SUPERSET_WEBSERVER_TIMEOUT = 300
EMAIL_REPORTS_CRON_SCHEDULE = "0 13 * * 1-5"   # 13:00 UTC weekdays
