import uvicorn
from starlette.middleware.cors import CORSMiddleware

from routers import mainpage_router

if __name__ == "__main__":
    app = mainpage_router.app
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    uvicorn.run(app, host="127.0.0.1", port=8000)
