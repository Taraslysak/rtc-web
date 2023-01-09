import sys

REDIS_OM_PATH = "redis_om"

if REDIS_OM_PATH not in sys.path:
    sys.path += [REDIS_OM_PATH]

from aredis_om import HashModel, Field, Migrator
