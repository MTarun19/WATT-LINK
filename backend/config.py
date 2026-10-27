import os

# ==========================================
# Project
# ==========================================

PROJECT_NAME = "WATT LINK"
VERSION = "1.0.0"

# ==========================================
# Database Configuration
# ==========================================

DB_USERNAME = "root"
DB_PASSWORD = "mysql"      
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "watt_link"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# ==========================================
# JWT Configuration
# ==========================================

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "WATT_LINK_SECRET_KEY_2026"
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ==========================================
# LLM Configuration
# ==========================================

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3"
)

# ==========================================
# Agentic AI Settings
# ==========================================

AI_ENABLED = True
MEMORY_SIZE = 200
CONFIDENCE_THRESHOLD = 0.75

# ==========================================
# ESP32 MQTT Configuration
# ==========================================

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "wattlink/sensors"

# ==========================================
# Logging
# ==========================================

LOG_LEVEL = "INFO"