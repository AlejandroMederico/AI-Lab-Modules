# backend/logger/logger.py
import logging
from pathlib import Path
from datetime import datetime

# Ruta absoluta a carpeta /logs
BASE_DIR = Path(__file__).resolve().parent.parent  # apunta a /backend
LOG_DIR = BASE_DIR / "logger" / "logs"
LOG_DIR.mkdir(exist_ok=True)

log_filename = datetime.now().strftime("app_%Y-%m-%d.log")
log_path = LOG_DIR / log_filename

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(log_path, encoding="utf-8"), logging.StreamHandler()],
)

logger = logging.getLogger("agente_empleo")
