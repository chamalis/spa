from pathlib import Path

from decouple import RepositoryEnv, Config

BASE_DIR = Path(__file__).resolve().parent.parent
env_file_path = BASE_DIR.joinpath('.env')
env_config = Config(RepositoryEnv(env_file_path))

# Settings start below this line, change according to ur needs
DEBUG = env_config.get('DEBUG', cast=bool, default=False)
# Logging sensitivity
LOGLEVEL = 'debug' if DEBUG else env_config.get('LOGLEVEL', default='info')

DB_HOST = env_config.get('DB_HOST', default='127.0.0.1')
DB_PORT = env_config.get('DB_PORT', cast=int, default=5432)
DB_NAME = env_config.get('POSTGRES_DB', default='spa')
DB_USER = env_config.get('POSTGRES_USER', default='postgres')
DB_PASS = env_config.get('POSTGRES_PASSWORD', default='postgres')

API_URLPATH = env_config.get('API_V1', default="/api/v1")
