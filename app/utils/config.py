# ==============================================================================
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By: Abhisek Ashirbad Sethy
# Created Date: 05/09/2023 (DD/MM/YYYY)
# Copyright: Apache License v2.0
# ==============================================================================

# Imports
import os
from dotenv import load_dotenv

load_dotenv()

#Database Configuration
DB_ECHO = False
DB_AUTOCOMMIT = True
DB_AUTOFLUSH = False
DB_URL = os.getenv("DATABASE_URL")