# ==============================================================================
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By: Abhisek Ashirbad Sethy
# Created Date: 05/09/2023 (DD/MM/YYYY)
# Copyright: Apache License v2.0
# ==============================================================================

# Imports
import os
from fastapi import FastAPI
from app.routes import BookHandler
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
bookhandler=BookHandler()

app.include_router(bookhandler.router)

if __name__ == "__main__":
    from uvicorn import run
    host = os.getenv("HOST", "localhost")
    port = int(os.getenv("PORT", 8000))
    workers = int(os.getenv("WORKERS", 1))
    run(app, host=host, port=port, workers=workers)