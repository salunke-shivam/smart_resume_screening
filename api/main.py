from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from monitoring.logger import log_info
import config

# create app
app = FastAPI(
    title="Smart Resume Screener",
    description="Agentic AI for resume screening",
    version="1.0.0"
)

# cors for streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# include routes
app.include_router(router)


@app.on_event("startup")
def startup():
    log_info("Server starting up")
    log_info(f"Environment: {config.APP_ENV}")