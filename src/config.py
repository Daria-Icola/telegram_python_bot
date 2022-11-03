import logging.config
import os

telegram = {
    "token": os.environ.get("TOKEN"),
    "driver_password": os.environ.get("DRIVER_PASSWORD"),
    "manager_password": os.environ.get("MANAGER_PASSWORD")
}

# # PROD
database = {
    "db_user": os.environ.get("DATABASE_USER"),
    "db_password": os.environ.get("DATABASE_PASSWORD"),
    "db": os.environ.get("DATABASE"),
    "host": os.environ.get("HOST"),
    "port": os.environ.get("PORT")
}

# # # # TEST
# database = {
#     "db_user": os.environ.get("POSTGRES_USER"),
#     "db_password": os.environ.get("POSTGRES_PASSWORD"),
#     "db": os.environ.get("POSTGRES_DB"),
#     "host": os.environ.get("HOST"),
#     "port": os.environ.get("PORT")
# }

# create logger
logging.config.fileConfig('./logging/logging.conf')
logger = logging.getLogger('reports_bot')
