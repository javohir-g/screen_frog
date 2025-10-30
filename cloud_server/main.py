from fastapi import FastAPI
from cloud_server.routes import router

app = FastAPI(title="Screen AI Relay (Render)")
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
