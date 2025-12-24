from fastapi import FastAPI
from engines.pit_engine.routes import router

app = FastAPI(title="Pit Engine")
app.include_router(router)

# Note: This engine is now part of the main application at engines/main.py
# Start the unified application instead:
#   uvicorn engines.main:app --port 8001 --reload
#
# To run this engine standalone (for development/testing):
#   uvicorn engines.pit_engine.main:app --port 8006 --reload
