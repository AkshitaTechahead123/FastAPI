from app.main import router
import uvicorn
from fastapi import FastAPI
app = FastAPI()
app.include_router(router= router)
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
