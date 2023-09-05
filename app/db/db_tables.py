# ==============================================================================
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By: Abhisek Ashirbad Sethy
# Created Date: 05/09/2023 (DD/MM/YYYY)
# Copyright: Apache License v2.0
# ==============================================================================

# Imports
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()

class Books(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    genre = Column(String)

