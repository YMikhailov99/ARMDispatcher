import uvicorn
from routers import mainpage_router


if __name__ == "__main__":
    app = mainpage_router.app
    uvicorn.run(app, host="127.0.0.1", port=8000)
