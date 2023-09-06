# ==============================================================================
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By: Abhisek Ashirbad Sethy
# Created Date: 05/09/2023 (DD/MM/YYYY)
# Copyright: Apache License v2.0
# ==============================================================================

# Imports
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.query import Query
from time import sleep

class RetryingQuery(Query):

    __retry_count__ = 3
    __retry_sleep_interval_sec__ = 0.5

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __iter__(self):
        attempts = 0
        while True:
            attempts += 1
            try:
                return super().__iter__()
            except OperationalError as ex:
                if "Connection lost to database during query" not in str(ex):
                    raise
                if attempts < self.__retry_count__:
                    self.__retry_sleep_interval_sec__, attempts
                    sleep(self.__retry_sleep_interval_sec__)
                    continue
                else:
                    raise

    def filter_if(self: Query, condition: bool, *criterion):
        if condition:
            return self.filter(*criterion)
        else:
            return self