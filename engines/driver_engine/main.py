from fastapi import FastAPI
from engines.driver_engine.routes import router

app = FastAPI(title="Driver Engine")
app.include_router(router)

# Note: This engine is now part of the main application at engines/main.py
# Start the unified application instead:
#   uvicorn engines.main:app --port 8001 --reload
#
# To run this engine standalone (for development/testing):
#   uvicorn engines.driver_engine.main:app --port 8008 --reload
