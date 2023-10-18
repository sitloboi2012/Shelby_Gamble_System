# -*- coding: utf-8 -*-
import logging

import logging_setup
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import finnhub

logger = logging.getLogger("Backend")

app = FastAPI(openapi_url="/api/shelby-backend/openapi.json", docs_url="/api/shelby-backend/docs")

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(finnhub.router)

if __name__ == "__main__":
    uvicorn.run("main:app", workers=1, host="0.0.0.0", port=8080)
