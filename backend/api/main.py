"""
backend/api/main.py — FastAPI application entry point.
Registers the prediction router and CORS middleware.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load .env from project root (two levels up from backend/api/)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

from .routers import predict

app = FastAPI(
    title="Football Analytics API",
    description=(
        "Predicts **HomeNoLose**, the probability that the home team does not lose "
        "(home win or draw), from bookmaker odds and the Asian Handicap.\n\n"
        "Predictions use the 6-feature CatBoost model "
        "(`ml_exploratory_analysis/models/catboost_6feat.cbm`). "
        "`/predict/data-stats` reads from the MySQL data warehouse; "
        "the other endpoints need only the model and its results files."
    ),
    version="1.0.0",
)

cors_origin = os.getenv("CORS_ORIGIN", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[cors_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router)
