from django.db.backends.mysql import base as mybase

# Some of these import MySQLdb, so import them after checking if it's installed.
from .features import DatabaseFeatures  # isort:skip


class DatabaseWrapper(mybase.DatabaseWrapper):
    features_class = DatabaseFeatures
