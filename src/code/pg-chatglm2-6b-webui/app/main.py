"""Main module to run the server."""
import uvicorn
from app.config import PORT

uvicorn.run("server:app", host="0.0.0.0", port=PORT)
